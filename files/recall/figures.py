"""Render the two article plots from the fixed-key notebook and evaluation JSON.

python figures.py AR_I.ipynb results.json --out images --print-dir print-figures
Requires matplotlib, numpy and Pillow. The compact exports reflow the same data
for a phone screen. The optional PDFs contain selectable text.
"""

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


INK = "#20374b"
TEAL = "#15736b"
RUST = "#ac523a"
SLATE = "#586980"
GRID = "#d8dfe1"
NOTEBOOK_SHA256 = "0fd30ee0670f1abf04a37c55216bcd8b47001fdc39a3b8a817460ed07164beec"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans", "Arial"],
    "font.size": 9, "text.color": INK,
    "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "axes.edgecolor": GRID, "axes.linewidth": 0.7, "svg.fonttype": "none", "pdf.fonttype": 42,
})


def length_curves(path):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != NOTEBOOK_SHA256:
        raise ValueError("Use the AR_I notebook from d148ad9d87f79df33ed64a0e22cd34d432dda44f.")
    cell = json.loads(data)["cells"][13]
    log = "".join("".join(o.get("text", [])) for o in cell["outputs"])
    curves = {}
    for model, length, accuracy in re.findall(r"Model (\w+) @ T=(\d+) accuracy = ([0-9.]+)", log):
        curves.setdefault(model, {})[int(length)] = float(accuracy) * 100
    for model in ("tf_rope", "tf_learned", "tf_nope"):
        if set(curves[model]) != set(range(4, 97)):
            raise ValueError(f"Incomplete length sweep for {model}")
    return curves


def position_chart(curves, compact):
    fig, ax = plt.subplots(figsize=(4.1, 3.0) if compact else (7.3, 3.25))
    fig.subplots_adjust(left=.15 if compact else .10, right=.975, bottom=.19, top=.82)
    ax.grid(axis="y", color=GRID, linewidth=.55)
    ax.set_axisbelow(True)
    ax.axvline(32, color=SLATE, ls=(0, (1, 3)), linewidth=1)
    for key, label, color, style in [
        ("tf_learned", "Learned", RUST, "-"), ("tf_nope", "No positions", SLATE, "--"),
        ("tf_rope", "Rotary", TEAL, "-."),
    ]:
        lengths = sorted(curves[key])
        ax.plot(lengths, [curves[key][t] for t in lengths], label=label, color=color,
                linestyle=style, linewidth=1.55, solid_capstyle="round")
    ax.scatter([32], [curves["tf_learned"][32]], color=RUST, s=22, zorder=3)
    ax.set(xlim=(3, 97), ylim=(-1, 104), xticks=[4, 16, 32, 48, 64, 80, 96],
           yticks=[0, 25, 50, 75, 100], xlabel="Sequence length (tokens)", ylabel="Accuracy (%)")
    ax.tick_params(length=0, pad=4)
    fig.legend(*ax.get_legend_handles_labels(), loc="upper center", bbox_to_anchor=(.51, .985),
               ncol=3, frameon=False, handlelength=1.6, columnspacing=1.3, fontsize=9)
    return fig


def wilson(correct, n):
    z = 1.96
    p = correct / n
    denom = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / denom
    radius = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return 100 * (mid - radius), 100 * (mid + radius)


def readout_chart(results, compact):
    run = next(r for r in results["runs"] if r["model"] == "hybrid" and r["eligible_keys"] == 16)
    test = next(t for t in run["tests"] if t["length"] == 96)
    n = results["examples_per_condition"]
    fig, ax = plt.subplots(figsize=(4.1, 2.85) if compact else (7.3, 2.9))
    fig.subplots_adjust(left=.30 if compact else .20, right=.80 if compact else .88, bottom=.23, top=.95)
    labels = ["All visible", "Block key", "Block value", "Block distractor"]
    ax.axvline(100 / 16, color=SLATE, linewidth=1.1, linestyle=(0, (2, 3)))
    for row, condition in enumerate(("unmasked", "key", "value", "distractor")):
        count = test["correct"][condition]
        pct = 100 * count / n
        low, high = wilson(count, n)
        color = RUST if condition == "value" else TEAL
        ax.hlines(row, 0, 100, color=GRID, linewidth=.8)
        ax.errorbar(pct, row, xerr=[[max(0, pct - low)], [max(0, high - pct)]], fmt="o",
                    markersize=5, color=color, ecolor=color, capsize=3.8, capthick=1.2, linewidth=1.2)
        ax.text(1.04, row, f"{pct:.1f}%", transform=ax.get_yaxis_transform(),
                ha="left", va="center", fontweight="bold", color=color)
    ax.set(xlim=(-2, 103), ylim=(3.6, -.6), xticks=[0, 25, 50, 75, 100],
           yticks=range(4), yticklabels=labels, xlabel="Correct answers (%)")
    ax.tick_params(length=0, pad=4)
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path)
    parser.add_argument("results", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--print-dir", type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if args.print_dir:
        args.print_dir.mkdir(parents=True, exist_ok=True)
    curves = length_curves(args.notebook)
    results = json.loads(args.results.read_text(encoding="utf-8"))
    for compact in (False, True):
        for name, build, data in [("recall-positions", position_chart, curves),
                                  ("recall-readout", readout_chart, results)]:
            fig = build(data, compact)
            stem = name + ("-compact" if compact else "")
            fig.savefig(args.out / f"{stem}.webp", dpi=300, facecolor="white",
                        pil_kwargs={"lossless": True})
            if args.print_dir:
                fig.savefig(args.print_dir / f"{stem}.pdf", facecolor="white")
                fig.savefig(args.print_dir / f"{stem}.svg", facecolor="white")
                fig.savefig(args.print_dir / f"{stem}.png", dpi=600, facecolor="white")
            plt.close(fig)


if __name__ == "__main__":
    main()
