# Spec: artifact manifest and `ppr install-api`

**Status:** draft, open for contributors · **Pain points:** 30–36 · **Contract:** build-api

## Problem
An API, service or tool built in one environment is installed into another with no record of what it assumed. Failures show up late and look unrelated: `Illegal instruction`, `required file not found`, 401 cascades, silent 429s, a service bound to the wrong interface.

## Idea
Every build emits a small manifest describing what it needs. Before installing, `ppr install-api` compares that manifest with the target's fingerprint (`core.env.fingerprint()`) and refuses with named reasons.

## Manifest: `ppr-artifact.toml`

```toml
[artifact]
name = "notes-api"
version = "1.4.0"
kind = "service"                 # service | library | cli
created = "2026-09-17T12:00:00Z"
ppr_version = "0.2.0"

[build]
machine = "aarch64"              # platform.machine() of the build host
libc = "bionic"                  # bionic | glibc | musl
cpu_features = ["asimd", "crc32"]  # features the binaries actually require
runtimes = { python = ">=3.11", node = ">=20" }

[interface]
schema = "openapi.json"          # optional
schema_sha256 = "…"
health = "http://127.0.0.1:{port}/health"

[[interface.ports]]
name = "http"
default = 8080
bind = "127.0.0.1"               # or 0.0.0.0 when reachable from other devices

[auth]
kind = "bearer"                  # none | bearer | basic | custom
env = "NOTES_API_TOKEN"          # variable the service reads

[limits]
requests_per_minute = 60

[dependencies]
lockfiles = { "package-lock.json" = "sha256:…" }

[files]
"bin/notes-api" = "sha256:…"
```

## Commands

```
ppr install-api --emit [path]      write ppr-artifact.toml for a built project
ppr install-api <artifact-dir>     pre-flight, then install into an isolated prefix
ppr install-api <dir> --check      pre-flight only
```

## Pre-flight checks (in order; stop at the first failing group)

| # | Check | Uses | Pain |
|---|---|---|---|
| 1 | File hashes match | hashlib | 20 |
| 2 | ELF arch and loader fit the host | `core.elf` | 35 |
| 3 | Required CPU features present | `/proc/cpuinfo` | 35 |
| 4 | Runtime versions satisfied | `core.env` tools | 1, 12 |
| 5 | Ports free (or auto-reassigned) | `env.port_free` | 3, 36 |
| 6 | Bind address matches intended reach | manifest | 36 |
| 7 | Auth variable present and non-empty | env | 32 |
| 8 | Schema hash matches the one the client was built against | hashlib | 31 |

Each failure is an `Issue` with a fix, recorded to `installs.jsonl`.

## Install
- Default prefix: `~/.local/share/ppr/artifacts/<name>/<version>/` (never overwrites; old versions stay until removed).
- Writes an env file with the resolved ports and a `run` script.

## Open questions
- How to derive `cpu_features` reliably without a disassembler (help wanted).
- Whether to support signing (probably a later ADR).
