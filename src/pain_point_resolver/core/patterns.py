"""Diagnosis engine: match output text against data/patterns.toml.

Opaque-failure contract (pain points #23, #25, #28): turn a wall of log text
into a short list of named causes with a fix and the evidence line.
"""
from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from functools import lru_cache
from importlib import resources

from .output import clean_line


@dataclass
class Pattern:
    id: str
    regex: str
    diagnosis: str
    fix: str
    pain_points: list[int] = field(default_factory=list)
    platforms: list[str] = field(default_factory=lambda: ["any"])
    confidence: str = "medium"

    def __post_init__(self) -> None:
        self.compiled = re.compile(self.regex, re.IGNORECASE)


@dataclass
class Finding:
    id: str
    diagnosis: str
    fix: str
    evidence: str
    confidence: str
    pain_points: list[int]


@lru_cache(maxsize=1)
def load_patterns() -> tuple[Pattern, ...]:
    raw = resources.files("pain_point_resolver.data").joinpath("patterns.toml").read_bytes()
    data = tomllib.loads(raw.decode("utf-8"))
    return tuple(Pattern(**item) for item in data.get("pattern", []))


MODULE_RE = re.compile(r"No module named '([^']+)'")
COMMAND_RE = re.compile(r"(?:^|[\s:])([A-Za-z0-9_.+-]+): (?:command )?not found")


def diagnose(text: str) -> list[Finding]:
    lines = [clean_line(line) for line in text.splitlines()]
    findings: list[Finding] = []
    for pat in load_patterns():
        for line in lines:
            if pat.compiled.search(line):
                findings.append(Finding(pat.id, pat.diagnosis, pat.fix, line[:200], pat.confidence, pat.pain_points))
                break

    modules = sorted({m.split(".")[0] for m in MODULE_RE.findall(text)})
    if modules:
        names = " ".join(modules)
        findings.append(Finding(
            "missing-python-modules",
            f"Missing Python modules: {names}",
            f"pip install {names}   (check `pkg search python-<name>` first; import and pip names can differ, e.g. cv2 -> opencv-python)",
            f"No module named '{modules[0]}'", "high", [19],
        ))

    commands = sorted({c for c in COMMAND_RE.findall(text) if c not in {"line", "bash", "sh", "zsh"}})
    if commands:
        findings.append(Finding(
            "missing-commands",
            f"Missing commands: {' '.join(commands)}",
            "pkg install <package>   (find it with: pkg search <name>)",
            f"{commands[0]}: command not found", "high", [2],
        ))
    return findings


def findings_markdown(findings: list[Finding]) -> str:
    if not findings:
        return "- No known pattern matched. Share this report plus AI_HANDOFF.md (from `ppr docs`) with a helper.\n"
    out = []
    for f in findings:
        out.append(f"- **{f.diagnosis}** (`{f.id}`, confidence: {f.confidence})")
        out.append(f"  - Fix: `{f.fix}`")
        out.append(f"  - Evidence: `{f.evidence.replace('`', chr(39))}`")
    return "\n".join(out) + "\n"
