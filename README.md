# Poof! 🫧

[![ci](https://github.com/logrelu/poof-photo-scrubber/actions/workflows/ci.yml/badge.svg)](https://github.com/logrelu/poof-photo-scrubber/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Photos that forget **where and when** the moment you share them. No app. Your library keeps its memories.

- **How:** a bundle of signed Apple Shortcuts (share-sheet action + Action Button/clipboard flows)
- **Why Shortcuts not an app:** see [docs/RESEARCH.md](docs/RESEARCH.md) and [docs/SOLUTION.md](docs/SOLUTION.md)
- **Is it done?** [docs/DEFINITION_OF_SUCCESS.md](docs/DEFINITION_OF_SUCCESS.md) · **How we test:** [docs/QA_WORKFLOW.md](docs/QA_WORKFLOW.md)

```
make build     # generate + sign build/*.shortcut
make test      # builder + leak-oracle tests (no phone needed)
make mac-qa    # run the real shortcut on macOS and verify output
open site/index.html
```
## Install (iPhone)
Open **https://logrelu.github.io/poof-photo-scrubber/** on your iPhone, tap **Download** under *Poof*, open the file, tap **Add Shortcut**. Signed files also live on the [Releases](../../releases) page.

## Contributing
Testing on your own phone is the most useful help right now. See [CONTRIBUTING.md](CONTRIBUTING.md), and please follow the [Code of Conduct](CODE_OF_CONDUCT.md). Found a leak? See [SECURITY.md](SECURITY.md).

## License
[MIT](LICENSE).
