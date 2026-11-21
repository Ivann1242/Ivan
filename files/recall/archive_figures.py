"""Draw the blog plates from the original associative-recall study (d148ad9).

Run with Python, matplotlib, NumPy and Pillow:
    python archive_figures.py /path/to/Analysis-AR-problem --out images/research

training.csv, beside this script, is the original fixed-key validation history.
The variable-key notebooks saved images. Reuse their plotted ink for curves and
read approximate coordinates only where the original colored strokes separate.
No notebook code or model is executed. See archive-license.txt for the license.
"""
import argparse
import base64
import csv
import hashlib
import io
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.path import Path as DrawingPath
import numpy as np
from PIL import Image


DIGESTS = {
    "AR_I.ipynb": "0fd30ee0670f1abf04a37c55216bcd8b47001fdc39a3b8a817460ed07164beec",
    "AR_II.ipynb": "64d30e827bafc74fe410dbea174afbb735c77f4e217a1ba6e76d98753318ae89",
    "training.csv": "5e31ab71547c94591ae2972324f90a1120cce8f5012df0786ff8b68a59278ac7",
}
INK, MUTED, RULE = "#1c303b", "#546471", "#dce3e4"
MAMBA, ROTARY, HYBRID = "#385f91", "#a8452d", "#126c60"
PURPLE = "#735484"
MODELS = [("mamba", "Mamba"), ("hybrid", "Hybrid"), ("tf_rope", "RoPE"),
          ("tf_learned", "Absolute"), ("tf_nope", "No positions")]
ARCHITECTURES = [("Mamba", MAMBA, "o"), ("RoPE", ROTARY, "^"), ("Hybrid", HYBRID, "D")]
SIZE = (4.8, 3.6)
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans", "Arial"],
    "font.size": 10.5, "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": RULE,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "svg.fonttype": "none", "pdf.fonttype": 42, "figure.facecolor": "white",
})


def verified(path):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != DIGESTS[path.name]:
        raise ValueError(f"Unexpected revision of {path.name}")
    return data


def notebook_png(cell):
    png = next(o["data"]["image/png"] for o in cell["outputs"] if "image/png" in o.get("data", {}))
    with Image.open(io.BytesIO(base64.b64decode(png))) as im:
        return np.array(im.convert("RGB"), dtype=np.int16)


class RasterPanel:
    """Native axes rectangle and saved axis limits of a single archived panel."""

    def __init__(self, rgb, frame, first, last, training=False):
        left, top, right, bottom = frame
        r, g, b = rgb[top:bottom + 1, left:right + 1].transpose(2, 0, 1)
        self.ink = {4: np.minimum(b - r, b - g), 8: np.minimum(r - g, g - b),
                    16: g - np.maximum(r, b)}
        pad = (last - first) * .05  # Matplotlib's original five percent x margins
        self.x, dx = np.linspace(first - pad, last + pad, right - left + 1, retstep=True)
        self.y, dy = np.linspace(105, -5, bottom - top + 1, retstep=True)
        self.extent = (self.x[0] - dx / 2, self.x[-1] + dx / 2,
                       self.y[-1] + dy / 2, self.y[0] - dy / 2)
        self.training = training
        self.first, self.last = first, last

    def reading(self, keys, length):
        """Center of one isolated stroke. A thick/ambiguous match must be reviewed."""
        column = self.ink[keys][:, np.argmin(abs(self.x - length))]
        mask = column > 18
        if length == 16:  # All sampled curves at 16 exceed 40%; exclude lower-left legend.
            mask &= self.y > 40
        if not mask.any() or np.ptp(self.y[mask]) > 4:
            raise ValueError(f"Ambiguous archived reading at {length} for {keys} keys")
        return np.clip(np.average(self.y[mask], weights=column[mask]), 0, 100)

    def draw_full_keys(self, ax, color, start):
        # M=16 was green and drawn last. Other line colors have no green excess.
        # Its opacity was 0.8 in training plots and 0.9 in length sweeps.
        alpha = np.clip(self.ink[16] / (93 if self.training else 104), 0, 1)
        if self.training:
            # The original legend is below 35% late in training, clear of the trace.
            alpha[(self.x[None, :] > .52 * self.last) & (self.y[:, None] < 35)] = 0
        visible = (self.x >= start) & (self.x <= self.last)
        if np.any(alpha[:, visible].max(axis=0) < .18):
            raise ValueError("Incomplete archived line")
        alpha[:, self.x < start - (self.x[1] - self.x[0])] = 0
        rgba = np.empty((*alpha.shape, 4))
        rgba[:, :, :3] = to_rgb(color)
        rgba[:, :, 3] = alpha
        ax.imshow(rgba, extent=self.extent, origin="upper", interpolation="bilinear",
                  aspect="auto", zorder=3)


