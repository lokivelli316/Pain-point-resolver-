"""Minimal ELF header reader (stdlib only).

Answers the two questions behind 'Illegal instruction' and 'required file not
found' on foreign binaries (pain points #30, #35): what CPU was this built for,
and which dynamic loader (glibc / musl / bionic) does it expect?
"""
from __future__ import annotations

import platform
import struct
from dataclasses import dataclass
from pathlib import Path

MACHINES = {0x03: "x86", 0x28: "arm", 0x3E: "x86_64", 0xB7: "aarch64", 0xF3: "riscv64"}

# Host machine name (platform.machine()) -> ELF arches it can execute natively.
COMPATIBLE = {
    "aarch64": {"aarch64", "arm"},
    "arm64": {"aarch64", "arm"},
    "armv8l": {"arm"},
    "armv7l": {"arm"},
    "x86_64": {"x86_64", "x86"},
    "amd64": {"x86_64", "x86"},
    "i686": {"x86"},
    "i386": {"x86"},
    "riscv64": {"riscv64"},
}


@dataclass
class ElfInfo:
    arch: str
    bits: int
    interpreter: str | None

    @property
    def libc(self) -> str:
        interp = self.interpreter or ""
        if not interp:
            return "static-or-library"
        if "ld-musl" in interp:
            return "musl"
        if "/system/bin/linker" in interp:
            return "bionic"
        if "ld-linux" in interp or "ld64.so" in interp:
            return "glibc"
        return f"unknown ({interp})"


def is_elf(path: Path) -> bool:
    try:
        with open(path, "rb") as fh:
            return fh.read(4) == b"\x7fELF"
    except OSError:
        return False


def read_elf(path: Path) -> ElfInfo | None:
    try:
        with open(path, "rb") as fh:
            head = fh.read(64)
            if len(head) < 52 or head[:4] != b"\x7fELF":
                return None
            bits = 64 if head[4] == 2 else 32
            end = "<" if head[5] == 1 else ">"
            machine = struct.unpack_from(end + "H", head, 18)[0]
            if bits == 64:
                phoff = struct.unpack_from(end + "Q", head, 32)[0]
                phentsize, phnum = struct.unpack_from(end + "HH", head, 54)
            else:
                phoff = struct.unpack_from(end + "I", head, 28)[0]
                phentsize, phnum = struct.unpack_from(end + "HH", head, 42)
            interpreter = None
            for i in range(min(phnum, 64)):
                fh.seek(phoff + i * phentsize)
                ph = fh.read(phentsize)
                if len(ph) < 20:
                    break
                if struct.unpack_from(end + "I", ph, 0)[0] != 3:  # PT_INTERP
                    continue
                if bits == 64:
                    offset = struct.unpack_from(end + "Q", ph, 8)[0]
                    size = struct.unpack_from(end + "Q", ph, 32)[0]
                else:
                    offset = struct.unpack_from(end + "I", ph, 4)[0]
                    size = struct.unpack_from(end + "I", ph, 16)[0]
                fh.seek(offset)
                interpreter = fh.read(min(size, 256)).split(b"\x00")[0].decode("utf-8", "replace")
                break
    except (OSError, struct.error):
        return None
    return ElfInfo(MACHINES.get(machine, f"unknown(0x{machine:x})"), bits, interpreter)


def compatibility_problems(info: ElfInfo, host_machine: str | None = None, host_libc: str | None = None) -> list[str]:
    """Human-readable reasons this binary will not run here. Empty list = looks runnable."""
    problems = []
    host = (host_machine or platform.machine()).lower()
    allowed = COMPATIBLE.get(host, {host})
    if info.arch not in allowed:
        problems.append(f"built for {info.arch}, this device is {host}")
    if host_libc and info.libc in {"glibc", "musl", "bionic"} and info.libc != host_libc:
        problems.append(f"expects {info.libc} loader ({info.interpreter}), this system uses {host_libc}")
    return problems
