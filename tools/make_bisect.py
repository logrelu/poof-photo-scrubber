#!/usr/bin/env python3
"""Builds small signed variants + site/test/index.html to bisect 'invalid shortcut' on a real phone."""
import pathlib, subprocess, sys, urllib.parse as u
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from shortcutlib import Shortcut
import build_shortcuts as bs

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "test"
OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://logrelu.github.io/poof-photo-scrubber/test/"


def v1():
    s = Shortcut("T1 comment only"); s.add("comment", {"WFCommentActionText": "hi"}); return s


def v2():
    s = Shortcut("T2 share-sheet flag", share_sheet=True); s.add("comment", {"WFCommentActionText": "hi"}); return s


def v3():
    s = Shortcut("T3 convert only")
    s.add("image.convert", {"WFImageFormat": "Match Input", "WFImagePreserveMetadata": False}); return s


def v4():
    s = Shortcut("T4 share only"); s.add("share", {}); return s


def v5():
    s = Shortcut("T5 latest to clipboard")
    s.add("getlatestphotos", {"WFGetLatestPhotoCount": 1}); s.add("setclipboard", {}); return s


def v6():
    s = bs.poof_and_share(); s.name = "T6 real Poof and Share"; return s


rows = []
for fn in (v1, v2, v3, v4, v5, v6):
    sc = fn()
    raw = OUT / f"{sc.name}.unsigned.shortcut"
    sc.write(str(raw))
    dst = OUT / f"{sc.name}.shortcut"
    subprocess.run(["shortcuts", "sign", "-m", "anyone", "-i", str(raw), "-o", str(dst)], check=True)
    raw.unlink()
    f = u.quote(sc.name + ".shortcut")
    link = "shortcuts://import-workflow?url=" + u.quote(BASE + f, safe="") + "&name=" + u.quote(sc.name, safe="")
    rows.append(f'<li><b>{sc.name}</b> &nbsp; <a href="{link}">1-tap</a> &nbsp; <a href="{f}">file</a></li>')

(OUT / "index.html").write_text(
    '<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
    '<title>Poof bisect</title><body style="font:18px system-ui;padding:16px;line-height:2">'
    '<h2>Poof bisect</h2><p>Tap each. Note which say "invalid".</p><ol>' + "".join(rows) + "</ol></body>")
print("built", len(rows))
