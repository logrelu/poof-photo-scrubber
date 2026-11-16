# Build Plan (goal: installable on an iPhone and passing the phone test)

Each step = one commit = one push. A step is "done" only when its gate passes.

| # | Step | Gate | Status |
|---|---|---|---|
| 1 | Research, solution, success criteria, QA, voice docs | reviewed | done |
| 2 | Shortcut builder + Poof bundle (sign) | `make build` signs 4 files | done |
| 3 | Leak oracle + fixtures + unit tests | `make test` green | done |
| 4 | Install page + Mac runtime QA script | page renders | done |
| 5 | **PLAN + PHONE_TEST + CI** (this step) | CI green on GitHub | in progress |
| 6 | Mac runtime QA: run real shortcut, verify output | `make mac-qa` CLEAN | blocked: needs one "Add Shortcut" click |
| 7 | Fix engine if Step 6 leaks (fallback re-encode path) | oracle CLEAN | pending |
| 8 | Phone install pack (AirDrop) + PHONE_TEST pass on a real iPhone | checklist D1-D7 | pending (user) |
| 9 | Frictionless install page (`shortcuts://import-workflow`), DISTRIBUTION.md | 3-tap install on phone | pending |
| 10 | Release: public Pages repo, versioned signed files, changelog | install from site | pending |

## Testing pyramid
1. **CI (every push):** unit tests, oracle self-test, plist validity. Ubuntu runner, no Apple tooling.
2. **Mac runtime (before phone):** real Convert Image on macOS Shortcuts, oracle verifies.
3. **Phone (release gate):** docs/PHONE_TEST.md, ~10 minutes.

## Constraint note
Private repo + GitHub Pages needs a paid plan, and `shortcuts://import-workflow?url=` can't fetch from a
private repo. So: **phone testing during development = AirDrop from the Mac.** Public release repo comes in Step 10.
