"""Re-evaluate the saved associative-recall models on CPU.

Install torch, numpy and einops. Check out Ivann1242/Analysis-AR-problem at
d148ad9d87f79df33ed64a0e22cd34d432dda44f. Supply the AR_II notebook and
its training checkpoints, named as in the notebook.

python evaluate.py --notebook AR_II.ipynb --checkpoints weights --out results

Pass --fixed-checkpoints with the AR_I checkpoint directory to export its
stored end-of-epoch validation histories as well.
"""

import argparse
import csv
import gzip
import hashlib
import io
import json
import sys
import types
from pathlib import Path

import einops
import numpy as np
import torch


NOTEBOOK_SHA256 = "64d30e827bafc74fe410dbea174afbb735c77f4e217a1ba6e76d98753318ae89"
SEED = 202511
SAMPLES = 1024
LENGTHS = (32, 64, 96)
MASKS = ("unmasked", "key", "value", "distractor")


def load_architectures(path):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != NOTEBOOK_SHA256:
        raise ValueError("Use AR_II.ipynb from the revision in the module docstring.")
    cells = json.loads(data)["cells"]
    module = types.ModuleType("recall_notebook_models")
    sys.modules[module.__name__] = module
    # Only the imports and model definitions from the verified notebook.
    for index in (0, 1, 5, 6, 7, 8, 9):
        source = "".join(cells[index]["source"])
        exec(compile(source, f"AR_II.ipynb:cell{index}", "exec"), module.__dict__)
    return module


def examples(length, keys, offset):
    """One final query. Filler is uniform on the 15 symbols other than that key."""
    rng = np.random.default_rng(np.random.SeedSequence([SEED, length, keys, offset]))
    row = np.arange(SAMPLES)
    query = rng.integers(keys, size=SAMPLES)
    target = rng.integers(16, size=SAMPLES)
    tokens = rng.integers(15, size=(SAMPLES, length))
    tokens += tokens >= query[:, None]
    key_pos = rng.integers(length - offset - 1, size=SAMPLES)
    value_pos = key_pos + offset
    tokens[row, key_pos] = query
    tokens[row, value_pos] = target
    tokens[:, -1] = query

    # A uniform prefix position excluding the planted key and value.
    distractor = rng.integers(length - 3, size=SAMPLES)
    distractor += distractor >= key_pos
    distractor += distractor >= value_pos
    return tuple(torch.from_numpy(a) for a in (tokens, target, key_pos, value_pos, distractor))


def build_model(module, architecture, width):
    if architecture == "hybrid":
        return module.HybridNet(16, width, max_len=128, attn_block_class=module.Block)
    if architecture == "mamba":
        return module.MambaNet(16, d_model=width, n_layer=2)
    return module.BaseNet(16, width, is_pe=False, max_len=128, attn_layers=2, block=module.BlockRoPE)


def probe_readout(model, tokens, key, value, distractor, native_logits):
    states = model.mamba_layer(model.embedding(tokens))
    q, k, v = model.att.c_attn(states).chunk(3, dim=-1)
    scores = (q[:, -1:] @ k.transpose(1, 2)).squeeze(1) / k.size(-1) ** 0.5
    rows = torch.arange(len(tokens))
    predictions = {}
    attention = {}
    for label, position in zip(MASKS, (None, key, value, distractor)):
        masked = scores.clone()
        if position is not None:
            masked[rows, position] = -torch.inf
        attention[label] = masked.softmax(dim=-1)
        context = attention[label].unsqueeze(1) @ v
        logits = model.head(model.norm_f(context)).squeeze(1)
        if position is None:
            torch.testing.assert_close(logits, native_logits, rtol=3e-4, atol=3e-4)
            if not torch.equal(logits.argmax(-1), native_logits.argmax(-1)):
                raise ValueError("Reconstructed readout disagrees with the notebook model.")
        predictions[label] = logits.argmax(-1)
    return predictions, scores.argmax(-1), attention


@torch.inference_mode()
def worked_example(model):
    alphabet = "ABCDEFGHIJKLMNOP"
    prefix = "DABCE"
    queries = {}
    for query in ("A", "C"):
        tokens = torch.tensor([[alphabet.index(symbol) for symbol in prefix + query]])
        key = torch.tensor([prefix.index(query)])
        pred, _, attention = probe_readout(
            model, tokens, key, key + 1, torch.tensor([0]), model(tokens)[:, -1]
        )
        queries[query] = {
            "key_pos": key.item(), "value_pos": key.item() + 1, "distractor_pos": 0,
            "target": prefix[key.item() + 1],
            "conditions": {
                label: {"prediction": alphabet[pred[label].item()],
                        "weights": attention[label][0].double().tolist()}
                for label in MASKS
            },
        }
    return {"checkpoint": "hybrid_M16.pth", "prefix": list(prefix), "queries": queries}


