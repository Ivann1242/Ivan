"""Rearrange saved outputs from Ivann1242/Analysis-AR-problem, revision d148ad9.

    python archive_figures.py /path/to/Analysis-AR-problem --out images

Requires matplotlib, numpy and Pillow. Optional --print-dir exports editable
axes and labels for inspection. The variable-key notebooks saved raster plots.
Their M=16 strokes are isolated and recolored in the original coordinates.
The fixed-key notebook also saved numerical scores, used directly in the table.
The original study and figure license is distributed as archive-license.txt.
"""

import argparse
import base64
import hashlib
import io
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
import numpy as np
from PIL import Image


NOTEBOOK_DIGESTS = {
    "AR_I": "0fd30ee0670f1abf04a37c55216bcd8b47001fdc39a3b8a817460ed07164beec",
    "AR_II": "64d30e827bafc74fe410dbea174afbb735c77f4e217a1ba6e76d98753318ae89",
}
INK, MUTED, RULE = "#1d303e", "#52636d", "#dce2e5"
HYBRID, MAMBA, ROTARY = "#116d66", "#365c87", "#a64d32"
WIDE, LONG_GAP = "#644f85", "#796143"
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans", "Arial"],
    "font.size": 10, "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": RULE,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "svg.fonttype": "none", "pdf.fonttype": 42, "figure.facecolor": "white",
})


def read_cells(directory, name):
    raw = (directory / (name + ".ipynb")).read_bytes()
    if hashlib.sha256(raw).hexdigest() != NOTEBOOK_DIGESTS[name]:
        raise ValueError(f"{name} differs from the d148ad9 source revision")
    return json.loads(raw)["cells"]


def saved_plot(cell):
    png = next(out["data"]["image/png"] for out in cell["outputs"]
               if "image/png" in out.get("data", {}))
    with Image.open(io.BytesIO(base64.b64decode(png))) as im:
        return np.array(im.convert("RGB"), dtype=np.int16)


def full_key_stroke(image, frame, first_test_length, display_from, color):
    # Frames are the black axis spines in the pinned, native notebook PNGs.
    left, top, right, bottom = frame
    red, green, blue = image[top:bottom + 1, left:right + 1].transpose(2, 0, 1)
    # Green was drawn last for M=16. Blue/orange competitors and gray furniture
    # have no green excess. Its solid stroke on white is RGB(65,169,65).
    alpha = np.clip((green - np.maximum(red, blue)) / 104, 0, 1)
    pad = (96 - first_test_length) * .05  # Matplotlib's saved horizontal margin
    x, dx = np.linspace(first_test_length - pad, 96 + pad, alpha.shape[1], retstep=True)
    y, dy = np.linspace(105, -5, alpha.shape[0], retstep=True)  # saved ylim = (-.05, 1.05)
    visible = (x >= display_from) & (x <= 96)
    # In these ranges the green curve clears the archived legend. Verify that
    # every interior column has one continuous stroke, including intersections.
    for column in alpha[:, visible].T:
        rows = np.flatnonzero(column > .18)
        if not len(rows) or np.any(np.diff(rows) > 3):
            raise ValueError("An original trace is missing or overlaps another green mark")
    alpha[:, x < display_from - dx] = 0
    rgba = np.empty((*alpha.shape, 4))
    rgba[:, :, :3] = to_rgb(color)
    rgba[:, :, 3] = alpha
    # Stroke centers anchor labels. The underlying pixel data are never fitted.
    centers = []
    for length in (32, 96):
        column = alpha[:, np.argmin(abs(x - length))]
        ink = column > .18
        centers.append(np.average(y[ink], weights=column[ink]))
    extent = (x[0] - dx / 2, x[-1] + dx / 2, y[-1] + dy / 2, y[0] - dy / 2)
    return rgba, extent, centers


