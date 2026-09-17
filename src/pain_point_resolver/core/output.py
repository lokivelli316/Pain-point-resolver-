"""Accessible output layer.

Every module prints through Reporter. The rules (full text in ACCESSIBILITY.md):
  * status is carried by words ([ok] [warn] [fail]), never by colour alone
  * no spinners, progress bars, box drawing or cursor tricks
  * colour is off when NO_COLOR is set, TERM=dumb, output is not a tty, or --no-color
  * one complete line at a time, so screen readers and tired eyes can follow
"""
from __future__ import annotations

import os
import re
import sys
from typing import TextIO

ANSI_RE = re.compile(
    r"\x1b\[[0-9;?]*[ -/]*[@-~]"          # CSI: colours, cursor moves, clears
    r"|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)"  # OSC: titles, hyperlinks
    r"|\x1b[()][A-Za-z0-9]"                # charset switches
)
# Box drawing, block elements, geometric shapes, braille spinners, hourglasses.
DECOR_RE = re.compile("[\u2500-\u25FF\u2800-\u28FF\u231B\u23F3]")
MULTISPACE_RE = re.compile(r"[ \t]{3,}")


def clean_line(text: str, collapse: bool = False) -> str:
    """Strip colour codes, carriage-return overwrites and decorative glyphs.

    collapse=True also squeezes long runs of spaces left behind by removed box drawing.
    """
    if "\r" in text:
        parts = [p for p in text.split("\r") if p.strip()]
        text = parts[-1] if parts else ""
    text = ANSI_RE.sub("", text)
    text = DECOR_RE.sub(" ", text)
    if collapse:
        text = MULTISPACE_RE.sub("  ", text)
    return text.rstrip()


def color_allowed(stream: TextIO, forced_off: bool = False) -> bool:
    if forced_off or os.environ.get("NO_COLOR") or os.environ.get("TERM") == "dumb":
        return False
    return bool(getattr(stream, "isatty", lambda: False)())


class Reporter:
    COLORS = {"ok": "32", "warn": "33", "fail": "31", "step": "36"}

    def __init__(self, quiet: bool = False, no_color: bool = False, stream: TextIO | None = None):
        self.stream = stream or sys.stdout
        self.quiet = quiet
        self.color = color_allowed(self.stream, no_color)

    def _emit(self, tag: str, message: str, force: bool = False) -> None:
        if self.quiet and not force:
            return
        label = f"[{tag}]"
        if self.color and tag in self.COLORS:
            label = f"\x1b[{self.COLORS[tag]}m{label}\x1b[0m"
        print(f"{label} {clean_line(message)}", file=self.stream, flush=True)

    def info(self, message: str) -> None:
        self._emit("info", message)

    def step(self, message: str) -> None:
        self._emit("step", message)

    def ok(self, message: str) -> None:
        self._emit("ok", message)

    def warn(self, message: str) -> None:
        self._emit("warn", message, force=True)

    def fail(self, message: str) -> None:
        self._emit("fail", message, force=True)

    def plain(self, message: str = "") -> None:
        """Always printed: results the user asked for."""
        print(clean_line(message), file=self.stream, flush=True)

    def heading(self, message: str) -> None:
        if not self.quiet:
            print(f"\n== {clean_line(message)} ==", file=self.stream, flush=True)
