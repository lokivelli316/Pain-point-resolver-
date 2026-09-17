# Architecture

```
src/pain_point_resolver/
  cli.py                 argparse front end; builds sub-commands from the module registry
  core/                  shared pieces every command uses
    output.py            Reporter: the only way to print (accessibility rules live here)
    runner.py            run a command: full log to disk, calm/rate-limited stream to screen
    patterns.py          match output against data/patterns.toml -> Findings
    scan.py              static pre-flight checks -> Issues (list of small check functions)
    env.py               environment fingerprint (plain dict), port probe
    elf.py               ELF arch + dynamic loader reader (foreign-binary check)
    stack.py             project stack detection (install/run steps)
    register.py          append-only, hash-chained JSONL registers
    paths.py             Termux vs Linux locations, new_run_dir()
    module.py            Module contract, Context, config + pain-map loaders
  modules/               one file per command
    __init__.py          MODULES registry
    planned.py           stubs for unbuilt commands (they print their spec)
  data/
    patterns.toml        failure knowledge base (contributor-friendly)
    pain_points.json     the 62-point map: status + owning modules
```

## Data flow

```
ppr hunt -- cmd
  runner.run_captured ──> hunts/<project>/<timestamp>/output.log
          │
  patterns.diagnose ──> Findings ──> REPORT.md
          │
  register.append ──> errors.jsonl (hash chain) + ERROR_REGISTER.md (mirror)

ppr docs
  stack.detect + scan.scan + env.fingerprint + errors.jsonl (this project)
          └──> docs/<project>/<timestamp>/{INSTALL, RUNNING, TROUBLESHOOTING, AI_HANDOFF}.md
               builds.jsonl (hash chain)
```

## Output locations

| Platform | Root |
|---|---|
| Termux | `~/storage/downloads/PainPointResolver/` (Android Download folder) |
| Linux/macOS | `$XDG_DATA_HOME/pain-point-resolver/` |
| Anywhere | `PPR_OUT=/path` overrides |

Every run creates a fresh timestamped folder. Nothing is overwritten.

## The five contracts

Each module declares one contract. `ppr modules --contract <name>` filters by it.

| Contract | Question it answers |
|---|---|
| environment | Is this device able to run this? |
| dependency | Are the pieces this needs known, pinned and compatible? |
| build-api | Will this artifact work here, before I install it? |
| observability | Where exactly did it break? |
| human | Can a person read, follow and recover from this comfortably? |

## Design constraints

- Standard library only (ADR 0001), so it installs on a fresh phone with no compiler.
- Knowledge lives in data files (ADR 0002), so non-programmers can contribute.
- Registers are append-only and hash-chained (ADR 0003).
- Output rules are a contract, not a theme (ADR 0004).
