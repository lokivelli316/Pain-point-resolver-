# Roadmap

Status is kept honest in `data/pain_points.json` (`ppr pain`). This file lists the work.

## Now: foundation (0.1)
- [x] Core: reporter, register, fingerprint, ELF inspector, scanner, calm runner, pattern engine
- [x] `doctor`, `docs`, `hunt`, `calm`, `a11y`, `register`
- [x] Pain map as data, with tests keeping modules and map in sync
- [ ] CI green on x86_64 and arm64
- [ ] First 10 community patterns

## Next: the leverage point (0.2)
- [ ] **`install-api`**: artifact manifest, arch/libc/CPU-feature/schema/port/auth pre-flight, isolated prefix → `docs/specs/artifact-manifest.md` · pain 30–36
- [ ] **`up`**: service ordering with health checks, automatic free ports → `docs/specs/services-and-ports.md` · pain 3, 26, 36
- [ ] `doctor`: CPU-feature check of binaries against `/proc/cpuinfo` (needs an instruction-set scan, help wanted)

## Then: graphs and traces (0.3)
- [ ] **`deps`**: read lockfiles (npm, pip, cargo, go), unified graph, SBOM export (CycloneDX JSON), stale/unpinned report → `docs/specs/dependency-graph.md` · pain 9, 16–22
- [ ] **`trace`**: staged install → build → runtime run with the first failing boundary named → `docs/specs/causal-trace.md` · pain 23–29

## Human side (ongoing)
- [ ] Guided learning paths from recorded failures (pain 43, 44, 48)
- [ ] Technical-debt budget report from findings over time (pain 49)
- [ ] Screen-reader testing with TalkBack in Termux (pain 57)
- [ ] Termux:X11 terminal profile with line height and letter spacing (pain 51, 56)

## Help wanted
Anything unchecked. Comment on the matching issue before starting so work isn't duplicated.
