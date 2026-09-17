"""Static pre-flight scan (Verification contract: pain points #6, #30, #35, #39-41).

Each check is a small function `check_x(ctx) -> None` that calls ctx.add(...).
To add a check: write the function, append it to CHECKS, add a test.
"""
from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterator

from . import elf, env, paths

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "target", "dist", "build", ".tox"}
MAX_FILES = 5000
SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}

TMP_RE = re.compile(r"""["' ]/tmp/""")
INTERP_RE = re.compile(r"""["' ](/usr/bin/|/bin/)(python3?|node|bash|sh)(["' ]|$)""")


@dataclass
class Issue:
    severity: str
    path: str
    problem: str
    fix: str
    pain_points: list[int] = field(default_factory=list)


@dataclass
class ScanContext:
    root: Path
    issues: list[Issue] = field(default_factory=list)
    _files: list[Path] | None = None

    def add(self, severity: str, path: Path | str, problem: str, fix: str, pain_points: list[int] | None = None) -> None:
        rel = str(path)
        if isinstance(path, Path):
            try:
                rel = str(path.relative_to(self.root))
            except ValueError:
                rel = str(path)
        self.issues.append(Issue(severity, rel, problem, fix, pain_points or []))

    def files(self) -> list[Path]:
        if self._files is None:
            found: list[Path] = []
            for dirpath, dirnames, filenames in os.walk(self.root):
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
                for name in filenames:
                    found.append(Path(dirpath) / name)
                    if len(found) >= MAX_FILES:
                        break
                if len(found) >= MAX_FILES:
                    break
            self._files = found
        return self._files

    def by_suffix(self, *suffixes: str) -> Iterator[Path]:
        return (f for f in self.files() if f.suffix in suffixes)


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def check_location(ctx: ScanContext) -> None:
    if paths.on_shared_storage(ctx.root):
        ctx.add("high", ctx.root, "Project is on Android shared storage: no exec bits, no symlinks, slow I/O.",
                f"cp -r '{ctx.root}' ~/ && cd ~/{ctx.root.name}", [6])


def check_readme(ctx: ScanContext) -> None:
    if not any((ctx.root / n).exists() for n in ("README.md", "README", "README.rst", "readme.md")):
        ctx.add("low", "README", "No README found.", "Add README.md so people and AI helpers get context.", [4, 5])


def check_shell(ctx: ScanContext) -> None:
    bash = shutil.which("bash")
    for f in ctx.by_suffix(".sh"):
        text = _read(f)
        first = text.splitlines()[0] if text else ""
        if bash:
            res = subprocess.run([bash, "-n", str(f)], capture_output=True, text=True)
            if res.returncode != 0:
                msg = (res.stderr.strip().splitlines() or ["syntax error"])[0]
                ctx.add("high", f, f"Bash syntax error: {msg}", f"Fix the reported line, then: bash -n {f.name}", [23])
        if re.match(r"#!/(bin|usr/bin|usr/local/bin)/", first) and "bin/env" not in first:
            ctx.add("medium", f, f"Hardcoded shebang '{first}' breaks when termux-exec is not active.",
                    f"termux-fix-shebang {f.name}", [6])
        if not os.access(f, os.X_OK):
            ctx.add("low", f, "Not executable.", f"chmod +x {f.name}", [2])


def check_crlf(ctx: ScanContext) -> None:
    for f in ctx.files():
        if f.suffix in {".sh", ".py", ".js", ".env"} or f.name == "Makefile":
            try:
                if b"\r\n" in f.read_bytes()[:200_000]:
                    ctx.add("high", f, "Windows CRLF line endings (causes $'\\r': command not found).",
                            f"sed -i 's/\\r$//' {f.name}", [1])
            except OSError:
                pass


def check_python(ctx: ScanContext) -> None:
    for f in ctx.by_suffix(".py"):
        try:
            ast.parse(_read(f), str(f))
        except SyntaxError as exc:
            ctx.add("high", f, f"Python syntax error line {exc.lineno}: {exc.msg}", "Fix the reported line.", [23])


def check_json(ctx: ScanContext) -> None:
    for f in ctx.by_suffix(".json"):
        try:
            json.loads(_read(f))
        except ValueError as exc:
            ctx.add("high", f, f"Invalid JSON: {exc}", "Fix the JSON (trailing commas are the usual culprit).", [4])


def check_javascript(ctx: ScanContext) -> None:
    node = shutil.which("node")
    if not node:
        return
    for f in ctx.by_suffix(".js", ".cjs"):
        res = subprocess.run([node, "--check", str(f)], capture_output=True, text=True)
        if res.returncode != 0:
            lines = [l for l in res.stderr.splitlines() if "Error" in l] or ["syntax error"]
            ctx.add("high", f, f"JavaScript check failed: {lines[0]}", f"node --check {f.name}", [23])


def check_hardcoded_paths(ctx: ScanContext) -> None:
    for f in ctx.by_suffix(".py", ".sh", ".js"):
        for n, line in enumerate(_read(f).splitlines(), 1):
            if TMP_RE.search(line):
                ctx.add("medium", f"{f.relative_to(ctx.root)}:{n}", "Hardcoded /tmp path.",
                        "Use $TMPDIR (Python: tempfile.gettempdir()).", [1, 6])
            if n > 1 and INTERP_RE.search(line):
                ctx.add("medium", f"{f.relative_to(ctx.root)}:{n}", "Hardcoded /bin or /usr/bin interpreter.",
                        "Call the command by name, or use shutil.which().", [1, 6])


def check_binaries(ctx: ScanContext) -> None:
    """Foreign-artifact check: the first piece of `install-api` pre-flight (#30, #35)."""
    host_libc = env.detect_libc()
    for f in ctx.files():
        if f.suffix not in {"", ".so", ".node", ".bin"} and ".so." not in f.name:
            continue
        try:
            if f.stat().st_size < 64 or not elf.is_elf(f):
                continue
        except OSError:
            continue
        info = elf.read_elf(f)
        if info is None:
            continue
        for problem in elf.compatibility_problems(info, host_libc=host_libc):
            ctx.add("high", f, f"Foreign binary: {problem}.",
                    "Rebuild on/for this device, use the pkg build, or run under proot-distro.", [30, 35])


CHECKS: list[Callable[[ScanContext], None]] = [
    check_location, check_readme, check_shell, check_crlf, check_python,
    check_json, check_javascript, check_hardcoded_paths, check_binaries,
]


def scan(root: Path) -> list[Issue]:
    ctx = ScanContext(Path(root).resolve())
    for check in CHECKS:
        check(ctx)
    ctx.issues.sort(key=lambda i: (SEVERITY_ORDER.get(i.severity, 9), i.path))
    return ctx.issues


def issues_markdown(issues: list[Issue]) -> str:
    if not issues:
        return "- No issues found.\n"
    out = []
    for i in issues:
        out.append(f"- **[{i.severity.upper()}]** `{i.path}` — {i.problem}")
        out.append(f"  - Fix: `{i.fix}`")
    return "\n".join(out) + "\n"
