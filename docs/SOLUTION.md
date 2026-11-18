# Solution: **Poof!** 🫧 — photos that forget where and when

> Share a photo. Poof. Where and when are gone. Your library still remembers.

## The bundle
| Shortcut | Trigger | What it does |
|---|---|---|
| **Poof** | Share sheet (images) | Scrub each selected image -> open share sheet again with clean copies. Original untouched. |
| **Poof-Latest** | Action Button / Back Tap / Control Center / Siri "Poof" | Scrub newest photo (or latest N) -> clipboard. Paste into any chatbot/chat. |
| **Poof-Pick** | Home Screen icon / widget | Pick photos -> scrub -> copy/share. For in-app uploads where the share sheet isn't reachable. |
| **Poof-Peek** | Share sheet or Siri | Shows what a photo *is leaking* (location, date, device) in a friendly alert. Educational + QA. |
| Automation recipe | Open WhatsApp/ChatGPT/Claude/Gemini | Auto-run *Poof-Latest* so the clipboard already holds a clean photo. |

## Flow (Poof)
```
Share sheet -> tap "Poof"
   -> [Repeat each image] Convert Image (Match Input, Preserve Metadata = OFF)
   -> Rename "poof-<n>" (kills filename-embedded dates like IMG_20261116)
   -> Share (clean copies) -> user picks WhatsApp / Messages / ChatGPT as usual
```
Zero files written to Photos. Nothing saved. Temp files live in Shortcuts' sandbox only.

## Architecture of this repo
- `tools/shortcutlib.py` : tiny typed builder for the `.shortcut` plist (WFWorkflow) format
- `tools/build_shortcuts.py` : defines each shortcut, writes `build/*.shortcut`, signs via `shortcuts sign`
- `tools/make_fixtures.py` : creates test JPEG/PNG with GPS + dates + device tags
- `tools/verify_clean.py` : scans an image for any leaking metadata (the QA oracle)
- `tests/` : unit tests for builder & verifier (runs in CI/local, no phone)
- `site/index.html` : playful install page w/ QR + 3-step setup
- `docs/` : research, success criteria, QA, voice

## Why not an app?
The brief says no extra app. We also found nothing an app could do at share time that a
Shortcut can't, except nicer UI/batching/preview. It's recorded as Phase 3 in ROADMAP.md.

## Risks
| Risk | Mitigation |
|---|---|
| Apple changes action parameter keys | Builder isolated in one module; QA step runs actual `shortcuts run` on macOS |
| User forgets to use Poof | Action Button + automation recipes; honest "what Poof can't catch" screen |
| HEIC dates survive | Force JPEG output fallback toggle; verified in QA |
| Unsigned file won't import | Build pipeline signs; CI check asserts signature header |
