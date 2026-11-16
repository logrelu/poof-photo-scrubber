# Definition of Success

## Must (ship-blockers)
- [ ] M1. Output copy has **no GPS** tags (any GPS IFD / `kCGImagePropertyGPSDictionary`).
- [ ] M2. Output copy has **no capture date/time** (EXIF DateTimeOriginal/Digitized, TIFF DateTime, XMP/IPTC dates).
- [ ] M3. Output has **no device identifiers** (Make, Model, Software, LensModel, serial/ BodySerialNumber).
- [ ] M4. **Original in Photos is byte-identical**; no new asset appears in the library.
- [ ] M5. Image **looks identical** (orientation correct, no visible downscale beyond Apple's own; SSIM sanity >= 0.99 on fixtures).
- [ ] M6. Works for **JPEG, HEIC, PNG, screenshots**, and **multi-select (up to 20)**.
- [ ] M7. Imports on a clean iPhone via a **signed** file, in <= 3 taps.
- [ ] M8. Works as a share-sheet action to **Messages, WhatsApp, Mail, AirDrop** and to **AI chat apps** (ChatGPT, Claude, Gemini).

## Should
- [ ] S1. Total added time <= 2 s per photo for 12 MP.
- [ ] S2. One extra tap in the share path (target: Poof is in the top row of actions).
- [ ] S3. Clipboard flow gives a clean photo in 0 taps after app-open automation.
- [ ] S4. Orientation preserved even though EXIF Orientation is stripped (pixels baked upright).
- [ ] S5. All copy playful, never scary, never preachy.

## Could
- Video scrub (location + creation date) in a v2 via Encode Media.
- A Peek report: "this photo was leaking: 📍 Cafe, 🕒 Sun 3:12pm, 📱 iPhone 16".

## Won't (explicitly out of scope)
- Intercepting shares inside other apps' private pickers (iOS forbids).
- Scrubbing the Photos library itself.
- Removing *visible* content (faces, street signs). Poof is about metadata.

## North-star metric
"**Zero leaks per 100 shares** when the user follows the 1-tap path," measured by `verify_clean.py` on QA fixtures and a device test matrix.
