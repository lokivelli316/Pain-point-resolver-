"""ppr hunt / ppr calm — run a command, keep the full log, diagnose failures, record them."""
from __future__ import annotations

import argparse
import shlex
from datetime import datetime
from pathlib import Path

from ..core import paths, patterns, runner
from ..core.module import Context, Module
from ..core.register import Register
from ..core.stack import project_name

ERRORS_FILE = "errors.jsonl"
ERRORS_MD = "ERROR_REGISTER.md"


def errors_register() -> Register:
    return Register(paths.ensure_output_root() / ERRORS_FILE)


def execute(cmd: list[str], ctx: Context, calm: bool, interval: float, heartbeat: float) -> int:
    r = ctx.reporter
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        r.fail("No command given. Example: ppr hunt -- npm install")
        return 2

    project = project_name(Path.cwd())
    out = paths.new_run_dir("hunts", project)
    log = out / "output.log"
    shown = shlex.join(cmd)
    r.step(f"running: {shown}")
    r.plain(f"full log: {log}")

    result = runner.run_captured(cmd, log, r, calm=calm, min_interval=interval, heartbeat=heartbeat)
    text = log.read_text(encoding="utf-8", errors="replace")
    findings = patterns.diagnose(text)

    report = out / "REPORT.md"
    report.write_text("\n".join([
        f"# Hunt report: {project}",
        f"- When: {datetime.now():%Y-%m-%d %H:%M:%S}",
        f"- Directory: `{Path.cwd()}`",
        f"- Command: `{shown}`",
        f"- Exit code: **{result.returncode}**",
        f"- Duration: {result.seconds:.1f}s, {result.lines} lines",
        "",
        "## Diagnosis",
        patterns.findings_markdown(findings),
        "## Output (last 80 lines, cleaned)",
        "```",
        *runner.tail(log, 80),
        "```",
        "",
    ]), encoding="utf-8")

    if result.returncode != 0 or findings:
        entry = errors_register().append({
            "project": project,
            "cwd": str(Path.cwd()),
            "cmd": shown,
            "exit": result.returncode,
            "findings": [f.id for f in findings],
            "report": str(report.relative_to(paths.output_root())),
            "tail": runner.tail(log, 12),
        })
        md = paths.output_root() / ERRORS_MD
        if not md.exists():
            md.write_text("# Error register (append-only mirror of errors.jsonl)\n\n", encoding="utf-8")
        with md.open("a", encoding="utf-8") as fh:
            fh.write(f"### #{entry['seq']} · {entry['ts']} · project: {project} · exit {result.returncode}\n")
            fh.write(f"- Command: `{shown}`\n- Report: `{entry['report']}`\n")
            fh.write(patterns.findings_markdown(findings) + "\n")

    r.heading("Result")
    if result.returncode == 0:
        r.ok(f"exit 0 in {result.seconds:.0f}s")
    else:
        r.fail(f"exit {result.returncode} after {result.seconds:.0f}s")
        if calm:
            r.plain("last lines:")
            for line in runner.tail(log, 8):
                r.plain(f"  {line}")
    for f in findings:
        r.warn(f.diagnosis)
        r.plain(f"    fix: {f.fix}")
    r.plain(f"report: {report}")
    return result.returncode


class Hunt(Module):
    name = "hunt"
    summary = "Run a command, diagnose any failure, record it in the append-only error register"
    pain_points = (7, 23, 25, 28, 29, 32, 33)
    status = "partial"
    contract = "observability"

    def add_arguments(self, p: argparse.ArgumentParser) -> None:
        p.add_argument("--calm", action="store_true", help="calm output (stage lines + heartbeat only)")
        p.add_argument("--interval", type=float, default=0.25, help="minimum seconds between screen lines")
        p.add_argument("cmd", nargs=argparse.REMAINDER, help="command to run, after --")

    def run(self, args: argparse.Namespace, ctx: Context) -> int:
        return execute(args.cmd, ctx, calm=args.calm, interval=args.interval, heartbeat=20.0)


class Calm(Module):
    name = "calm"
    summary = "Run a build with low-motion, low-flicker output (full log kept on disk)"
    pain_points = (47, 50, 53, 54, 58, 59, 61)
    status = "partial"
    contract = "human"

    def add_arguments(self, p: argparse.ArgumentParser) -> None:
        p.add_argument("--interval", type=float, help="minimum seconds between screen lines (default 0.5)")
        p.add_argument("--heartbeat", type=float, help="seconds between 'still running' lines (default 20)")
        p.add_argument("--print-env", action="store_true",
                       help="print shell exports that calm down most tools, for your ~/.bashrc")
        p.add_argument("cmd", nargs=argparse.REMAINDER, help="command to run, after --")

    def run(self, args: argparse.Namespace, ctx: Context) -> int:
        if args.print_env:
            for key, value in runner.CALM_ENV.items():
                ctx.reporter.plain(f"export {key}={shlex.quote(value)}")
            for key in runner.DROP_ENV:
                ctx.reporter.plain(f"unset {key}")
            return 0
        cfg = ctx.config.get("calm", {})
        interval = args.interval if args.interval is not None else float(cfg.get("interval", 0.5))
        heartbeat = args.heartbeat if args.heartbeat is not None else float(cfg.get("heartbeat", 20))
        return execute(args.cmd, ctx, calm=True, interval=interval, heartbeat=heartbeat)
