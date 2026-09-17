# Spec: `ppr trace`

**Status:** draft · **Pain points:** 23–29 · **Contract:** observability

Run a project's lifecycle as named stages and report the **first failing boundary** instead of the last error printed.

```toml
# ppr.toml
[[trace.stage]]
name = "install"
cmd = "npm ci"

[[trace.stage]]
name = "build"
cmd = "npm run build"

[[trace.stage]]
name = "start"
cmd = "npm start"
background = true
ready = "http://127.0.0.1:3000/health"

[[trace.stage]]
name = "smoke"
cmd = "curl -fsS http://127.0.0.1:3000/api/ping"
```

Behaviour:
1. Each stage runs through `core.runner` with its own log; `trace.jsonl` gets one entry per stage (start, end, exit, findings) sharing a `run_id`.
2. The first stage with non-zero exit, or a `ready` probe that never passes, is the boundary. Later stages are skipped and marked as such.
3. The report shows: boundary stage, diagnosis from `core.patterns`, last lines, and the previous successful run of the same stage (from the register) for comparison. This is what helps with "it worked yesterday" (pain 24, 29).
4. `--export otel` may later write OpenTelemetry-compatible JSON spans.
