import io
import json
import os
import struct
import tempfile
import unittest
from pathlib import Path

from pain_point_resolver.core import elf, env, runner, scan
from pain_point_resolver.core.output import Reporter, clean_line
from pain_point_resolver.core.register import Register
from pain_point_resolver.modules.a11y import BACKGROUND, PALETTE, colors_properties, contrast, foreground_for


def fake_elf(path: Path, machine: int, interp: bytes | None) -> None:
    """Write a minimal 64-bit little-endian ELF with an optional PT_INTERP."""
    phoff, phentsize = 64, 56
    header = bytearray(64)
    header[:4] = b"\x7fELF"
    header[4], header[5] = 2, 1
    struct.pack_into("<H", header, 18, machine)
    struct.pack_into("<Q", header, 32, phoff)
    struct.pack_into("<HH", header, 54, phentsize, 1 if interp else 0)
    body = bytes(header)
    if interp:
        ph = bytearray(phentsize)
        struct.pack_into("<I", ph, 0, 3)
        struct.pack_into("<Q", ph, 8, 64 + phentsize)
        struct.pack_into("<Q", ph, 32, len(interp) + 1)
        body += bytes(ph) + interp + b"\x00"
    path.write_bytes(body)


class OutputTests(unittest.TestCase):
    def test_clean_line_strips_noise(self):
        self.assertEqual(clean_line("\x1b[31mred\x1b[0m"), "red")
        self.assertEqual(clean_line("10%\r50%\r100% done"), "100% done")
        self.assertNotIn("\u2500", clean_line("\u250c\u2500\u2500 box \u2500\u2510"))

    def test_status_words_without_colour(self):
        buf = io.StringIO()
        Reporter(stream=buf).fail("broken")
        self.assertEqual(buf.getvalue(), "[fail] broken\n")

    def test_quiet_still_shows_failures(self):
        buf = io.StringIO()
        r = Reporter(quiet=True, stream=buf)
        r.info("hidden")
        r.warn("shown")
        self.assertEqual(buf.getvalue(), "[warn] shown\n")


class RegisterTests(unittest.TestCase):
    def test_chain_detects_tampering(self):
        with tempfile.TemporaryDirectory() as d:
            reg = Register(Path(d) / "r.jsonl")
            for i in range(3):
                reg.append({"n": i})
            self.assertEqual(reg.verify(), (True, None))
            lines = reg.path.read_text().splitlines()
            entry = json.loads(lines[1])
            entry["n"] = 99
            lines[1] = json.dumps(entry)
            reg.path.write_text("\n".join(lines) + "\n")
            self.assertEqual(reg.verify(), (False, 2))

    def test_deleted_line_detected(self):
        with tempfile.TemporaryDirectory() as d:
            reg = Register(Path(d) / "r.jsonl")
            for i in range(3):
                reg.append({"n": i})
            lines = reg.path.read_text().splitlines()
            reg.path.write_text(lines[0] + "\n" + lines[2] + "\n")
            self.assertFalse(reg.verify()[0])


class ElfTests(unittest.TestCase):
    def test_foreign_arch_and_libc(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "tool"
            fake_elf(p, 0x3E, b"/lib64/ld-linux-x86-64.so.2")
            info = elf.read_elf(p)
            self.assertEqual((info.arch, info.libc), ("x86_64", "glibc"))
            problems = elf.compatibility_problems(info, host_machine="aarch64", host_libc="bionic")
            self.assertEqual(len(problems), 2)

    def test_matching_bionic_binary_is_fine(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "tool"
            fake_elf(p, 0xB7, b"/system/bin/linker64")
            info = elf.read_elf(p)
            self.assertEqual(info.libc, "bionic")
            self.assertEqual(elf.compatibility_problems(info, "aarch64", "bionic"), [])

    def test_non_elf(self):
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"#!/bin/sh\n" * 10)
            f.flush()
            self.assertIsNone(elf.read_elf(Path(f.name)))


class ScanTests(unittest.TestCase):
    def test_detects_planted_faults(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "run.sh").write_bytes(b"#!/bin/bash\necho hi\r\n")
            (root / "main.py").write_text('open("/tmp/x")\ndef f(:\n')
            (root / "cfg.json").write_text('{"a": 1,}')
            fake_elf(root / "tool", 0x28 if os.uname().machine not in ("aarch64", "arm64", "armv7l", "armv8l") else 0x3E,
                     b"/lib/ld-musl-armhf.so.1")
            problems = " | ".join(i.problem for i in scan.scan(root))
            for expected in ("CRLF", "shebang", "Python syntax", "Invalid JSON", "/tmp", "Foreign binary", "README"):
                self.assertIn(expected, problems)

    def test_clean_project(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "README.md").write_text("# ok\n")
            (root / "app.py").write_text("import tempfile\nprint(tempfile.gettempdir())\n")
            self.assertEqual(scan.scan(root), [])


class EnvTests(unittest.TestCase):
    def test_fingerprint_is_json_serialisable(self):
        json.dumps(env.fingerprint(include_tools=False))

    def test_port_probe(self):
        import socket
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            s.listen()
            self.assertFalse(env.port_free(s.getsockname()[1]))


class RunnerTests(unittest.TestCase):
    def test_capture_and_calm(self):
        with tempfile.TemporaryDirectory() as d:
            buf = io.StringIO()
            script = "for i in 1 2 3 4 5; do echo noise $i; done; echo 'Compiling x'; echo 'error: boom'; exit 4"
            res = runner.run_captured(["sh", "-c", script], Path(d) / "log", Reporter(stream=buf), calm=True, min_interval=0)
            self.assertEqual(res.returncode, 4)
            self.assertEqual(res.lines, 7)
            shown = buf.getvalue()
            self.assertIn("Compiling x", shown)
            self.assertIn("error: boom", shown)
            self.assertNotIn("noise", shown)
            self.assertIn("noise 3", (Path(d) / "log").read_text())

    def test_missing_command(self):
        with tempfile.TemporaryDirectory() as d:
            res = runner.run_captured(["no-such-cmd-xyz"], Path(d) / "log", Reporter(stream=io.StringIO()))
            self.assertEqual(res.returncode, 127)

    def test_calm_env(self):
        e = runner.calm_environment({"FORCE_COLOR": "1"})
        self.assertNotIn("FORCE_COLOR", e)
        self.assertEqual(e["NO_COLOR"], "1")


class A11yTests(unittest.TestCase):
    def test_palette_contrast(self):
        for key, value in PALETTE.items():
            floor = 1.0 if key == "color0" else 4.5
            self.assertGreaterEqual(contrast(value, BACKGROUND), floor, key)

    def test_foreground_hits_target_without_pure_white(self):
        for target in (4.5, 7.0, 10.0):
            fg = foreground_for(BACKGROUND, target)
            self.assertGreaterEqual(contrast(fg, BACKGROUND), target)
            self.assertLess(contrast(fg, BACKGROUND), target + 0.5)
            self.assertNotEqual(fg.lower(), "#ffffff")
        self.assertIn("background=#1c1e22", colors_properties(7.0))


if __name__ == "__main__":
    unittest.main()