def length_chart(curves, start, size):
    fig, ax = plt.subplots(figsize=size)
    compact = size[0] < 5
    left_margin = .17 if compact else .105
    right_margin = (.71 if compact else .81) if start == 32 else .80
    fig.subplots_adjust(left=left_margin, right=right_margin, bottom=.20, top=.85)
    ax.set_xlim(start, 96)
    ax.set_ylim(-2, 104)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.set_xticks([t for t in (16, 32, 48, 64, 80, 96) if t >= start])
    ax.set_xlabel("Test sequence length", labelpad=5)
    ax.set_ylabel("Recall accuracy", labelpad=3)
    ax.tick_params(length=0, pad=4, labelsize=9)
    ax.grid(axis="y", color=RULE, linewidth=.65)
    ax.axvline(32, color=MUTED, linewidth=.85, linestyle=(0, (2, 3)))
    ax.text(32, 1.055, "Trained at 32", transform=ax.get_xaxis_transform(),
            ha="left" if start == 32 else "center", color=MUTED, fontsize=9)
    for label, color, (pixels, extent, (_, end_y)) in curves:
        ax.imshow(pixels, extent=extent, origin="upper", aspect="auto",
                  interpolation="bilinear", zorder=3)
        ax.annotate(label, (96, end_y), xytext=(6, 0), textcoords="offset points",
                    va="center", fontsize=9 if compact else 10, color=color, fontweight="semibold")
    return fig


