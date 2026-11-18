# Phone test (10 minutes)

## Install
1. On the Mac: `make build`, then AirDrop **`build/Poof.shortcut`** to your iPhone (Poof-Peek too, it's the leak viewer).
2. Tap the file, then **Add Shortcut**. If the share-sheet row doesn't show later, restart the phone once.
3. Photos > Share > scroll Actions > **Edit Actions** > pin **Poof** and **Poof-Peek**.

## Tests (write results in docs/qa-results/YYYY-MM-DD.md)
| # | Do this | Pass if |
|---|---|---|
| P1 | Take a photo outdoors (Location Services on). Share > **Poof-Peek** | Shows a place + time + model (proves the photo *is* leaky; if empty, take another) |
| P2 | Share same photo > **Poof** > Messages to yourself | Send succeeds |
| P3 | Long-press the *received* image > Save to Files. Share it > **Poof-Peek** | Place and date are empty |
| P4 | Receive on another device / tap (i) on received photo | No map, no date |
| P5 | Open original in Photos | Still has map location (original untouched) |
| P6 | Photos library count before/after | No new photos added |
| P7 | Select 5 photos mixed (HEIC, screenshot) > Poof | All 5 arrive, all clean |
| P8 | WhatsApp / ChatGPT / Claude via share sheet | Send/upload works |

**Any leak = P0.** Screenshot Poof-Peek results and send them to me; I will adjust the engine.

## Independent verification (do not rely on Poof-Peek alone)
Poof-Peek uses the same Shortcuts engine, so it can share blind spots with Poof. For at least P3, also:
1. AirDrop the *received* clean file to a Mac (or save to Files and open on a Mac).
2. Run `python3 tools/verify_clean.py <file>` (the independent checker) and/or Preview > Tools > Show Inspector > GPS / Exif tabs.
3. Pass only if both say nothing leaks.

## Extra cases (from external review)
| # | Case | Pass if |
|---|---|---|
| P9 | JPEG and **HEIC** from a recent iPhone, with GPS | Clean, both formats |
| P10 | **Edited** photo (crop / filter applied) | Clean; no edit-history leak |
| P11 | Photo with a **caption / keywords** set in Photos | Caption and keywords absent in the output |
| P12 | Screenshot | Clean; still looks right |
| P13 | Send via Messages, WhatsApp, Instagram, AirDrop; retrieve the received file | Metadata not **re-introduced** by the receiving path |
| P14 | Paste into ChatGPT and Claude (Poof-Latest flow) | Upload works; downloaded copy clean where retrievable |
| P15 | Image quality + orientation vs original | Visually identical, upright |
| P16 | Airplane mode | Works offline |
