"""ppr register — show and verify the append-only registers."""
from __future__ import annotations

import argparse

from ..core import paths
from ..core.module import Context, Module
from ..core.register import Register

REGISTERS = ("errors.jsonl", "builds.jsonl")


class RegisterTool(Module):
    name = "register"
    summary = "Show recent entries and verify the hash chain of the append-only registers"
    pain_points = (29, 49)
    status = "working"
    contract = "observability"

    def add_arguments(self, p: argparse.ArgumentParser) -> None:
        p.add_argument("action", choices=("verify", "show"))
        p.add_argument("--which", choices=("errors", "builds"), default="errors")
        p.add_argument("--project", help="only entries for this project")
        p.add_argument("-n", type=int, default=10, help="entries to show")

    def run(self, args: argparse.Namespace, ctx: Context) -> int:
        r = ctx.reporter
        root = paths.output_root()
        if args.action == "verify":
            bad = 0
            for name in REGISTERS:
                reg = Register(root / name)
                if not reg.path.exists():
                    r.info(f"{name}: not created yet")
                    continue
                intact, seq = reg.verify()
                if intact:
                    r.ok(f"{name}: chain intact")
                else:
                    bad += 1
                    r.fail(f"{name}: chain broken at entry #{seq} (edited or deleted line)")
            return 1 if bad else 0

        reg = Register(root / f"{args.which}.jsonl")
        match = {"project": args.project} if args.project else {}
        entries = reg.tail(args.n, **match)
        if not entries:
            r.info("no entries")
        for e in entries:
            extra = f"exit {e['exit']} · {e['cmd']} · {', '.join(e['findings']) or 'unmatched'}" \
                if args.which == "errors" else f"{e.get('kind')} · {e.get('findings')} finding(s) · {e.get('folder')}"
            r.plain(f"#{e['seq']} {e['ts']} {e.get('project', '')} · {extra}")
        return 0
