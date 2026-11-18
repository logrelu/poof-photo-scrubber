#!/usr/bin/env python3
"""Defines the Poof shortcut bundle, writes build/*.shortcut and signs them."""
from __future__ import annotations
import subprocess, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from shortcutlib import Shortcut, SHORTCUT_INPUT, as_input, text_with

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"


def scrub(sc: Shortcut, source):
    """THE engine: Convert Image, keep format, Preserve Metadata OFF."""
    return sc.add("image.convert", {
        "WFInput": as_input(source),
        "WFImageFormat": "Match Input",
        "WFImagePreserveMetadata": False,
    }, name="Poofed Images")


def poof_and_share() -> Shortcut:
    sc = Shortcut("Poof", share_sheet=True)
    clean = scrub(sc, SHORTCUT_INPUT)
    sc.add("share", {"WFInput": clean.token()})
    return sc


def poof_latest() -> Shortcut:
    sc = Shortcut("Poof-Latest", glyph="bolt")
    latest = sc.add("getlatestphotos", {"WFGetLatestPhotoCount": 1}, "Latest Photos")
    clean = scrub(sc, latest)
    sc.add("setclipboard", {"WFInput": clean.token()})
    sc.add("notification", {
        "WFNotificationActionTitle": "Poof! 🫧",
        "WFNotificationActionBody": "Where & when are gone. Clean photo is on your clipboard - just paste.",
    })
    return sc


def poof_pick() -> Shortcut:
    sc = Shortcut("Poof-Pick", glyph="photo")
    picked = sc.add("selectphoto", {"WFSelectMultiplePhotos": True}, "Photos")
    clean = scrub(sc, picked)
    sc.add("setclipboard", {"WFInput": clean.token()})
    sc.add("share", {"WFInput": clean.token()})
    return sc


def poof_peek() -> Shortcut:
    sc = Shortcut("Poof-Peek", glyph="eye", share_sheet=True)
    when = sc.add("properties.images", {"WFInput": SHORTCUT_INPUT,
                  "WFContentItemPropertyName": "Date Taken"}, "Date Taken")
    where = sc.add("properties.images", {"WFInput": SHORTCUT_INPUT,
                   "WFContentItemPropertyName": "Location"}, "Location")
    cam = sc.add("properties.images", {"WFInput": SHORTCUT_INPUT,
                 "WFContentItemPropertyName": "Camera Model"}, "Camera Model")
    sc.add("alert", {
        "WFAlertActionTitle": "This photo was telling on you",
        "WFAlertActionMessage": text_with("📍 ", where, "\n🕒 ", when, "\n📱 ", cam),
        "WFAlertActionCancelButtonShown": False,
    })
    return sc


ALL = [poof_and_share, poof_latest, poof_pick, poof_peek]


def build(sign: bool = True) -> list[pathlib.Path]:
    BUILD.mkdir(exist_ok=True)
    out = []
    for fn in ALL:
        sc = fn()
        raw = BUILD / f"{sc.name}.unsigned.shortcut"
        sc.write(str(raw))
        if sign:
            dst = BUILD / f"{sc.name}.shortcut"
            r = subprocess.run(["shortcuts", "sign", "-m", "anyone", "-i", str(raw), "-o", str(dst)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                sys.exit(f"sign failed for {sc.name}: {r.stderr}")
            raw.unlink()
            out.append(dst)
        else:
            out.append(raw)
    return out


if __name__ == "__main__":
    for p in build(sign="--no-sign" not in sys.argv):
        print("built", p.name, p.stat().st_size, "bytes")
