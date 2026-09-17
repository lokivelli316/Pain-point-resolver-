"""Run a command, keep the full log on disk, show a calm stream on screen.

Human contract (pain points #53, #54, #58, #59): the full raw output goes to a
log file. The terminal gets complete lines only, rate-limited, with colour,
progress bars and box drawing removed. In calm mode it gets even less: stage
lines and a heartbeat, never a flood.
"""
from __future__ import annotations

import os
import re
import selectors
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from .output import Reporter, clean_line

CALM_ENV = {
    "NO_COLOR": "1",
    "CLICOLOR": "0",
    "CI": "true",
    "TERM": "dumb",
    "PYTHONUNBUFFERED": "1",
    "PIP_PROGRESS_BAR": "off",
    "PIP_DISABLE_PIP_VERSION_CHECK": "1",
    "npm_config_progress": "false",
    "npm_config_fund": "false",
    "npm_config_audit": "false",
    "npm_config_color": "false",
    "CARGO_TERM_PROGRESS_WHEN": "never",
    "CARGO_TERM_COLOR": "never",
}
DROP_ENV = ("FORCE_COLOR", "CLICOLOR_FORCE")

STAGE_RE = re.compile(
    r"^(> Task|Step \d|={3,}>|-{3,}>|\[\d+/\d+\]|Collecting |Building |Compiling |Installing |"
    r"Downloading |Successfully |Finished |Running |Linking |added \d+ packages|BUILD )",
    re.IGNORECASE,
)
ERROR_RE = re.compile(r"\b(error|failed|fatal|exception|traceback)\b", re.IGNORECASE)


@dataclass
class RunResult:
    returncode: int
    lines: int
    seconds: float
    log_path: Path


def calm_environment(base: dict | None = None) -> dict:
    envv = dict(base if base is not None else os.environ)
    for key in DROP_ENV:
        envv.pop(key, None)
    envv.update(CALM_ENV)
    return envv


def run_captured(
    cmd: list[str],
    log_path: Path,
    reporter: Reporter,
    calm: bool = False,
    min_interval: float = 0.5,
    heartbeat: float = 20.0,
    cwd: Path | None = None,
) -> RunResult:
    """Run cmd. calm=True: stage/error lines + heartbeat only. min_interval caps screen updates (0.5s = 2/s)."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    last_shown = 0.0
    last_beat = started
    count = 0
    held: str | None = None  # newest line suppressed by the rate limit
    env = calm_environment() if calm else None

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, env=env)
    except FileNotFoundError:
        log_path.write_text(f"{cmd[0]}: command not found\n", encoding="utf-8")
        return RunResult(127, 1, 0.0, log_path)

    def show(line: str) -> None:
        nonlocal last_shown, held
        now = time.monotonic()
        if now - last_shown >= min_interval:
            reporter.plain(line)
            last_shown, held = now, None
        else:
            held = line

    assert proc.stdout is not None
    sel = selectors.DefaultSelector()
    sel.register(proc.stdout, selectors.EVENT_READ)
    buf = b""
    with log_path.open("wb") as log:
        while True:
            events = sel.select(timeout=1.0)
            if events:
                chunk = os.read(proc.stdout.fileno(), 65536)
                if not chunk:
                    break
                log.write(chunk)
                buf += chunk
                *complete, buf = buf.split(b"\n")
                for raw in complete:
                    line = clean_line(raw.decode("utf-8", "replace"), collapse=True)
                    if not line.strip():
                        continue
                    count += 1
                    if ERROR_RE.search(line):
                        reporter.plain(line)  # errors are never rate-limited away
                        last_shown = time.monotonic()
                    elif not calm or STAGE_RE.search(line.lstrip()):
                        show(line)
            now = time.monotonic()
            if calm and now - last_beat >= heartbeat:
                reporter.plain(f"... still running: {count} lines, {int(now - started)}s")
                last_beat = now
            if held and now - last_shown >= min_interval:
                show(held)
        if buf.strip():
            count += 1
            line = clean_line(buf.decode("utf-8", "replace"))
            if not calm or ERROR_RE.search(line):
                reporter.plain(line)
    sel.close()
    proc.stdout.close()
    proc.wait()
    if held:
        reporter.plain(held)
    return RunResult(proc.returncode, count, time.monotonic() - started, log_path)


def tail(path: Path, n: int = 80) -> list[str]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    return [clean_line(l) for l in lines[-n:]]
