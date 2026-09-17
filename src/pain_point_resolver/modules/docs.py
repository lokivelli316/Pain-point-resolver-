"""ppr docs — install / running / troubleshooting manuals plus an AI handoff, per build."""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from .. import __version__
from ..core import env, paths, patterns, scan
from ..core.module import Context, Module
from ..core.register import Register
from ..core.stack import Stack, detect
from .hunt import ERRORS_FILE

TERMUX_CONSTRAINTS = """\
- No root, no sudo, no systemd, no Docker. The package manager is `pkg` (an apt wrapper).
- Android's bionic libc, not glibc: prebuilt Linux binaries often fail. Prefer `pkg install`, fall back to `proot-distro`.
- No `/tmp`, `/bin` or `/usr`. Use `$PREFIX` (`/data/data/com.termux/files/usr`) and `$TMPDIR`.
- Shared storage (`~/storage/*`, `/sdcard`) has no exec bits and no symlinks. Code lives in `$HOME`.
- Android may kill background processes (low memory, phantom process killer on Android 12+).
- Compiled Python packages: check `pkg search python-<name>` before pip builds from source.
"""


def _code(lines: list[str]) -> str:
    return "```bash\n" + "\n".join(lines) + "\n```\n"


def _stamp() -> str:
    return f"_Pain Point Resolver {__version__} · {datetime.now():%Y-%m-%d %H:%M}_\n"


def install_manual(st: Stack) -> str:
    get = [f"cd ~ && git clone {st.remote} && cd {st.name}"] if st.remote else [f"cp -r '/path/to/{st.name}' ~/ && cd ~/{st.name}"]
    body = [
        f"# {st.name}: Installation Manual", _stamp(),
        f"**Detected stack:** {', '.join(st.languages) or 'none detected'}",
        f"**Repository:** {st.remote}\n" if st.remote else "",
        "## 1. Termux prerequisites",
        "- Install Termux from **F-Droid** or **GitHub releases**. Keep add-ons (Termux:API, Termux:Boot) from the same source.",
        "- Link storage once: `termux-setup-storage`",
        "- Keep projects in `$HOME`, not Downloads.\n",
        "## 2. System packages", _code(["pkg update && pkg upgrade -y", f"pkg install -y {' '.join(st.packages)}"]),
        "## 3. Get the project", _code(get),
        "## 4. Project dependencies",
        _code([f"cd ~/{st.name}", *(st.install or ["# no dependency manifest detected: add steps here"])]),
    ]
    if st.notes:
        body += ["### Notes", *[f"- {n}" for n in st.notes], ""]
    body += ["## 5. Verify", _code([f"ppr doctor ~/{st.name}"]),
             "A clean run ends with **0 blocking problem(s)**. Anything else is in TROUBLESHOOTING.md.\n"]
    return "\n".join(body)


def running_manual(st: Stack) -> str:
    return "\n".join([
        f"# {st.name}: Running Manual", _stamp(),
        "## Start", _code([f"cd ~/{st.name}", *(st.run or ["# no entrypoint detected: add the start command here"])]),
        "## Start with diagnosis and calm output",
        _code(["ppr hunt -- <start command>        # full output, failures diagnosed",
               "ppr calm -- <build command>        # low-motion output, full log on disk",
               'ppr hunt -- bash -c "a && b"      # chained commands']),
        "## Keep it alive",
        "- `termux-wake-lock` stops Android sleeping Termux; `termux-wake-unlock` releases it.",
        f"- Background with a log: `nohup <cmd> > ~/{st.name}.log 2>&1 &`",
        f"- Detachable session: `pkg install tmux`, `tmux new -s {st.name}`, run, then Ctrl-b d. Back: `tmux attach -t {st.name}`",
        "- Start on boot: Termux:Boot add-on, script in `~/.termux/boot/`.\n",
        "## Stop",
        "- Foreground: Ctrl-C (Volume-Down acts as Ctrl on the Termux keyboard).",
        '- Background: `pkill -f "<cmd>"`\n',
    ])


def troubleshooting(st: Stack, issues: list[scan.Issue], past: list[dict]) -> str:
    body = [
        f"# {st.name}: Troubleshooting", _stamp(),
        "## How to use",
        "1. Rerun the failing command as `ppr hunt -- <cmd>`.",
        "2. The report is saved and the failure is added to the error register.",
        "3. Rebuild these docs with `ppr docs` and it appears below.\n",
        f"## Static scan: {len(issues)} finding(s)", scan.issues_markdown(issues),
        "## Recorded failures for this project",
    ]
    if past:
        for e in past:
            body.append(f"- #{e['seq']} {e['ts']} · exit {e['exit']} · `{e['cmd']}` · findings: {', '.join(e['findings']) or 'none matched'} · `{e['report']}`")
    else:
        body.append("- None recorded yet.")
    body += ["", "## Known failure patterns", "| id | diagnosis | fix | confidence |", "|---|---|---|---|"]
    for pat in patterns.load_patterns():
        fix = pat.fix.replace("|", "\\|")
        body.append(f"| `{pat.id}` | {pat.diagnosis} | `{fix}` | {pat.confidence} |")
    return "\n".join(body) + "\n"


