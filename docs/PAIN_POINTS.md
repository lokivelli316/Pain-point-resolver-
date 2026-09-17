# Pain point map

_Generated from `src/pain_point_resolver/data/pain_points.json`. Edit that file, then run `python scripts/gen_pain_points_md.py`._

Status: **open** 30 · **partial** 32

Leverage point: **#30**

## Environment & Setup

| # | Pain point | Contract | Status | Modules |
|---|---|---|---|---|
| 1 | Environment non-determinism (works on my machine) | environment | partial | `doctor` |
| 2 | Complicated installs with unclear steps and no progress feedback | environment | partial | `docs` |
| 3 | Port conflicts between projects and services | environment | partial | `doctor` |
| 4 | Outdated or missing docs (README, .env.example) that don't match reality | environment | partial | `docs` |
| 5 | Long onboarding before a newcomer can contribute | environment | partial | `docs` |
| 6 | Android sandboxing: SELinux W^X and scoped storage block execution and access | environment | partial | `doctor` |
| 7 | Android background restrictions and process killing during builds | environment | partial | `hunt` |

## Build Systems

| # | Pain point | Contract | Status | Modules |
|---|---|---|---|---|
| 8 | Slow compile cycles | build-api | open | help wanted |
| 9 | Non-deterministic dependency graphs (no lockfiles, no pinned toolchains) | build-api | open | help wanted |
| 10 | Build tool performance regressions and rising CI cost | build-api | open | help wanted |
| 11 | AAPT2/Gradle architecture mismatches on ARM64 Android | build-api | partial | `doctor` |
| 12 | Cross-compilation failures: missing libs, linker flags, host tool discovery | build-api | partial | `doctor` |
| 13 | Imperative build scripts causing non-reproducibility and cache misses | build-api | open | help wanted |
| 14 | Fragmented toolchains across projects and platforms | build-api | open | help wanted |
| 15 | Insufficient build tooling | build-api | open | help wanted |

## Dependency Management

| # | Pain point | Contract | Status | Modules |
|---|---|---|---|---|
| 16 | Dependency upkeep draining time from real work | dependency | open | help wanted |
| 17 | Dependencies frozen at first choice, then needing urgent patches | dependency | open | help wanted |
| 18 | No visibility into transitive dependencies | dependency | open | help wanted |
| 19 | Dependency hell: conflicting or bloated versions | dependency | open | help wanted |
| 20 | Supply-chain risk from unmaintained or malicious packages | dependency | open | help wanted |
| 21 | Alert overload from vulnerability and patch notices | dependency | open | help wanted |
| 22 | Package manager resolution limits and mirror failures | dependency | open | help wanted |

## Debugging & Observability

| # | Pain point | Contract | Status | Modules |
|---|---|---|---|---|
| 23 | Misidentified root causes; fixes that create new bugs | observability | partial | `hunt` |
| 24 | Dev vs production divergence | observability | open | help wanted |
| 25 | Inconsistent logging; hunting for the real error message | observability | partial | `hunt` |
| 26 | Service start ordering: APIs look broken while backends warm up | observability | open | help wanted |
| 27 | Latency in distributed API calls | observability | open | help wanted |
| 28 | Long stack traces and logs that are slow to read and easy to misread | observability | partial | `hunt` |
| 29 | Bugs that cannot be reproduced reliably | observability | partial | `hunt`, `register` |

## API Lifecycle & Cross-Build

| # | Pain point | Contract | Status | Modules |
|---|---|---|---|---|
| 30 | Installing and debugging your own APIs from other builds (foreign artifacts, unknown compatibility) | build-api | partial | `doctor` |
| 31 | Schema drift between sandbox and production | build-api | open | help wanted |
| 32 | Auth cascade failures: expired tokens causing 401s downstream | build-api | partial | `hunt` |
| 33 | Silent rate limiting that looks like a performance bug | build-api | partial | `hunt` |
| 34 | APIs that return unhelpful status codes | build-api | open | help wanted |
| 35 | Binary incompatibility: wrong CPU/libc assumptions (Illegal instruction) | build-api | partial | `doctor` |
| 36 | Port binding mistakes (localhost vs 0.0.0.0) | build-api | partial | `doctor` |

## Tooling & Workflow

| # | Pain point | Contract | Status | Modules |
|---|---|---|---|---|
| 37 | Tool sprawl and context switching | build-api | open | help wanted |
| 38 | Too many tedious manual tasks | build-api | open | help wanted |
| 39 | Manual code review bottlenecks | build-api | open | help wanted |
| 40 | Security testing bottlenecks | build-api | open | help wanted |
| 41 | Rework | build-api | open | help wanted |
| 42 | Slow redeploys | build-api | open | help wanted |

## Learning & Human Factors

| # | Pain point | Contract | Status | Modules |
|---|---|---|---|---|
| 43 | No structured guidance for self-taught developers | human | open | help wanted |
| 44 | Too many resources, no progress | human | open | help wanted |
| 45 | Imposter syndrome (Cannot be automated away; tooling can only reduce the load.) | human | open | help wanted |
| 46 | Isolation when learning alone (Cannot be automated away; tooling can only reduce the load.) | human | open | help wanted |
| 47 | Cognitive overload from how material is presented | human | partial | `calm` |
| 48 | Copy-paste without understanding | human | partial | `docs` |

## Maintenance & Burnout

| # | Pain point | Contract | Status | Modules |
|---|---|---|---|---|
| 49 | Technical debt accumulation | human | partial | `register` |
| 50 | Burnout (Cannot be automated away; tooling can only reduce the load.) | human | partial | `calm` |

## Visual Accessibility

| # | Pain point | Contract | Status | Modules |
|---|---|---|---|---|
| 51 | Astigmatism: tight monospace text blurs together | human | partial | `a11y` |
| 52 | Farsightedness: small default terminal text | human | open | help wanted |
| 53 | Migraine triggers: flicker, glare, constant redraw | human | partial | `calm` |
| 54 | Sensory intensity of build output (rapid scrolling, flashing status) | human | partial | `calm` |
| 55 | Colour schemes that are either harsh or too low-contrast | human | partial | `a11y` |
| 56 | No line-height or letter-spacing control in Termux | human | partial | `a11y` |

## Screen Reader & Assistive Tech

| # | Pain point | Contract | Status | Modules |
|---|---|---|---|---|
| 57 | Terminal output is hard for screen readers to follow | human | open | help wanted |
| 58 | No accessible, line-by-line mode for build and CI logs | human | partial | `calm` |

## Cognitive & Sensory

| # | Pain point | Contract | Status | Modules |
|---|---|---|---|---|
| 59 | Cognitive overload from simultaneous text, colour and status channels | human | partial | `calm` |
| 60 | Context switching between AI output and your own code under magnification | human | partial | `docs` |
| 61 | Box-drawing and decorative Unicode adding noise | human | partial | `calm` |
| 62 | No standard accessible mode for CLIs | human | partial | `a11y` |
