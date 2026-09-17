Rules every contributor, human or AI, follows in this repository:

1. Standard library only. No runtime dependencies. Python 3.11+.
2. Upgrade-only outputs: never overwrite a report or register. New run, new folder.
3. Registers are append-only. Corrections are new entries.
4. No document certifies itself. Claims of "resolved" need a test that proves it.
5. All output goes through `Reporter`. No colour-only meaning, no spinners, no box drawing.
6. Every new failure pattern ships with a sample in `tests/samples/`.
7. Be honest about confidence (`high` / `medium` / `low`).
