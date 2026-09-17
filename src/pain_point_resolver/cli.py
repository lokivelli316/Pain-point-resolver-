"""ppr — Pain Point Resolver command line."""
from __future__ import annotations

import argparse
import sys

from . import __version__
from .core import paths
from .core.module import CONTRACTS, Context, load_config, pain_points
from .core.output import Reporter
from .modules import MODULES


def build_parser() -> tuple[argparse.ArgumentParser, dict]:
    parser = argparse.ArgumentParser(
        prog="ppr",
        description="Pain Point Resolver: turn recurring developer pain into pre-flight checks.",
    )
    parser.add_argument("--version", action="version", version=f"ppr {__version__}")
    parser.add_argument("-q", "--quiet", action="store_true", help="only warnings, failures and results")
    parser.add_argument("--no-color", action="store_true", help="never use colour (NO_COLOR is also honoured)")
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    instances = {}
    for cls in MODULES:
        mod = cls()
        instances[mod.name] = mod
        mp = sub.add_parser(mod.name, help=mod.summary, description=mod.summary)
        mod.add_arguments(mp)

    mods = sub.add_parser("modules", help="list commands, their status and the pain points they cover")
    mods.add_argument("--contract", choices=CONTRACTS)
    pain = sub.add_parser("pain", help="browse the 62-point pain map")
    pain.add_argument("id", nargs="?", type=int)
    pain.add_argument("--status", choices=("open", "partial", "resolved"))
    return parser, instances


def list_modules(r: Reporter, contract: str | None) -> int:
    for cls in MODULES:
        m = cls()
        if contract and m.contract != contract:
            continue
        r.plain(f"{m.name:<12} {m.status:<8} {m.contract:<13} pain {','.join(map(str, m.pain_points))}")
        r.plain(f"{'':<12} {m.summary}")
    return 0


def show_pain(r: Reporter, pid: int | None, status: str | None) -> int:
    table = pain_points()
    if pid is not None:
        p = table.get(pid)
        if not p:
            r.fail(f"No pain point #{pid} (valid: 1-{max(table)})")
            return 2
        r.plain(f"#{p['id']} {p['title']}")
        r.plain(f"group: {p['group']} · contract: {p['contract']} · status: {p['status']}")
        r.plain(f"modules: {', '.join(p['modules']) or 'none yet (open for contributors)'}")
        if p.get("note"):
            r.plain(f"note: {p['note']}")
        return 0
    counts: dict[str, int] = {}
    for p in table.values():
        counts[p["status"]] = counts.get(p["status"], 0) + 1
        if status and p["status"] != status:
            continue
        r.plain(f"#{p['id']:<3} {p['status']:<8} {p['title']}")
    r.plain("")
    r.plain(" · ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return _main(argv)
    except BrokenPipeError:  # e.g. `ppr pain | head`
        import os
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return 0


def _main(argv: list[str] | None) -> int:
    parser, instances = build_parser()
    args = parser.parse_args(argv)
    reporter = Reporter(quiet=args.quiet, no_color=args.no_color)
    if not args.command:
        parser.print_help()
        return 0
    if args.command == "modules":
        return list_modules(reporter, args.contract)
    if args.command == "pain":
        return show_pain(reporter, args.id, args.status)
    ctx = Context(reporter=reporter, config=load_config())
    try:
        return instances[args.command].run(args, ctx)
    except paths.StorageNotLinked as exc:
        reporter.fail(str(exc))
        return 2
    except KeyboardInterrupt:
        reporter.warn("stopped")
        return 130


if __name__ == "__main__":
    sys.exit(main())
