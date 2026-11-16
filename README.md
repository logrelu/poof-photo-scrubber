# Poof! 🫧
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
Install on iPhone: AirDrop/iCloud-share the `.shortcut` files from `build/`, tap **Add Shortcut**.