def handoff(st: Stack, fp: dict, issues: list[scan.Issue], past: list[dict]) -> str:
    tree = []
    for dirpath, dirnames, filenames in os.walk(st.root):
        rel = Path(dirpath).relative_to(st.root)
        depth = len(rel.parts)
        dirnames[:] = sorted(d for d in dirnames if d not in scan.SKIP_DIRS and not d.startswith("."))
        if depth >= 3:
            dirnames[:] = []
        for name in sorted(filenames):
            if not name.startswith("."):
                tree.append(str(rel / name))
        if len(tree) > 150:
            tree.append("... (truncated)")
            break
    rules = st.root / ".ppr" / "RULES.md"
    readme = next((st.root / n for n in ("README.md", "README", "readme.md") if (st.root / n).is_file()), None)
    body = [
        f"# AI handoff: {st.name}",
        "> Paste this whole file into a new AI session before asking for help with this project.",
        _stamp(),
        "## Environment constraints (Termux on Android)" if fp.get("termux") else "## Environment",
        TERMUX_CONSTRAINTS if fp.get("termux") else "",
        env.to_markdown(fp),
        "## Project",
        f"- Path: `{st.root}`",
        f"- Remote: {st.remote or 'none'}",
        f"- Stack: {', '.join(st.languages) or 'none detected'}",
        f"- System packages: {' '.join(st.packages)}",
        f"- Install: {' ; '.join(st.install) or 'none detected'}",
        f"- Run: {' ; '.join(st.run) or 'none detected'}",
        *[f"- Note: {n}" for n in st.notes],
        "", "## Files (depth 3)", "```", *tree, "```", "",
        f"## Open findings ({len(issues)})", scan.issues_markdown(issues),
        "## Recent failures",
        *([f"- `{e['cmd']}` exit {e['exit']}: {', '.join(e['findings']) or 'unmatched'}\n  last lines: `{' / '.join(e.get('tail', [])[-3:])}`" for e in past] or ["- None recorded."]),
        "", "## Project rules for any AI or human helper",
        rules.read_text(encoding="utf-8") if rules.is_file() else
        "- None pinned. Put rules every helper must follow in `.ppr/RULES.md`.",
    ]
    if readme:
        lines = readme.read_text(encoding="utf-8", errors="replace").splitlines()[:40]
        body += ["", "## README (first 40 lines)", "````", *lines, "````"]
    return "\n".join(body) + "\n"


class Docs(Module):
    name = "docs"
    summary = "Write install, running and troubleshooting manuals plus an AI handoff to the output folder"
    pain_points = (2, 4, 5, 48, 60)
    status = "partial"
    contract = "human"

    def add_arguments(self, p: argparse.ArgumentParser) -> None:
        p.add_argument("path", nargs="?", default=".", help="project directory (default: current)")

    def run(self, args: argparse.Namespace, ctx: Context) -> int:
        r = ctx.reporter
        root = Path(args.path).resolve()
        if not root.is_dir():
            r.fail(f"Not a directory: {root}")
            return 2
        try:
            out_root = paths.ensure_output_root()
        except paths.StorageNotLinked as exc:
            r.fail(str(exc))
            return 2
        st = detect(root)
        r.step(f"project {st.name}: {', '.join(st.languages) or 'no stack detected'}")
        issues = scan.scan(root)
        r.step(f"static scan: {len(issues)} finding(s)")
        fp = env.fingerprint()
        past = Register(out_root / ERRORS_FILE).tail(5, project=st.name)

        out = paths.new_run_dir("docs", st.name)
        files = {
            "INSTALL.md": install_manual(st),
            "RUNNING.md": running_manual(st),
            "TROUBLESHOOTING.md": troubleshooting(st, issues, past),
            "AI_HANDOFF.md": handoff(st, fp, issues, past),
        }
        index = [f"# {st.name}: document pack", _stamp(), "| File | Use it for |", "|---|---|",
                 "| INSTALL.md | Fresh install on a clean device |",
                 "| RUNNING.md | Start, background, stop |",
                 "| TROUBLESHOOTING.md | Findings, past failures, known fixes |",
                 "| AI_HANDOFF.md | Paste into any AI session for full context |",
                 "| fingerprint.json | Machine-readable environment snapshot |", "",
                 f"- Static scan: **{len(issues)}** finding(s)", f"- Source: `{root}`"]
        files["00_START_HERE.md"] = "\n".join(index) + "\n"
        for name, text in files.items():
            (out / name).write_text(text, encoding="utf-8")
        (out / "fingerprint.json").write_text(json.dumps(fp, indent=2), encoding="utf-8")

        Register(out_root / "builds.jsonl").append({
            "kind": "docs", "project": st.name, "findings": len(issues),
            "folder": str(out.relative_to(out_root)),
        })
        r.ok(f"written to {out}")
        return 0
