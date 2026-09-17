# Pain Point Resolver

**Turn recurring developer pain into pre-flight checks.**
Termux-first. Accessibility-first. Standard library only.

> ### 📣 Report a pain point → [**open one here**](https://github.com/lokivelli316/Pain-point-resolver-/issues/new?template=pain_point.yml)
> No pain is too small. No question is too basic. Nobody gets left behind.

---

## The call

Every developer carries a list of problems they've quietly learned to live with. There's the install that fails with no explanation. There's the error that means something completely different from what it says, and the build that works on one machine but never on the next. There's the screen full of scrolling noise that ends the session with a headache.

Most of those problems are never fixed. They get worked around, alone, and then forgotten, until the next person hits the same wall and starts from zero.

**This project exists to stop that loop.**

Somewhere right now a beginner is stuck on something a professional solved years ago and never wrote down. Somewhere a professional is losing an afternoon to something a beginner noticed first but was too nervous to mention. A pain point doesn't care about job titles. The one plaguing a first-week learner is often the same one quietly costing a senior engineer an hour a week.

So here is the invitation:

- **Amateurs**: your pain points are real data. Report them. You are not "just a noob", you are the early-warning system.
- **Professionals**: your fixes are worth more shared than remembered. Leave the trail for the people behind you.
- **AI collaborators and the people who work with them**: bring the tireless pattern-matching. Humans review, everyone contributes. Silicon and carbon, one team.
- **People with accessibility needs**: your constraints find the design failures everyone else has learned to tolerate. You are a core part of this project.

"Oh, that's a noob problem, I've got mine sorted" isn't welcome here. If it hurt you, it counts. If you fixed it, share it. If you can't fix it yet, say so. Someone else may be one step away.

We don't brush problems off. We name them, confirm them, hunt them together, and prove the fix with a test. Then we move to the next one.

**No coder left behind.** Not one small step for a few, but one solid leap for all programmer-kind.

*Robert "Lokivelli" Earlywine-Lucas, founder*

---

## How a pain point gets squashed

```
 report  -->  confirm  -->  hunt  -->  fix proposed  -->  resolved
 anyone       2+ people      open to     PR with a         a test proves it,
 can file     hit it too     everyone    test attached     and it's recorded
```

1. **Report it** with the [pain point form](https://github.com/lokivelli316/Pain-point-resolver-/issues/new?template=pain_point.yml). Say what hurt, how often, and what you tried.
2. **Confirm it**: if it hits you too, comment with your setup. Two independent confirmations move it to *confirmed*.
3. **Hunt it** in the issue or in [Discussions](https://github.com/lokivelli316/Pain-point-resolver-/discussions). Workarounds, root causes and half-ideas are all welcome.
4. **Fix it** with a pull request: a failure pattern, a scan check, a doc, or a whole new command.
5. **Resolve it** only when a test proves the fix. Nothing certifies itself.

The full process is in [docs/community/PAIN_POINT_LIFECYCLE.md](docs/community/PAIN_POINT_LIFECYCLE.md). AI-assisted contributors should also read [AI_COLLABORATORS.md](AI_COLLABORATORS.md).

---

## What the tool does today

`ppr` fingerprints your device, pre-flights your project, diagnoses failed commands, and writes install, running and troubleshooting manuals plus an AI handoff file. It also runs builds with calm, low-flicker output. Every run is saved, and failures go into an append-only, tamper-evident register, so the next person or the next AI starts from what is already known.

The project maps **62 common developer pain points** onto **five contracts**. Each command owns part of that map, and anyone can pick up the unbuilt parts.

```
ppr doctor              why is this broken? (device + project pre-flight)
ppr docs                write INSTALL / RUNNING / TROUBLESHOOTING / AI_HANDOFF
ppr hunt -- <cmd>       run it, diagnose the failure, record it
ppr calm -- <build>     same, with low-motion output for sensitive eyes
ppr a11y theme --apply  calibrated low-glare Termux colours, steady cursor
ppr register verify     prove the error history hasn't been edited
ppr pain                browse the 62-point pain map
ppr modules             what's built, what's planned, who owns what
```

## Install

**Termux (Android)**
```bash
pkg install -y git python
git clone https://github.com/lokivelli316/Pain-point-resolver-
cd Pain-point-resolver- && sh install.sh
```
Reports land in your phone's **Download/PainPointResolver/** folder.

**Linux / macOS**
```bash
git clone https://github.com/lokivelli316/Pain-point-resolver-
cd Pain-point-resolver- && sh install.sh     # uses pipx if present, else a private venv
```
Reports land in `~/.local/share/pain-point-resolver/`. Set `PPR_OUT` to put them anywhere else.

## Quick start

```bash
cd ~/my-project
ppr doctor                        # device + project pre-flight
ppr doctor --port 3000            # is the port free?
ppr doctor --binary ./vendor/tool # will this foreign binary run here?
ppr hunt -- npm install           # run and diagnose
ppr docs                          # write the document pack
```

Paste `AI_HANDOFF.md` into any AI assistant and it has your environment, project layout, open findings, recent failures and your project rules (`.ppr/RULES.md`) in one go.

## The five contracts

| Contract | Pain points | Built | Planned |
|---|---|---|---|
| Environment | 1–7, 11–14, 35–36, 51–56 | `doctor` | `up` |
| Dependency | 8–22, 31–32 | — | `deps` |
| Build / API | 30, 33–36, 39–42 | `doctor --binary` | `install-api` |
| Observability | 23–29, 49 | `hunt`, `register` | `trace` |
| Human & accessibility | 43–62 | `docs`, `calm`, `a11y` | see [ROADMAP.md](ROADMAP.md) |

**#30 is the leverage point.** It covers installing and debugging your own APIs across builds. Solving it forces environment fingerprinting, dependency graphing, causal tracing and pre-flight verification into existence, and those four resolve most of the rest. The spec is in [`docs/specs/artifact-manifest.md`](docs/specs/artifact-manifest.md).

Honest status: **32 of 62 partially covered, 0 fully resolved.** A pain point is only marked resolved when a test proves it. Some items (imposter syndrome, isolation, burnout) cannot be automated away. Tooling can only take weight off.

## Accessibility is a core requirement

Build output is a real migraine and eye-strain trigger. Every `ppr` command follows [ACCESSIBILITY.md](ACCESSIBILITY.md):
- status is carried by words, never by colour alone
- no spinners or box drawing
- `NO_COLOR` is honoured
- screen updates are rate-limited
- the full raw log always goes to disk

## Contributing

This project is meant to be built by more than one person. Start with [CONTRIBUTING.md](CONTRIBUTING.md). The easiest first contribution is a new failure pattern: one TOML block and one sample line, no Python required.

- [ROADMAP.md](ROADMAP.md): what's next and what's open
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): how the pieces fit
- [docs/MODULE_GUIDE.md](docs/MODULE_GUIDE.md): build a new command
- [GOVERNANCE.md](GOVERNANCE.md): how decisions are made

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
Started as *ForgeDoc* by Robert M. Earlywine-Lucas (Lokivelli).
