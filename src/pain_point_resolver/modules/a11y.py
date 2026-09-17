"""ppr a11y — calibrated, low-glare Termux theme and cursor settings.

What Termux itself supports (so this module only touches these):
  ~/.termux/colors.properties   background, foreground, cursor, color0..color15
  ~/.termux/termux.properties   terminal-cursor-blink-rate (0 = off), terminal-cursor-style
  ~/.termux/font.ttf            the font (swap the file; size is pinch-zoom only)
Termux has no line-height or letter-spacing setting. Those need Termux:X11 with a
desktop terminal; see docs/ACCESSIBILITY_SETUP.md.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from ..core import paths
from ..core.module import Context, Module

# Muted palette on an off-black background: no pure black, no pure white.
BACKGROUND = "#1c1e22"
PALETTE = {
    "color0": "#2a2d33", "color1": "#e0827a", "color2": "#9cc58a", "color3": "#dcc27a",
    "color4": "#8fb0e0", "color5": "#c79ad8", "color6": "#82c4c4", "color7": "#c8c4bc",
    "color8": "#80858f", "color9": "#eb9c95", "color10": "#b3d6a3", "color11": "#e8d49a",
    "color12": "#a9c3ea", "color13": "#d6b3e3", "color14": "#a0d4d4", "color15": "#e6e2da",
}
CURSOR = "#e8d49a"
TERMUX_KEYS = {"terminal-cursor-blink-rate": "0", "terminal-cursor-style": "block"}
MARKER = "# --- added by pain-point-resolver (ppr a11y) ---"


def _channel(c: float) -> float:
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast(a: str, b: str) -> float:
    """WCAG 2.x contrast ratio, 1.0 to 21.0."""
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def foreground_for(background: str, target: float) -> str:
    """Warm off-white whose contrast against background is as close to target as possible."""
    lo, hi = 0.0, 1.0
    best = "#d8d4cc"
    for _ in range(30):
        mid = (lo + hi) / 2
        r, g, b = (round(255 * mid * k) for k in (1.0, 0.985, 0.95))
        candidate = f"#{min(r,255):02x}{min(g,255):02x}{min(b,255):02x}"
        if contrast(candidate, background) < target:
            lo = mid
        else:
            hi, best = mid, candidate
    return best


def colors_properties(target: float) -> str:
    fg = foreground_for(BACKGROUND, target)
    lines = [
        "# Calibrated low-glare theme from pain-point-resolver",
        f"# foreground/background contrast {contrast(fg, BACKGROUND):.1f}:1 (target {target}:1)",
        f"background={BACKGROUND}",
        f"foreground={fg}",
        f"cursor={CURSOR}",
        *[f"{k}={v}" for k, v in PALETTE.items()],
    ]
    return "\n".join(lines) + "\n"


class A11y(Module):
    name = "a11y"
    summary = "Calibrated low-glare Termux colours, steady cursor, contrast checker"
    pain_points = (51, 55, 56, 62)
    status = "partial"
    contract = "human"

    def add_arguments(self, p: argparse.ArgumentParser) -> None:
        sub = p.add_subparsers(dest="action", required=True)
        theme = sub.add_parser("theme", help="show (or --apply) the calibrated Termux theme")
        theme.add_argument("--contrast", type=float, default=7.0,
                           help="foreground contrast target, 4.5 (AA) to 12; default 7.0 (AAA)")
        theme.add_argument("--apply", action="store_true", help="write it to ~/.termux (old file is kept)")
        check = sub.add_parser("check", help="contrast ratio of two hex colours")
        check.add_argument("fg")
        check.add_argument("bg")

    def run(self, args: argparse.Namespace, ctx: Context) -> int:
        r = ctx.reporter
        if args.action == "check":
            ratio = contrast(args.fg, args.bg)
            grade = "AAA" if ratio >= 7 else "AA" if ratio >= 4.5 else "below AA"
            r.plain(f"{args.fg} on {args.bg}: {ratio:.2f}:1 ({grade})")
            return 0

        target = max(4.5, min(args.contrast, 12.0))
        text = colors_properties(target)
        if not args.apply:
            r.plain(text)
            r.plain("Run with --apply to install it (Termux only).")
            return 0
        if not paths.is_termux():
            r.fail("--apply only works inside Termux")
            return 2

        tdir = Path.home() / ".termux"
        tdir.mkdir(exist_ok=True)
        colors = tdir / "colors.properties"
        if colors.exists():
            retired = tdir / f"colors.properties.retired-{paths.timestamp()}"
            colors.rename(retired)
            r.info(f"previous theme kept as {retired.name}")
        colors.write_text(text, encoding="utf-8")
        r.ok("theme written")

        props = tdir / "termux.properties"
        existing = props.read_text(encoding="utf-8") if props.exists() else ""
        present = {line.split("=", 1)[0].strip() for line in existing.splitlines()
                   if "=" in line and not line.lstrip().startswith("#")}
        missing = {k: v for k, v in TERMUX_KEYS.items() if k not in present}
        if missing:
            with props.open("a", encoding="utf-8") as fh:
                fh.write(f"\n{MARKER}\n" + "".join(f"{k} = {v}\n" for k, v in missing.items()))
            r.ok("steady block cursor enabled")
        else:
            r.info("cursor settings already set by you; left unchanged")

        if shutil.which("termux-reload-settings"):
            subprocess.run(["termux-reload-settings"], check=False)
            r.ok("settings reloaded")
        return 0