@torch.inference_mode()
def evaluate(model, architecture, keys, offset, length, pairs_writer):
    tokens, target, key, value, distractor = examples(length, keys, offset)
    counts = {"unmasked": 0}
    value_top = 0
    for start in range(0, SAMPLES, 32):
        batch = slice(start, start + 32)
        logits = model(tokens[batch])[:, -1]
        if architecture != "hybrid":
            counts["unmasked"] += int((logits.argmax(-1) == target[batch]).sum())
            continue
        predictions, top, _ = probe_readout(
            model, tokens[batch], key[batch], value[batch], distractor[batch], logits
        )
        for label, pred in predictions.items():
            counts[label] = counts.get(label, 0) + int((pred == target[batch]).sum())
        value_top += int((top == value[batch]).sum())
        for j, row in enumerate(range(start, start + len(top))):
            pairs_writer.writerow([
                keys, length, row, int(tokens[row, -1]), int(target[row]), int(key[row]),
                int(value[row]), int(distractor[row]), int(top[j]),
                *(int(predictions[label][j]) for label in MASKS),
            ])
    result = {"length": length, "correct": counts}
    if architecture == "hybrid":
        result["top_attention_at_value"] = value_top
    return result


def export_training(directory, destination):
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["model", "offset", "epoch", "validation_accuracy"])
        for offset in (1, 5):
            for name in ("mamba", "hybrid", "tf_rope", "tf_learned", "tf_nope"):
                suffix = "5" if offset == 5 else ""
                ckpt = torch.load(directory / f"{name}{suffix}.pth", weights_only=True, map_location="cpu")
                history = ckpt["acc_history"]
                if len(history) != ckpt["epoch"] + 1:
                    raise ValueError(f"Incomplete history for {name} at offset {offset}")
                writer.writerows((name, offset, epoch, accuracy)
                                 for epoch, accuracy in enumerate(history, start=1))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", required=True, type=Path)
    parser.add_argument("--checkpoints", required=True, type=Path)
    parser.add_argument("--fixed-checkpoints", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    module = load_architectures(args.notebook)
    torch.set_num_threads(2)
    runs = []
    demo = None
    settings = [(name, keys, 8, 1) for keys in (4, 8, 16) for name in ("tf_rope", "mamba", "hybrid")]
    settings.extend([("mamba", 16, 64, 1), ("mamba", 16, 64, 10)])
    args.out.mkdir(parents=True, exist_ok=True)
    with gzip.GzipFile(filename=str(args.out / "paired-predictions.csv.gz"), mode="wb", mtime=0) as gz:
        with io.TextIOWrapper(gz, encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(["eligible_keys", "length", "sample", "query", "target", "key_pos",
                             "value_pos", "distractor_pos", "top_attention_pos", *MASKS])
            for architecture, keys, width, offset in settings:
                stem = f"{architecture}_M{keys}"
                if width == 64:
                    stem += "_d64"
                if offset == 10:
                    stem += "_t10"
                path = args.checkpoints / (stem + ".pth")
                checkpoint = torch.load(path, map_location="cpu", weights_only=True)
                model = build_model(module, architecture, width)
                model.load_state_dict(checkpoint["model"])
                model.eval()
                if architecture == "hybrid" and keys == 16:
                    demo = worked_example(model)
                runs.append({
                    "checkpoint": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "epochs": checkpoint["epoch"] + 1, "model": architecture,
                    "eligible_keys": keys, "width": width, "offset": offset,
                    "tests": [evaluate(model, architecture, keys, offset, t, writer) for t in LENGTHS],
                })
                print(f"Evaluated {stem}", flush=True)
    result = {
        "notebook_sha256": NOTEBOOK_SHA256, "seed": SEED, "examples_per_condition": SAMPLES,
        "versions": {"torch": str(torch.__version__), "numpy": np.__version__, "einops": einops.__version__},
        "runs": runs, "worked_example": demo,
    }
    (args.out / "results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.fixed_checkpoints:
        export_training(args.fixed_checkpoints, args.out / "training.csv")


if __name__ == "__main__":
    main()
