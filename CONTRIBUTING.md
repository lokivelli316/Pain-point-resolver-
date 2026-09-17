# Contributing

Thanks for helping. You do not need to be an expert. The project started on a phone in Termux, and it is built to be worked on the same way.

## Ground rules

These are pinned in [`.ppr/RULES.md`](.ppr/RULES.md) and apply to humans and AI assistants alike:

1. **Standard library only.** No runtime dependencies. Python 3.11+.
2. **Upgrade-only outputs.** Never overwrite a report or register entry; a new run gets a new folder.
3. **Append-only registers.** Corrections are new entries.
4. **Nothing certifies itself.** A pain point is only `resolved` when a test proves it.
5. **Accessible output.** Print through `Reporter`. No colour-only meaning, spinners or box drawing. See [ACCESSIBILITY.md](ACCESSIBILITY.md).
6. **Every pattern has a sample** in `tests/samples/`.
7. **Say how sure you are.** `high`, `medium` and `low` confidence are all acceptable; overclaiming is not.

## Pick a lane

| You have… | Start here |
|---|---|
| 2 minutes | [Report a pain point](https://github.com/lokivelli316/Pain-point-resolver-/issues/new?template=pain_point.yml), or say "me too" on one |
| 10 minutes, no Python | Add a failure pattern (below) |
| An error that `ppr hunt` didn't recognise | Open a **Failure pattern** issue with the log |
| An hour of Python | Add a scan check in `core/scan.py` |
| A weekend | Build a planned command (`up`, `install-api`, `deps`, `trace`) from its spec |
| Accessibility experience | Review or extend [ACCESSIBILITY.md](ACCESSIBILITY.md) and `modules/a11y.py` |
| A device we don't have | Run `ppr doctor --json` and attach it to a **Device report** issue |

Issues labelled `good first issue` are sized for newcomers. How reports move from *new* to *resolved* is described in [docs/community/PAIN_POINT_LIFECYCLE.md](docs/community/PAIN_POINT_LIFECYCLE.md). Using an AI assistant? Read [AI_COLLABORATORS.md](AI_COLLABORATORS.md).

## Add a failure pattern (no Python needed)

1. Add a block to `src/pain_point_resolver/data/patterns.toml`:
   ```toml
   [[pattern]]
   id = "your-pattern-id"
   regex = 'text that appears in the error'
   diagnosis = "What is actually wrong, in plain words."
   fix = "The command or action that fixes it."
   pain_points = [2]
   platforms = ["termux"]
   confidence = "medium"
   ```
2. Create `tests/samples/your-pattern-id.txt` containing a real error line (remove personal paths and tokens).
3. Run the tests (below) and open a pull request.

## Set up

```bash
git clone https://github.com/<you>/Pain-point-resolver-
cd Pain-point-resolver-
python -m venv .venv && . .venv/bin/activate    # on Termux you can skip the venv
pip install -e .
python -m unittest discover -s tests -t .
```

The whole suite runs in under a second, including on a phone.

## Build a command

Read [docs/MODULE_GUIDE.md](docs/MODULE_GUIDE.md). In short:

1. Create `src/pain_point_resolver/modules/<name>.py` with a `Module` subclass.
2. Register it in `modules/__init__.py` (and remove the planned stub if there is one).
3. Update `data/pain_points.json`: the module name under each pain point it touches, and `status` `partial`.
4. Add tests. `tests/test_registry.py` checks that the pain map and the modules agree.
5. Add a line to `CHANGELOG.md` under *Unreleased*.

## Pull requests

- Keep each PR to one change.
- Include the output of the test run.
- For anything that changes terminal output, paste a before/after sample.
- Say which pain point IDs the change affects.
- If an AI assistant wrote part of the change, say so. That's fine; review it like any other code.

## Commit messages

`area: short summary`, for example `patterns: add gradle daemon OOM` or `scan: detect glibc-only wheels`.

## Reporting security problems

Please don't open a public issue. See [SECURITY.md](SECURITY.md).

## Conduct

Be kind and assume good faith. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

By contributing you agree that your contribution is licensed under Apache-2.0.
