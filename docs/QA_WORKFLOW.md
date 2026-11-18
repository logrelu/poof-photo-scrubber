# QA Workflow

Three rings, cheap to expensive. Nothing merges unless Ring 1 is green; nothing ships unless Ring 3 passes on a device.

## Ring 1 - Automated, local (every commit): `make test`
1. **Builder tests**: generated plist round-trips, every action has a UUID, variable references resolve, share-sheet input types set to images.
2. **Verifier tests**: `verify_clean.py` flags a fixture with GPS/dates/device (must FAIL it) and passes a stripped one (must PASS). The oracle must be proven able to catch leaks, or its "pass" means nothing.
3. **Signing check**: `shortcuts sign` succeeds; output starts with `AEA1` header.
4. **Fixture matrix**: JPEG (GPS+dates+make/model), JPEG rotated (orientation 6), PNG with text chunks, tiny & large dims.

## Ring 2 - macOS runtime (before release): `make mac-qa`
macOS 26 runs the *same Shortcuts engine* incl. Convert Image.
1. Import signed shortcut (`open build/Poof*.shortcut`, click Add).
2. `shortcuts run "Poof" --input-path fixtures/leaky.jpg --output-path out/clean.jpg`
3. `verify_clean.py out/clean.jpg` -> must print `CLEAN`.
4. Diff pixel dimensions & SSIM vs source.

## Ring 3 - Real device matrix (release gate)
Device: iPhone on current iOS 26.x. Use a fresh photo taken at home with Location Services on.
| # | Scenario | Pass if |
|---|---|---|
| D1 | Photos > Share > Poof > Messages (to self) | Received image: Info shows no location; save to Files, run Poof-Peek -> nothing leaks |
| D2 | Same, 5 photos mixed HEIC/JPEG/screenshot | All 5 clean, order kept |
| D3 | WhatsApp send from share sheet | Clean (verify via saving received media) |
| D4 | ChatGPT / Claude / Gemini via share sheet | Upload accepted, no EXIF on downloaded copy where retrievable |
| D5 | Poof-Latest via Action Button | Clipboard has image; paste into Notes; Peek clean |
| D6 | App-open automation | Opening app runs it without a prompt |
| D7 | Original photo in Photos | Still has location on the map; no duplicates in library |
| D8 | Live Photo, Portrait (depth), burst | Doesn't crash; outputs a still; documented behavior |
| D9 | Airplane mode | Works offline |
| D10 | 20 photos | Completes < 40 s, no memory kill |
Record results in `docs/qa-results/YYYY-MM-DD.md` (template included).

## Bug triage
- Any metadata leak = **P0** (blocks release).
- Share-sheet ordering or wording = P2.