def project_cover(curves):
    fig, ax = plt.subplots(figsize=(4.5, 2.5))
    fig.subplots_adjust(left=.29, right=.77, bottom=.23, top=.79)
    ax.set(xlim=(32, 96), ylim=(0, 105))
    ax.set_axis_off()
    for x, heading in ((32, "32 tokens"), (96, "96 tokens")):
        ax.axvline(x, color=RULE, linewidth=.8)
        ax.text(x, 1.13, heading, transform=ax.get_xaxis_transform(), ha="center",
                color=INK, fontsize=11, fontweight="bold")
    for label, color, (pixels, extent, (first, last)) in curves:
        ax.imshow(pixels, extent=extent, origin="upper", aspect="auto", interpolation="bilinear")
        ax.scatter([32, 96], [first, last], s=13, color=color, clip_on=False, zorder=3)
        ax.annotate(f"{label}  ≈{first:.0f}%", (32, first), xytext=(-7, 0), textcoords="offset points",
                    ha="right", va="center", fontsize=9, color=color, fontweight="bold")
        ax.annotate(f"≈{last:.0f}%", (96, last), xytext=(7, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=11, color=color, fontweight="bold")
    fig.text(.53, .10, "Recall accuracy  ·  16 possible keys", ha="center", fontsize=9, color=MUTED)
    return fig


def fixed_key_scores(cells):
    scores = {}
    for gap, index in ((1, 13), (5, 21)):
        log = "".join("".join(o.get("text", [])) for o in cells[index]["outputs"])
        matches = re.findall(r"Model (\w+) @ T=96 accuracy = ([0-9.]+)", log)
        if len(matches) != 5:
            raise ValueError("Expected all five logged fixed-key rates at length 96")
        for name, score in matches:
            # 990 trials and four logged decimals identify a unique count.
            # Recover it before rounding the displayed percentages to one decimal.
            count = round(float(score) * 990)
            if f"{count / 990:.4f}" != score:
                raise ValueError(f"Unexpected accuracy for 990 trials: {score}")
            scores[name.removesuffix("5"), gap] = 100 * count / 990
    return scores


def gap_chart(scores, size):
    fig, ax = plt.subplots(figsize=size)
    fig.subplots_adjust(left=.025, right=.98, bottom=.02, top=.98)
    ax.set(xlim=(0, 1), ylim=(-.6, 5.2))
    ax.set_axis_off()
    for x, header in ((.01, "Model"), (.46, "Gap of 1"), (.75, "Gap of 5")):
        ax.text(x, 4.92, header, va="center", fontsize=10, fontweight="semibold")
    ax.hlines(4.58, .01, .985, color=RULE, linewidth=.8)
    rows = [
        ("hybrid", "Hybrid", HYBRID), ("mamba", "Mamba", MAMBA), ("tf_rope", "RoPE", ROTARY),
        ("tf_learned", "Learned positions", MUTED), ("tf_nope", "No explicit positions", MUTED),
    ]
    for i, (name, label, color) in enumerate(rows):
        y = 4 - i
        ax.text(.01, y, label, va="center", fontsize=10)
        for gap, x in ((1, .46), (5, .75)):
            pct = scores[name, gap]
            number = f"{pct:.1f}".removesuffix(".0")
            ax.text(x, y + .055, number + "%", ha="left", va="center",
                    fontsize=10, color=color, fontweight="semibold")
            ax.hlines(y - .28, x, x + .19, linewidth=2, color=RULE)
            ax.hlines(y - .28, x, x + .19 * pct / 100, linewidth=2.5, color=color)
    return fig


def export(fig, name, out, print_dir):
    fig.savefig(out / (name + ".webp"), dpi=300, pil_kwargs={"lossless": True})
    if print_dir:
        fig.savefig(print_dir / (name + ".pdf"))
        fig.savefig(print_dir / (name + ".svg"))
        fig.savefig(print_dir / (name + ".png"), dpi=600)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="Original study checkout at d148ad9")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--print-dir", type=Path)
    args = parser.parse_args()
    args.out.mkdir(exist_ok=True, parents=True)
    if args.print_dir:
        args.print_dir.mkdir(exist_ok=True, parents=True)
    fixed = fixed_key_scores(read_cells(args.archive, "AR_I"))
    variable = read_cells(args.archive, "AR_II")
    narrow = saved_plot(variable[12])
    mamba_frame = (780, 132, 1417, 570)
    architecture = [
        ("Hybrid", HYBRID, full_key_stroke(narrow, (1486, 132, 2123, 570), 4, 16, HYBRID)),
        ("Mamba", MAMBA, full_key_stroke(narrow, mamba_frame, 4, 16, MAMBA)),
        ("RoPE", ROTARY, full_key_stroke(narrow, (75, 132, 712, 570), 4, 16, ROTARY)),
    ]
    widths = [
        ("d = 8, gap 1", MAMBA, full_key_stroke(narrow, mamba_frame, 4, 32, MAMBA)),
        ("d = 64, gap 1", WIDE, full_key_stroke(saved_plot(variable[15]), (76, 39, 925, 640), 4, 32, WIDE)),
        ("d = 64, gap 10", LONG_GAP, full_key_stroke(saved_plot(variable[18]), (76, 39, 922, 640), 11, 32, LONG_GAP)),
    ]
    for suffix, length_size, gap_size in [("", (7.3, 3.2), (7.3, 2.7)),
                                         ("-compact", (4.1, 2.9), (4.1, 2.7))]:
        export(length_chart(architecture, 16, length_size), "recall-archive-models" + suffix, args.out, args.print_dir)
        export(gap_chart(fixed, gap_size), "recall-archive-gap" + suffix, args.out, args.print_dir)
        export(length_chart(widths, 32, length_size), "recall-archive-width" + suffix, args.out, args.print_dir)

    cover = project_cover(architecture[1:])
    preview = io.BytesIO()
    cover.savefig(preview, format="png", dpi=600)
    if args.print_dir:
        cover.savefig(args.print_dir / "recall-archive-cover.pdf")
    plt.close(cover)
    with Image.open(preview) as im:
        for w in (480, 1080):
            resized = im.convert("RGB").resize((w, round(im.height * w / im.width)), Image.Resampling.LANCZOS)
            resized.save(args.out / f"recall-archive-cover-{w}.webp", lossless=True)
            if w == 1080:
                resized.save(args.out / "recall-archive-cover.png", optimize=True)


if __name__ == "__main__":
    main()
