# Contributing to Poof

Thanks for helping. Poof is small on purpose: a few Apple Shortcuts that strip location, date and device info from a photo when you share it.

## The fastest ways to help (no code)
- **Test on your phone** and file a [Device test report](../../issues/new?template=device-test.yml). Different iOS versions and photo types are the most useful thing we're missing.
- **Report a leak** with the [Metadata leak form](../../issues/new?template=leak.yml). A leak is treated as top priority.
- **Report an install problem** with the [Install form](../../issues/new?template=install.yml).

## Code changes
1. Open an issue first for anything bigger than a typo, so we can agree on it.
2. Fork the repo, then branch from `main`.
3. Set up and test:
   ```
   pip install pillow
   make test        # builder + leak-oracle tests, no phone needed
   make build       # needs macOS (uses the `shortcuts` CLI to sign)
   ```
4. Open a pull request into `main`. Fill in the template. CI must pass.

### Ground rules
- **The shortcuts are generated.** Edit `tools/build_shortcuts.py` (and `tools/shortcutlib.py`), never the `.shortcut` files by hand.
- **Names must stay plain** (letters, digits, `.`, `_`, `-`). GitHub renames anything else in release files, and an imported shortcut is named after its file. A test enforces this.
- **Privacy is the product.** No network actions, no analytics, no new permissions. Any change that touches what gets stripped needs a test that proves the leak checker catches the leak first, then passes.
- **Don't claim what you haven't tested.** Docs and the site say "expected" until a real device result exists.
- Keep the playful tone ([docs/VOICE_AND_DESIGN.md](docs/VOICE_AND_DESIGN.md)).

### Commits and privacy
Use a private commit email, not your personal one. In GitHub: Settings → Emails → tick **Keep my email addresses private** and **Block command line pushes that expose my email**, then use your `ID+username@users.noreply.github.com` address in git.

### Releases
Maintainers only. Site buttons download the signed files from the GitHub Release (that's what makes downloads countable).

## License
By contributing you agree your work is released under the [MIT License](LICENSE).
