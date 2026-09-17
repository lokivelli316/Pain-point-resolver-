"""ppr doctor — why is this broken? Fingerprint + static pre-flight + port/binary checks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..core import elf, env, paths, scan
from ..core.module import Context, Module


class Doctor(Module):
    name = "doctor"
    summary = "Fingerprint this device and pre-flight a project (syntax, paths, foreign binaries, ports)"
    pain_points = (1, 3, 6, 11, 12, 30, 35, 36)
    status = "partial"
    contract = "environment"

    def add_arguments(self, p: argparse.ArgumentParser) -> None:
        p.add_argument("path", nargs="?", default=".", help="project directory (default: current)")
        p.add_argument("--port", type=int, action="append", default=[], help="check a port is free (repeatable)")
        p.add_argument("--binary", type=Path, action="append", default=[], help="inspect a binary for arch/libc fit")
        p.add_argument("--json", action="store_true", help="machine-readable output")
        p.add_argument("--save", action="store_true", help="also write a report to the output folder")

    def run(self, args: argparse.Namespace, ctx: Context) -> int:
        r = ctx.reporter
        root = Path(args.path).resolve()
        if not root.is_dir():
            r.fail(f"Not a directory: {root}")
            return 2

        fp = env.fingerprint()
        issues = scan.scan(root)
        ports = {port: env.port_free(port) for port in args.port}
        binaries = []
        for b in args.binary:
            info = elf.read_elf(b)
            problems = elf.compatibility_problems(info, host_libc=fp["libc"]) if info else ["not an ELF binary or unreadable"]
            binaries.append({"path": str(b), "arch": info.arch if info else None,
                             "libc": info.libc if info else None, "problems": problems})

        high = sum(1 for i in issues if i.severity == "high")
        bad = high + sum(1 for ok in ports.values() if not ok) + sum(1 for b in binaries if b["problems"])

        if args.json:
            r.plain(json.dumps({
                "fingerprint": fp,
                "issues": [i.__dict__ for i in issues],
                "ports": ports,
                "binaries": binaries,
            }, indent=2))
            return 1 if bad else 0

        r.heading("Device")
        r.plain(f"{fp['system']} {fp['machine']} · libc {fp['libc']} · python {fp['python']}")
        if fp["termux"]:
            r.plain(f"Termux {fp['termux_version'] or '?'} · Android {fp['android_release'] or '?'} "
                    f"(SDK {fp['android_sdk'] or '?'}) · {fp['device'] or ''}")
            if not fp["shared_storage_linked"]:
                r.warn("Shared storage not linked: run termux-setup-storage")
        r.plain(f"Free space in home: {fp['home_free_gb']} GB")

        r.heading(f"Project scan: {root.name}")
        if not issues:
            r.ok("No issues found")
        for i in issues:
            tag = r.fail if i.severity == "high" else r.warn
            tag(f"{i.severity.upper()} {i.path}: {i.problem}")
            r.plain(f"    fix: {i.fix}")

        if ports:
            r.heading("Ports")
            for port, free in ports.items():
                (r.ok if free else r.fail)(f"port {port} is {'free' if free else 'in use'}")
        if binaries:
            r.heading("Binaries")
            for b in binaries:
                if b["problems"]:
                    r.fail(f"{b['path']}: " + "; ".join(b["problems"]))
                else:
                    r.ok(f"{b['path']}: {b['arch']} / {b['libc']} looks runnable here")

        if args.save:
            out = paths.new_run_dir("doctor", root.name)
            (out / "doctor.md").write_text(
                env.to_markdown(fp) + "\n## Scan\n\n" + scan.issues_markdown(issues), encoding="utf-8")
            (out / "fingerprint.json").write_text(json.dumps(fp, indent=2), encoding="utf-8")
            r.ok(f"Report saved: {out}")

        r.heading("Result")
        (r.fail if bad else r.ok)(f"{bad} blocking problem(s), {len(issues)} total finding(s)")
        return 1 if bad else 0
