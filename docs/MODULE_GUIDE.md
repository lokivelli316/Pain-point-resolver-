# Writing a command

A command is a `Module` subclass in `src/pain_point_resolver/modules/`.

```python
"""ppr ports: list which configured ports are free."""
from __future__ import annotations

import argparse

from ..core import env
from ..core.module import Context, Module


class Ports(Module):
    name = "ports"
    summary = "Check whether ports are free"
    pain_points = (3, 36)          # ids from data/pain_points.json
    status = "partial"             # working | partial | planned
    contract = "environment"       # environment | dependency | build-api | observability | human

    def add_arguments(self, p: argparse.ArgumentParser) -> None:
        p.add_argument("ports", nargs="+", type=int)

    def run(self, args: argparse.Namespace, ctx: Context) -> int:
        r = ctx.reporter
        busy = 0
        for port in args.ports:
            if env.port_free(port):
                r.ok(f"port {port} free")
            else:
                busy += 1
                r.fail(f"port {port} in use")
        return 1 if busy else 0
```

Then:

1. Add it to `MODULES` in `modules/__init__.py`.
2. In `data/pain_points.json`, add `"ports"` to the `modules` list of pain points 3 and 36, and set `status` to `partial` if it was `open`.
3. Add tests under `tests/`. `test_registry.py` fails if the map and modules disagree.

## Rules of thumb

- **Print only through `ctx.reporter`.** `ok`, `warn`, `fail`, `info`, `step` for status; `plain` for results; `heading` for sections.
- **Return codes:** `0` success, `1` problems found, `2` usage or setup error, command's own code for `hunt`/`calm`.
- **Running other programs:** use `core.runner.run_captured` if the output can be long; `subprocess.run(..., capture_output=True, timeout=...)` for quick probes.
- **Writing files:** `paths.new_run_dir("<command>", project)` gives a fresh folder. Never overwrite.
- **Recording events:** `Register(paths.ensure_output_root() / "<name>.jsonl").append({...})`.
- **Config:** read `ctx.config.get("<command>", {})`, which merges `~/.config/ppr/config.toml` and `./ppr.toml`.
- **Termux vs Linux:** check `paths.is_termux()`; never hardcode `/tmp`, `/usr/bin`, or `/sdcard`.

## Adding a scan check

In `core/scan.py`:

```python
def check_lockfile(ctx: ScanContext) -> None:
    if (ctx.root / "package.json").exists() and not (ctx.root / "package-lock.json").exists():
        ctx.add("medium", "package.json", "No lockfile: installs are not reproducible.",
                "npm install  (then commit package-lock.json)", [9])
```

Append it to `CHECKS` and add a test in `tests/test_core.py`.