def figure():
    fig, ax = plt.subplots(figsize=SIZE)
    fig.subplots_adjust(left=.16, right=.97, bottom=.21, top=.81)
    ax.tick_params(length=0, pad=4, labelsize=10)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=RULE, lw=.7)
    return fig, ax


def key(fig, entries):
    handles = [Line2D([], [], color=color, marker=marker, linestyle="none",
                      markeredgewidth=0, markersize=7, label=label) for label, color, marker in entries]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(.52, .99),
               frameon=False, ncol=len(entries), columnspacing=1.15, handlelength=.8,
               handletextpad=.38, fontsize=10)


def accuracy_axis(ax):
    ax.set_ylim(-3, 105)
    ax.set_yticks([0, 25, 50, 75, 100])


def arrow(ax, points, color, width):
    path = DrawingPath(points, [DrawingPath.MOVETO, DrawingPath.CURVE4,
                                DrawingPath.CURVE4, DrawingPath.CURVE4])
    ax.add_patch(FancyArrowPatch(path=path, arrowstyle="-|>", color=color,
                                 lw=width, mutation_scale=8, zorder=1))


def task_figure(size=SIZE):
    fig, ax = plt.subplots(figsize=size)
    fig.subplots_adjust(left=.035, right=.965, bottom=.04, top=.96)
    ax.set(xlim=(-.56, 7.56), ylim=(-2.03, 1.94))
    ax.set_axis_off()
    arrow(ax, [(7, .30), (6.9, 1.80), (.1, 1.80), (0, .30)], HYBRID, 1.55)
    arrow(ax, [(.15, -.31), (.15, -.89), (1.04, -.89), (1.0, -.31)], ROTARY, 1.55)
    arrow(ax, [(-.13, -.31), (-.10, -1.98), (4.99, -1.98), (5, -.31)], PURPLE, 1.55)
    ax.text(3.5, 1.68, "Find the earlier A", fontsize=12, color=HYBRID, ha="center")
    ax.text(1.23, -.99, "1 step", fontsize=11, color=ROTARY, ha="center")
    ax.text(3.10, -1.80, "5 steps", fontsize=11, color=PURPLE, ha="center")
    tokens = "ABDEFCGA"
    for i, token in enumerate(tokens):
        face, edge, ink = "#f4f6f6", "#e0e6e6", MUTED
        if i == 0:
            face, edge, ink = "#dcf0e9", HYBRID, HYBRID
        elif i == 7:
            face, edge, ink = HYBRID, HYBRID, "white"
        elif i == 1:
            face, edge, ink = "#f7e5de", "#d79d8e", ROTARY
        elif i == 5:
            face, edge, ink = "#eee8f2", "#baabc6", PURPLE
        ax.add_patch(FancyBboxPatch((i - .40, -.245), .80, .49,
                                    boxstyle="round,pad=0.015,rounding_size=.07",
                                    lw=.85, fc=face, ec=edge))
        ax.text(i, 0, token, va="center", ha="center", fontfamily="DejaVu Serif", fontsize=17, color=ink)
    return fig


def learning_figure(histories):
    fig, ax = figure()
    fig.subplots_adjust(left=.27, right=.94, top=.85)
    ax.set(xlim=(-4, 185), ylim=(-.65, 4.65), xlabel="Completed epochs to 90% validation accuracy")
    ax.set_xticks([0, 50, 100, 150])
    ax.set_yticks(range(4, -1, -1), [name for _, name in MODELS])
    ax.grid(False)
    ax.vlines([0, 50, 100, 150], .48, 4.52, colors=RULE, lw=.65, zorder=0)
    key(fig, [("Gap 1", ROTARY, "o"), ("Gap 5", HYBRID, "D")])
    for y, (model, _) in zip(range(4, -1, -1), MODELS):
        xs = [next((epoch for epoch, v in histories[model, gap] if v >= .9), None) for gap in (1, 5)]
        if xs[0] is None and xs[1] is None:
            ax.text(4, y, "Below 90% at 250 epochs", fontsize=10, color=MUTED, va="center")
            continue
        ax.plot(xs, [y - .10, y + .10], color="#9faaa9", lw=1.2)
        for x, dy, color, marker in zip(xs, [-.10, .10], [ROTARY, HYBRID], ["o", "D"]):
            ax.scatter(x, y + dy, s=36, color=color, marker=marker, zorder=3)
    return fig


def fixed_scores(cells):
    scores = {}
    for gap, index in ((1, 13), (5, 21)):
        log = "".join("".join(o.get("text", [])) for o in cells[index]["outputs"])
        for model, length, rate in re.findall(r"Model (\w+) @ T=(\d+) accuracy = ([0-9.]+)", log):
            count = round(float(rate) * 990)
            if f"{count / 990:.4f}" != rate:
                raise ValueError("Score is inconsistent with 990 examples")
            scores[model.removesuffix("5"), gap, int(length)] = 100 * count / 990
    return scores


