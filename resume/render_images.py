#!/usr/bin/env python3
"""Render resume/Resume.pdf pages to optimised JPEGs for the /resume/ web viewer.

The viewer at resume/index.html displays these images so the resume renders on
every device (desktop and mobile), while the round button downloads the real PDF.
Run this after rebuilding Resume.pdf; the resume CI workflow does it automatically.

Dependencies: PyMuPDF (fitz) and Pillow.
"""
import os

import fitz  # PyMuPDF
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "Resume.pdf")
OUT = os.path.join(HERE, "assets")
WIDTH = 1000
QUALITY = 80


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    doc = fitz.open(PDF)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        tmp = os.path.join(OUT, f"_t{i + 1}.png")
        pix.save(tmp)
        im = Image.open(tmp).convert("RGB")
        w, h = im.size
        im = im.resize((WIDTH, round(h * WIDTH / w)), Image.LANCZOS)
        im.save(
            os.path.join(OUT, f"resume-p{i + 1}.jpg"),
            "JPEG",
            quality=QUALITY,
            optimize=True,
            progressive=True,
        )
        os.remove(tmp)
    print(f"rendered {doc.page_count} page(s) to {OUT}")


if __name__ == "__main__":
    main()
