# Spec: `ppr deps`

**Status:** draft · **Pain points:** 9, 16–22 · **Contract:** dependency

Read the lockfiles a project already has, build one graph, and report on it. Stdlib only, no network by default.

## Inputs
| Ecosystem | File | Parser |
|---|---|---|
| npm | `package-lock.json` v2/v3 (`packages` map) | json |
| Python | `requirements.txt`, `pip freeze` output | text |
| Rust | `Cargo.lock` | tomllib |
| Go | `go.mod`, `go.sum` | text |

## Output
- `deps/<project>/<timestamp>/graph.json`: `{nodes: [{id, name, version, ecosystem, direct}], edges: [[from, to]]}`
- `sbom.cdx.json`: CycloneDX 1.5 JSON, components only
- Screen summary: direct vs transitive counts, and the checks below

## Checks
- No lockfile (pain 9)
- Unpinned direct dependencies (9, 17)
- Same package at several versions (19)
- Very deep chains (18)
- Optional: `--osv` exports a list for `osv-scanner` rather than calling the network itself (20, 21)
