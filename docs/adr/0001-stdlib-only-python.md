# ADR 0001: Python standard library only

Status: accepted · 2026-09-17

**Context.** The tool must install on a fresh Android phone in Termux, where compiling native wheels is slow and fragile. The original ForgeDoc was a shell script; it was hard to test and to extend with structured data.

**Decision.** Python 3.11+ (for `tomllib`), no runtime dependencies. Development tools may be used in CI only.

**Consequences.** Easy installs everywhere and a fast test suite. Some features (YAML, rich terminals) are off the table. Anything needing a heavy library becomes an optional export for an external tool.
