"""Declared-but-unbuilt commands. Each one is a place for contributors to start.

To build one: create modules/<name>.py with a real Module subclass, swap it in
modules/__init__.py, update data/pain_points.json, and follow its spec.
"""
from __future__ import annotations

from ..core.module import PlannedModule


class Up(PlannedModule):
    name = "up"
    summary = "(planned) start a project's services in order, with automatic free ports"
    pain_points = (3, 26, 36)
    contract = "environment"
    spec = "docs/specs/services-and-ports.md"


class InstallApi(PlannedModule):
    name = "install-api"
    summary = "(planned) verify a foreign API artifact (arch, libc, schema, ports, auth) before installing"
    pain_points = (30, 31, 32, 33, 34, 35, 36)
    contract = "build-api"
    spec = "docs/specs/artifact-manifest.md"


class Deps(PlannedModule):
    name = "deps"
    summary = "(planned) unified dependency graph, lockfile check and SBOM across builds"
    pain_points = (9, 16, 17, 18, 19, 20, 21, 22)
    contract = "dependency"
    spec = "docs/specs/dependency-graph.md"


class Trace(PlannedModule):
    name = "trace"
    summary = "(planned) trace install -> build -> runtime and name the first failing boundary"
    pain_points = (23, 24, 26, 27, 28, 29)
    contract = "observability"
    spec = "docs/specs/causal-trace.md"


PLANNED = [Up, InstallApi, Deps, Trace]
