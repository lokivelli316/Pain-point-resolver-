"""Environment fingerprint (Environment contract: pain points #1, #6, #7, #11, #12, #35).

The fingerprint is plain data (a dict) so it can be diffed between machines,
embedded in reports, and later compared against an artifact manifest.
"""
from __future__ import annotations

import os
import platform
import shutil
import socket
import subprocess
from pathlib import Path

from . import paths

TOOLS = ("bash", "python", "pip", "node", "npm", "git", "clang", "make", "cmake",
         "rustc", "cargo", "go", "java", "tmux", "shellcheck", "proot-distro")


def _run(cmd: list[str], timeout: float = 3.0) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (out.stdout or out.stderr).strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def getprop(key: str) -> str:
    return _run(["getprop", key]) if shutil.which("getprop") else ""


def detect_libc() -> str:
    if paths.is_termux() or getprop("ro.build.version.sdk"):
        return "bionic"
    name, version = platform.libc_ver()
    if name:
        return "glibc" if name == "glibc" else name
    if any(Path("/lib").glob("ld-musl-*")):
        return "musl"
    return platform.system().lower()


def cpu_features() -> list[str]:
    try:
        text = Path("/proc/cpuinfo").read_text(errors="replace")
    except OSError:
        return []
    for line in text.splitlines():
        key, _, value = line.partition(":")
        if key.strip().lower() in {"features", "flags"}:
            return sorted(set(value.split()))
    return []


def tool_version(name: str) -> str | None:
    if not shutil.which(name):
        return None
    if name == "proot-distro":
        return "installed"
    cmd = {"go": ["go", "version"], "java": ["java", "-version"]}.get(name, [name, "--version"])
    out = _run(cmd)
    return out.splitlines()[0] if out else "installed"


def port_free(port: int, host: str = "127.0.0.1") -> bool:
    """Try to bind. Works without root on Android, where `ss -ltnp` is restricted."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
        except OSError:
            return False
    return True


def fingerprint(include_tools: bool = True) -> dict:
    home = Path.home()
    usage = shutil.disk_usage(home)
    data = {
        "system": platform.system(),
        "machine": platform.machine(),
        "kernel": platform.release(),
        "python": platform.python_version(),
        "libc": detect_libc(),
        "termux": paths.is_termux(),
        "termux_version": os.environ.get("TERMUX_VERSION"),
        "android_release": getprop("ro.build.version.release") or None,
        "android_sdk": getprop("ro.build.version.sdk") or None,
        "android_abi": getprop("ro.product.cpu.abi") or None,
        "device": " ".join(filter(None, [getprop("ro.product.manufacturer"), getprop("ro.product.model")])) or None,
        "prefix": str(paths.prefix()),
        "tmpdir": os.environ.get("TMPDIR"),
        "home_free_gb": round(usage.free / 1e9, 1),
        "shared_storage_linked": (home / "storage" / "downloads").exists() if paths.is_termux() else None,
        "cpu_features": cpu_features(),
    }
    if include_tools:
        data["tools"] = {t: tool_version(t) for t in TOOLS}
    return data


def to_markdown(fp: dict) -> str:
    lines = ["## Environment fingerprint", ""]
    for key, value in fp.items():
        if key in {"tools", "cpu_features"}:
            continue
        if value not in (None, ""):
            lines.append(f"- {key}: `{value}`")
    feats = fp.get("cpu_features") or []
    if feats:
        shown = " ".join(feats[:40]) + (" ..." if len(feats) > 40 else "")
        lines.append(f"- cpu_features ({len(feats)}): `{shown}`")
    tools = fp.get("tools") or {}
    if tools:
        lines += ["", "### Toolchain"]
        present = {k: v for k, v in tools.items() if v}
        for name, ver in present.items():
            lines.append(f"- {name}: {ver}")
        missing = [k for k, v in tools.items() if not v]
        if missing:
            lines.append(f"- not installed: {', '.join(missing)}")
    return "\n".join(lines) + "\n"
