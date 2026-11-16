#!/usr/bin/env python3
"""QA oracle: reports any metadata that tells where/when/what-device. Exit 0 = CLEAN."""
from __future__ import annotations
import sys
from PIL import Image

EXIF_LEAKS = {271: "Make", 272: "Model", 305: "Software", 306: "DateTime", 315: "Artist",
              33432: "Copyright", 0x9003: "DateTimeOriginal", 0x9004: "DateTimeDigitized",
              0x9010: "OffsetTime", 0xA431: "BodySerialNumber", 0xA434: "LensModel",
              0xA433: "LensMake", 0x9291: "SubSecTimeOriginal"}


def leaks(path: str) -> list[str]:
    found: list[str] = []
    im = Image.open(path)
    ex = im.getexif()
    if ex.get_ifd(0x8825):
        found.append("GPS block present")
    sub = ex.get_ifd(0x8769)
    for tag, name in EXIF_LEAKS.items():
        if tag in ex or tag in sub:
            found.append(f"EXIF {name}")
    # XMP / IPTC / PNG text chunks / comments
    for key in im.info:
        k = str(key).lower()
        if k in ("xmp", "xml:com.adobe.xmp", "photoshop", "comment") or k.startswith("exif"):
            if k.startswith("exif") and not ex:
                continue
            found.append(f"embedded {key}")
    for key in im.info:  # PNG tEXt/iTXt style chunks
        if any(w in str(key).lower() for w in ("creation", "date", "time", "location", "gps", "latitude")):
            found.append(f"text chunk {key}")
    raw = open(path, "rb").read()
    for needle, label in ((b"<x:xmpmeta", "raw XMP packet"), (b"GPSLatitude", "raw GPSLatitude"),
                          (b"DateTimeOriginal", "raw DateTimeOriginal")):
        if needle in raw:
            found.append(label)
    return sorted(set(found))


def main(argv: list[str]) -> int:
    rc = 0
    for p in argv:
        l = leaks(p)
        if l:
            print(f"LEAKY  {p}: " + ", ".join(l)); rc = 1
        else:
            print(f"CLEAN  {p}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
