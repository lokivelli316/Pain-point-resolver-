"""Where things live, on Termux and on regular Linux/macOS."""
from __future__ import annotations

import os
from pathlib import Path

TERMUX_PREFIX = "/data/data/com.termux/files/usr"


class StorageNotLinked(RuntimeError):
    """Termux shared storage has not been linked with termux-setup-storage."""


def is_termux() -> bool:
    return "TERMUX_VERSION" in os.environ or Path(TERMUX_PREFIX).is_dir()


def prefix() -> Path:
    default = TERMUX_PREFIX if is_termux() else "/usr"
    return Path(os.environ.get("PREFIX", default))


def tmp_dir() -> Path:
    raw = os.environ.get("TMPDIR") or (str(prefix() / "tmp") if is_termux() else "/tmp")
    path = Path(raw)
    path.mkdir(parents=True, exist_ok=True)
    return path


def config_dir() -> Path:
    base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "ppr"


def output_root() -> Path:
    """Reports go to Android Downloads on Termux, the XDG data dir elsewhere. PPR_OUT overrides."""
    override = os.environ.get("PPR_OUT")
    if override:
        return Path(override).expanduser()
    if is_termux():
        return Path.home() / "storage" / "downloads" / "PainPointResolver"
    base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / "pain-point-resolver"


def ensure_output_root() -> Path:
    root = output_root()
    downloads = Path.home() / "storage" / "downloads"
    if is_termux() and not os.environ.get("PPR_OUT") and not downloads.exists():
        raise StorageNotLinked("Shared storage is not linked. Run: termux-setup-storage  (then tap Allow)")
    root.mkdir(parents=True, exist_ok=True)
    return root


def on_shared_storage(path: Path) -> bool:
    resolved = str(Path(path).resolve())
    return resolved.startswith(("/storage/", "/sdcard/", "/mnt/sdcard/"))


def timestamp() -> str:
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d_%H%M%S")


def new_run_dir(*parts: str) -> Path:
    """Create a fresh, never-reused folder under the output root (upgrade-only: nothing is overwritten)."""
    base = ensure_output_root().joinpath(*parts)
    base.mkdir(parents=True, exist_ok=True)
    stamp = timestamp()
    candidate = base / stamp
    n = 2
    while candidate.exists():
        candidate = base / f"{stamp}-{n}"
        n += 1
    candidate.mkdir()
    return candidate
