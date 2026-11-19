# Security policy

Poof's whole job is not leaking private data, so reports about leaks are welcome.

## What counts
- A photo that still carries **location, date, camera/device info or other metadata** after Poof processed it.
- Anything that makes a Poof shortcut send data somewhere (it should not use the network at all).
- A signed shortcut file in a release that doesn't match the source in `tools/`.

## How to report
- **Private (preferred for anything that could harm users):** use **Security → Report a vulnerability** on this repository.
- **Ordinary leaks you reproduced on your own test photo:** the public [Metadata leak form](../../issues/new?template=leak.yml) is fine. Please don't attach photos that show your real location.

## What to include
Device and iOS version, which shortcut, the photo type (JPEG/HEIC/PNG, edited, screenshot), and how you checked it (for example Poof-Peek or the Photos info panel).

## Supported versions
Only the latest release is supported. Poof is pre-1.0.

We'll acknowledge reports as soon as we can. This is a volunteer project, so we can't promise a fixed response time.
