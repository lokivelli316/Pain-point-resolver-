# ADR 0004: Accessibility is an output contract

Status: accepted · 2026-09-17

**Decision.** All output goes through `core.output.Reporter`, and streamed foreign output goes through `core.runner`. The rules in ACCESSIBILITY.md are requirements, checked in review and, where possible, by tests.

**Consequences.** Some visual polish is given up. Calm, readable output is the default experience rather than an opt-in mode.
