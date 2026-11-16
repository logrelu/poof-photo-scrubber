#!/usr/bin/env python3
"""Builds deliberately leaky test images in fixtures/."""
import pathlib
from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngInfo

OUT = pathlib.Path(__file__).resolve().parent.parent / "fixtures"


def art(w, h):
    im = Image.new("RGB", (w, h), (185, 167, 255))
    d = ImageDraw.Draw(im)
    d.ellipse((w//4, h//4, 3*w//4, 3*h//4), fill=(140, 245, 208))
    d.text((12, 12), "poof test", fill=(27, 21, 48))
    return im


def leaky_exif(orientation=1):
    from PIL import Image as I
    ex = I.Exif()
    ex[271], ex[272], ex[305] = "Apple", "iPhone 16 Pro", "26.1"
    ex[306] = "2026:11:16 15:12:00"
    ex[274] = orientation
    ex[0x8769] = {0x9003: "2026:11:16 15:12:00", 0x9004: "2026:11:16 15:12:00",
                  0xA434: "iPhone 16 Pro back camera"}
    ex[0x8825] = {1: "N", 2: (37.0, 46.0, 29.7), 3: "W", 4: (122.0, 25.0, 9.8)}
    return ex


def main():
    OUT.mkdir(exist_ok=True)
    art(1200, 800).save(OUT / "leaky.jpg", exif=leaky_exif(), quality=92)
    art(800, 1200).save(OUT / "leaky_rotated.jpg", exif=leaky_exif(6), quality=92)
    art(64, 64).save(OUT / "leaky_tiny.jpg", exif=leaky_exif())
    pi = PngInfo(); pi.add_text("Creation Time", "2026-11-16"); pi.add_text("Location", "37.77,-122.41")
    art(600, 600).save(OUT / "leaky.png", pnginfo=pi)
    art(1200, 800).save(OUT / "clean.jpg", quality=92)
    print("fixtures:", sorted(p.name for p in OUT.iterdir()))


if __name__ == "__main__":
    main()
