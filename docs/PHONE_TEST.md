# Phone test (10 minutes)

## Install
1. On the Mac: `make build`, then AirDrop **`build/Poof & Share.shortcut`** to your iPhone (Poof Peek too, it's the leak viewer).
2. Tap the file, then **Add Shortcut**. If the share-sheet row doesn't show later, restart the phone once.
3. Photos > Share > scroll Actions > **Edit Actions** > pin **Poof & Share** and **Poof Peek**.

## Tests (write results in docs/qa-results/YYYY-MM-DD.md)
| # | Do this | Pass if |
|---|---|---|
| P1 | Take a photo outdoors (Location Services on). Share > **Poof Peek** | Shows a place + time + model (proves the photo *is* leaky; if empty, take another) |
| P2 | Share same photo > **Poof & Share** > Messages to yourself | Send succeeds |
| P3 | Long-press the *received* image > Save to Files. Share it > **Poof Peek** | Place and date are empty |
| P4 | Receive on another device / tap (i) on received photo | No map, no date |
| P5 | Open original in Photos | Still has map location (original untouched) |
| P6 | Photos library count before/after | No new photos added |
| P7 | Select 5 photos mixed (HEIC, screenshot) > Poof & Share | All 5 arrive, all clean |
| P8 | WhatsApp / ChatGPT / Claude via share sheet | Send/upload works |

**Any leak = P0.** Screenshot Poof Peek results and send them to me; I will adjust the engine.
