"""Prepare the associative-recall plots from the project's original II_2.png.

The pinned source is linked on the project page. Render the interactive studies'
static posters with render_research.mjs.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "research"


def save_image(name, image):
    OUT.mkdir(parents=True, exist_ok=True)
    image = image.convert("RGB")
    for width in (480, 1080):
        size = (width, round(width * image.height / image.width))
        resized = image.resize(size, Image.Resampling.LANCZOS)
        resized.save(OUT / f"{name}-{width}.webp", lossless=True, method=6)
        if width == 1080:
            resized.save(OUT / f"{name}.png", optimize=True)


def recall(source):
    with Image.open(source) as original:
        if original.size != (1838, 496):
            raise ValueError("Expected II_2.png from commit d148ad9 of Analysis-AR-problem")
        save_image("recall-results", original)
        middle_panel = original.crop((625, 0, 1230, 496))
        panel = ImageOps.contain(middle_panel, (1050, 582), Image.Resampling.LANCZOS)
        cover = Image.new("RGB", (1080, 600), "white")
        cover.paste(panel, ((1080-panel.width)//2, (600-panel.height)//2))
        save_image("recall", cover)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("recall_original", type=Path)
    recall(parser.parse_args().recall_original)
