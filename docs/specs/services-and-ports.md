# Spec: `ppr up`

**Status:** draft · **Pain points:** 3, 26, 36 · **Contract:** environment

Start a project's services in dependency order, give each a free port, and wait for health before starting dependants.

```toml
# ppr.toml
[services.db]
cmd = "postgres -D ~/pgdata"
port = 5432
health = "tcp"

[services.api]
cmd = "python app.py"
port = "auto"            # first free port from 8000 up
env_port = "PORT"        # exported to the process
health = "http://127.0.0.1:{port}/health"
after = ["db"]
timeout = 60
```

Behaviour:
1. Topologically sort by `after`; a cycle is a usage error.
2. Resolve ports with `env.port_free`; export `PPR_PORT_<NAME>` to every service.
3. Start each through `core.runner` (logs under `up/<project>/<timestamp>/<service>.log`).
4. Poll health (TCP connect or HTTP 2xx via `urllib`) with backoff until `timeout`.
5. On failure, name the service and show its last log lines. Don't start dependants.
6. `ppr up --down` stops what the last run started (PIDs recorded in `up.jsonl`).
7. Warn when a service binds 127.0.0.1 but a dependant runs in proot or on another device.