def positions_figure(scores):
    fig, ax = plt.subplots(figsize=SIZE)
    fig.subplots_adjust(left=.012, right=.988, bottom=.035, top=.94)
    ax.set(xlim=(0, 8.30), ylim=(-.65, 6.30))
    ax.set_axis_off()
    columns = [(1, 31), (1, 32), (1, 33), (1, 96), (5, 32), (5, 96)]
    centers = [2.55, 3.55, 4.55, 5.55, 6.85, 7.85]
    for x, lab in [(4.05, "Gap of 1"), (7.35, "Gap of 5")]:
        ax.text(x, 5.9, lab, ha="center", fontsize=12, fontweight="bold")
    ax.hlines([5.55, 5.55], [2.1, 6.4], [6.0, 8.29], colors=RULE, lw=1)
    ax.text(.08, 5.02, "Length", color=MUTED, fontsize=10)
    for x, (_, length) in zip(centers, columns):
        ax.text(x, 5.02, str(length), ha="center", fontsize=10, color=INK if length == 32 else MUTED)
    cmap = LinearSegmentedColormap.from_list("recall", ["#f2f6f4", "#b6d7cd", "#5d988c", "#195c55"])
    for y, (model, label) in zip(range(4, -1, -1), MODELS):
        ax.text(.08, y, label, va="center", fontsize=10.5)
        for x, (gap, length) in zip(centers, columns):
            v = scores[model, gap, length]
            face = cmap(v / 100)
            ax.add_patch(Rectangle((x - .47, y - .44), .94, .88, facecolor=face, linewidth=0))
            ax.text(x, y, f"{v:.1f}".removesuffix(".0"), ha="center", va="center",
                    color="white" if v > 68 else INK, fontsize=10)
    return fig


def curve_figure(series, training=False, delay=False):
    fig, ax = figure()
    # The original long-delay legend obscures several samples below length 25.
    start = 1 if training else 25 if delay else 16
    ax.set_xlim((start, 1060 if training else 97.5))
    accuracy_axis(ax)
    ax.set_ylabel("Validation accuracy (%)" if training else "Recall accuracy (%)")
    ax.set_xlabel("Completed epochs" if training else "Sequence length (tokens)")
    if training:
        ax.set_xticks([1, 250, 500, 750, 1000], ["1", "250", "500", "750", "1,000"])
    else:
        ax.set_xticks([start, 32, 48, 64, 80, 96])
        ax.axvline(32, color="#7c8b93", ls=(0, (2, 3)), lw=1)
        for tick in ax.get_xticklabels():
            if tick.get_text() == "32":
                tick.set_weight("bold")
                tick.set_color(INK)
    if delay:
        ax.axhline(6.25, color=MUTED, ls=(0, (4, 3)), lw=1)
    key(fig, [(label, color, marker) for label, color, marker, _ in series])
    for _, color, marker, panel in series:
        panel.draw_full_keys(ax, color, start)
        ax.scatter(panel.last, panel.reading(16, panel.last), s=28, marker=marker,
                   facecolor=color, edgecolor="white", linewidth=.6, zorder=4)
    return fig


def diversity_figure(lengths):
    fig, ax = figure()
    fig.subplots_adjust(left=.16, right=.94, top=.80)
    ax.set(xlim=(59, 106), ylim=(-1, 108), xlabel="Accuracy at 16 tokens (%)",
           ylabel="Accuracy at 96 tokens (%)")
    ax.set_xticks([60, 70, 80, 90, 100])
    ax.set_yticks([0, 25, 50, 75, 100])
    key(fig, ARCHITECTURES)
    labels = {"Mamba": [(1, 8), (4, 6), (-9, -13)],
              "RoPE": [(-1, -13), (7, 4), (1, -13)]}
    for name, color, marker in ARCHITECTURES:
        panel = lengths[name]
        if name == "Hybrid":
            # At ceiling the three original strokes overlap. Place one representative point.
            x, y = panel.reading(16, 16), panel.reading(16, 96)
            ax.scatter(x, y, marker=marker, s=40, color=color, zorder=3)
            ax.annotate("4, 8, 16", (x, y), xytext=(-7, -11), textcoords="offset points",
                        ha="right", va="center", color=color, fontsize=10)
            continue
        pts = [(panel.reading(m, 16), panel.reading(m, 96)) for m in (4, 8, 16)]
        xx, yy = zip(*pts)
        ax.plot(xx, yy, lw=1.3, color=color, alpha=.72)
        ax.scatter(xx, yy, color=color, s=37, marker=marker, zorder=3)
        for count, point, offset in zip((4, 8, 16), pts, labels[name]):
            ax.annotate(str(count), point, xytext=offset, textcoords="offset points",
                        ha="center", fontsize=10, color=color)
    return fig


