"""Module registry. Adding a command = one import and one list entry."""
from __future__ import annotations

from .a11y import A11y
from .docs import Docs
from .doctor import Doctor
from .hunt import Calm, Hunt
from .planned import PLANNED
from .register import RegisterTool

MODULES = [Doctor, Docs, Hunt, Calm, A11y, RegisterTool, *PLANNED]
