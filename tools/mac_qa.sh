#!/bin/bash
# Ring 2: run the REAL shortcut on macOS against leaky fixtures, then verify with the oracle.
# Prereq: `open build/"Poof & Share.shortcut"` and click Add in Shortcuts once.
set -u
cd "$(dirname "$0")/.."
python3 tools/make_fixtures.py >/dev/null
mkdir -p out; rc=0
if ! shortcuts list | grep -qx "Poof & Share"; then echo "Import 'Poof & Share' first (open build/...)"; exit 2; fi
for f in leaky.jpg leaky_rotated.jpg leaky.png; do
  rm -f "out/$f"
  shortcuts run "Poof & Share" --input-path "fixtures/$f" --output-path "out/$f" 2>&1 | tail -1
  [ -f "out/$f" ] || { echo "NO OUTPUT for $f (Share action may not emit file; see QA notes)"; rc=1; continue; }
  python3 tools/verify_clean.py "out/$f" || rc=1
  python3 - "$f" <<'PY'
import sys; from PIL import Image
a=Image.open(f"fixtures/{sys.argv[1]}"); b=Image.open(f"out/{sys.argv[1]}")
print("  size", a.size, "->", b.size, "| format", a.format, "->", b.format)
PY
done
exit $rc