def width_figure(narrow, wide):
    fig, ax = figure()
    fig.subplots_adjust(left=.18, right=.96)
    ax.set(xlim=(-40, 27), ylim=(-.52, 2.52), xlabel="Change in accuracy (percentage points)")
    ax.set_xticks([-30, -15, 0, 15], ["−30", "−15", "0", "+15"])
    ax.set_yticks([2, 1, 0], ["4 keys", "8 keys", "16 keys"])
    ax.grid(False)
    ax.axvline(0, color=MUTED, lw=.9)
    ax.hlines([.5, 1.5], -40, 27, colors=RULE, lw=.65)
    key(fig, [("16 tokens", PURPLE, "s"), ("96 tokens", MAMBA, "s")])
    for length, offset, color in [(16, .14, PURPLE), (96, -.14, MAMBA)]:
        for y, count in zip([2, 1, 0], (4, 8, 16)):
            gain = wide.reading(count, length) - narrow.reading(count, length)
            ax.barh(y + offset, gain, height=.20, color=color, zorder=3)
            direction = 1 if gain > 0 else -1
            label = f"{gain:+.0f}".replace("-", "−")
            ax.annotate(label, (gain, y + offset), xytext=(4 * direction, 0),
                        textcoords="offset points", ha="left" if gain > 0 else "right",
                        va="center", fontsize=10, color=color)
    return fig


def export(fig, stem, directory, print_dir, cover=False):
    if print_dir:
        fig.savefig(print_dir / (stem + ".svg"))
        fig.savefig(print_dir / (stem + ".pdf"), dpi=300)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=600)
    plt.close(fig)
    with Image.open(buf) as source:
        im = source.convert("RGB")
        for w in ((480, 1080) if cover else (560, 1120)):
            h = round(w * im.height / im.width)
            resized = im.resize((w, h), Image.Resampling.LANCZOS)
            resized.save(directory / f"{stem}-{w}.webp", lossless=True)
            if cover and w == 1080:
                resized.save(directory / f"{stem}.png", optimize=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--print-dir", type=Path)
    parser.add_argument("--history", type=Path, default=Path(__file__).with_name("training.csv"))
    args = parser.parse_args()
    directory = args.out / "associative-recall"
    directory.mkdir(exist_ok=True, parents=True)
    if args.print_dir:
        args.print_dir.mkdir(exist_ok=True, parents=True)
    fixed, variable = [json.loads(verified(args.archive / name))["cells"]
                       for name in ("AR_I.ipynb", "AR_II.ipynb")]
    histories = {}
    for row in csv.DictReader(verified(args.history).decode().splitlines()):
        histories.setdefault((row["model"], int(row["offset"])), []).append(
            (int(row["epoch"]), float(row["validation_accuracy"])))
    length_png = notebook_png(variable[12])
    training_png = notebook_png(variable[11])
    # Black axis spines in the unresized notebook PNGs. Original horizontal
    # limits follow the plotted domain. Training epochs are displayed one-based.
    lengths = {name: RasterPanel(length_png, (left, 132, right, 570), 4, 96)
               for name, left, right in [("RoPE", 75, 712), ("Mamba", 780, 1417), ("Hybrid", 1486, 2123)]}
    training = {name: RasterPanel(training_png, (left, 39, right, 520), 1, end, training=True)
                for name, left, right, end in [("Mamba", 76, 708, 1030),
                                               ("RoPE", 790, 1422, 400), ("Hybrid", 1504, 2136, 300)]}
    wide = RasterPanel(notebook_png(variable[15]), (76, 39, 925, 640), 4, 96)
    delayed = RasterPanel(notebook_png(variable[18]), (76, 39, 922, 640), 11, 96)
    figures = {
        "task": task_figure(),
        "learning": learning_figure(histories),
        "positions": positions_figure(fixed_scores(fixed)),
        "variable-training": curve_figure([(*a, training[a[0]]) for a in ARCHITECTURES], training=True),
        "keys": diversity_figure(lengths),
        "hybrid": curve_figure([(*a, lengths[a[0]]) for a in ARCHITECTURES]),
        "width": width_figure(lengths["Mamba"], wide),
        "delay": curve_figure([("Gap 1", MAMBA, "o", wide), ("Gap 10", PURPLE, "D", delayed)], delay=True),
    }
    for stem, fig in figures.items():
        export(fig, stem, directory, args.print_dir)
    export(task_figure((4.8, 8 / 3)), "recall-study-cover", args.out, args.print_dir, cover=True)


if __name__ == "__main__":
    main()
