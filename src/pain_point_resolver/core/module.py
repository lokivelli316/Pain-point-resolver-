"""The module contract. Every `ppr <command>` is one Module subclass.

A module declares:
  name         the sub-command
  summary      one line for `ppr --help`
  pain_points  ids from data/pain_points.json it resolves or reduces
  status       "working" | "partial" | "planned"
  contract     which of the five contracts it belongs to

and implements add_arguments() and run(). See docs/MODULE_GUIDE.md.
"""
from __future__ import annotations

import argparse
import json
import tomllib
from dataclasses import dataclass, field
from functools import lru_cache
from importlib import resources
from pathlib import Path

from . import paths
from .output import Reporter

CONTRACTS = ("environment", "dependency", "build-api", "observability", "human")


@dataclass
class Context:
    reporter: Reporter
    config: dict = field(default_factory=dict)


def load_config(project: Path | None = None) -> dict:
    """User config (~/.config/ppr/config.toml) overlaid by project config (./ppr.toml)."""
    merged: dict = {}
    for candidate in (paths.config_dir() / "config.toml", (project or Path.cwd()) / "ppr.toml"):
        if candidate.is_file():
            with candidate.open("rb") as fh:
                for section, values in tomllib.load(fh).items():
                    if isinstance(values, dict):
                        merged.setdefault(section, {}).update(values)
                    else:
                        merged[section] = values
    return merged


@lru_cache(maxsize=1)
def pain_points() -> dict[int, dict]:
    raw = resources.files("pain_point_resolver.data").joinpath("pain_points.json").read_text(encoding="utf-8")
    return {item["id"]: item for item in json.loads(raw)["pain_points"]}


class Module:
    name: str = ""
    summary: str = ""
    pain_points: tuple[int, ...] = ()
    status: str = "planned"
    contract: str = ""

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Declare command-line options."""

    def run(self, args: argparse.Namespace, ctx: Context) -> int:
        raise NotImplementedError


class PlannedModule(Module):
    """A declared-but-unbuilt command. It explains itself and points contributors at the spec."""

    status = "planned"
    spec: str = ""

    def run(self, args: argparse.Namespace, ctx: Context) -> int:
        r = ctx.reporter
        r.warn(f"'ppr {self.name}' is planned, not built yet.")
        r.plain(f"Resolves pain points: {', '.join(map(str, self.pain_points))}")
        if self.spec:
            r.plain(f"Spec: {self.spec}")
        r.plain("Want to build it? See CONTRIBUTING.md and the 'module: " + self.name + "' issue label.")
        return 2
