# ADR 0003: Append-only, hash-chained registers; upgrade-only outputs

Status: accepted · 2026-09-17

**Decision.** Event history is JSON Lines where each entry stores the SHA-256 of the previous one. Nothing rewrites a register. Every run writes to a new timestamped folder. Replaced user files (e.g. a Termux theme) are renamed with a `retired-<timestamp>` suffix, never deleted.

**Consequences.** History is trustworthy enough to learn from, and `ppr register verify` catches edits. The chain is tamper-evident, not tamper-proof (no signatures). Disk use grows; a future `ppr prune` must be explicit and user-initiated.
