# Research: how do we scrub a photo *only at share time*?

## The problem
Photos carry EXIF/GPS/TIFF/IPTC metadata: where (GPS), when (DateTimeOriginal, etc.), device model,
sometimes more (lens, software, depth/portrait extras, HEIC auxiliary data, Live Photo pairing IDs).
We want that gone from the **outgoing copy** while the **library original stays intact**
(location memories, Places album, "On this day" all keep working).

## What iOS actually allows (the hard constraints)
| Constraint | Consequence |
|---|---|
| No API/hook to intercept *another app's* share or file upload | We can't silently auto-scrub "every share". Something must be *in the path* the user takes. |
| Share sheet is system UI; 3rd parties add **Action extensions / Shortcuts** rows only | We can show up *in* the share sheet, not replace it. |
| Shortcuts **"Show in Share Sheet"** shortcuts appear in the Share Sheet's action list for images | Zero-install path that is genuinely "at share time". |
| Convert Image action w/ **Preserve Metadata OFF** drops EXIF/GPS/dates | The scrub engine is built in; no app needed. |
| Built-in Share Sheet > Options > **Location** toggle | Removes GPS only. Keeps timestamp + camera. Not remembered between shares. |
| App-open personal automations (iOS 17+) can run without a confirm prompt | Enables a "prep clipboard when I open ChatGPT/WhatsApp" flow. |
| Action Button, Back Tap, Control Center, Lock Screen controls can run a shortcut | One-gesture scrub of newest photo. |
| Shortcut files must be **signed** to import (iOS 15+) | We sign with `shortcuts sign -m anyone` on macOS. |
| Automations can't be shipped as importable files | Ship as a 6-tap guided recipe. |

## Candidate solutions
| # | Approach | At share time? | No extra app? | Friction | Verdict |
|---|---|---|---|---|---|
| A | Built-in Share Options > Location off | yes | yes | 2 taps every time, GPS only | Baseline/fallback; **insufficient** (time remains) |
| B | **Share-sheet Shortcut** ("Poof") | yes | yes (Shortcuts is built in) | 1 extra tap, then the normal share opens with a clean copy | **Primary** |
| C | Native app w/ Share/Action Extension | yes | **no** (it's an app) | 1 tap, nicer UI, batch, previews | Rejected by brief; kept as Phase-3 option |
| D | App-open automation -> clean newest photo to clipboard | near | yes | 0 taps then paste | **Companion** for AI chatbots |
| E | Action Button / Back Tap -> clean newest photo | near | yes | 1 gesture | **Companion** |
| F | Turn off camera geotag (Settings>Privacy>Location>Camera) | no | yes | none | Loses data forever. Opposite of goal |
| G | Photos Library "clean copy" in a hidden album | no | yes | pollutes library | Rejected (brief: *not in your gallery*) |
| H | Mac `exiftool` pipeline | n/a | n/a | n/a | Out of scope; used only for QA |

## Decision
**Ship B + D + E as a bundle of signed `.shortcut` files, no app.**
Honest caveat, stated up front in the UX: iOS cannot force-scrub shares started from *other apps'
own pickers* (e.g. WhatsApp's in-app gallery button). WhatsApp re-encodes media and strips most EXIF
itself, but it's not a guarantee we can promise; Messages sends metadata intact; AI chatbots vary.
For in-app pickers, the clipboard flow (D/E) is the answer: paste the clean photo instead of picking.

## Open questions to verify on a real device (tracked in QA_WORKFLOW.md)
1. Does Convert Image (Match Input, Preserve Metadata off) fully strip *HEIC* dates & GPS, or only JPEG?
2. Does `Match Input` preserve HEIC or force JPEG? (Forum reports say screenshots flip PNG->JPEG.)
3. Does the Live Photo input degrade to a still? (Acceptable; documented.)
4. Exact label & ordering of Shortcut rows in share sheet on iOS 26.
5. Does Convert Image drop the file-system creation date on the output? (We also set a neutral name.)

## Sources
- Share Sheet Options > Location toggle: igeeksblog, Apple Personal Safety guide (support.apple.com/guide/personal-safety/ips0d7a5df82)
- Convert Image / Preserve Metadata: matthewcassinelli.com/actions/convert-image, privacyguides.org "Integrating metadata removal", talk.macpowerusers.com thread
- Privacy Guides forum: "EXIF removal tools iOS, no apps required"
