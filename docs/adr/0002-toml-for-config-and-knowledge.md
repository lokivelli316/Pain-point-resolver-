# ADR 0002: TOML for configuration and knowledge; JSON for maps and registers

Status: accepted · 2026-09-17

**Context.** Early design sketches used YAML, which the standard library cannot read.

**Decision.** Human-edited files (config, patterns, manifests) are TOML. Machine-maintained data (pain map, registers, fingerprints) is JSON / JSON Lines.

**Consequences.** Non-programmers can add patterns safely. `ppr.toml` replaces the sketched `dev.yaml` / `accessibility.yaml`.
