"""Project stack detection: what is this project, how is it installed and run."""
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

HEAVY_PY = re.compile(
    r"^(numpy|scipy|pandas|matplotlib|cryptography|pillow|lxml|grpcio|opencv[-a-z]*|torch|"
    r"psutil|pyzmq|tiktoken|pydantic[-_]core|orjson)\b",
    re.IGNORECASE | re.MULTILINE,
)
NATIVE_NODE = ("node-gyp", "bcrypt", "sqlite3", "sharp", "canvas", "better-sqlite3")
PY_ENTRIES = ("main.py", "app.py", "server.py", "run.py", "manage.py", "bot.py", "cli.py")


@dataclass
class Stack:
    root: Path
    name: str
    remote: str = ""
    languages: list[str] = field(default_factory=list)
    packages: list[str] = field(default_factory=lambda: ["git"])
    install: list[str] = field(default_factory=list)
    run: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def need(self, *pkgs: str) -> None:
        for pkg in pkgs:
            if pkg not in self.packages:
                self.packages.append(pkg)


def _git(root: Path, *args: str) -> str:
    try:
        out = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, timeout=5)
        return out.stdout.strip() if out.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def project_name(path: Path) -> str:
    top = _git(path, "rev-parse", "--show-toplevel")
    return Path(top).name if top else Path(path).resolve().name


def detect(root: Path) -> Stack:
    root = Path(root).resolve()
    st = Stack(root=root, name=project_name(root), remote=_git(root, "remote", "get-url", "origin"))

    pkg_json = root / "package.json"
    if pkg_json.is_file():
        st.languages.append("Node.js")
        st.need("nodejs")
        st.install.append("npm ci" if (root / "package-lock.json").exists() else "npm install")
        try:
            data = json.loads(pkg_json.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = {}
            st.notes.append("package.json could not be parsed — see the static scan.")
        for script, command in (data.get("scripts") or {}).items():
            st.run.append(f"npm run {script}   # {command}")
        deps = {**(data.get("dependencies") or {}), **(data.get("devDependencies") or {})}
        if any(name in deps for name in NATIVE_NODE):
            st.need("build-essential", "python")
            st.notes.append("Native Node modules present. If the build fails on Android: "
                            "mkdir -p ~/.gyp && echo \"{'variables':{'android_ndk_path':''}}\" > ~/.gyp/include.gypi")

    req = root / "requirements.txt"
    if req.is_file() or (root / "pyproject.toml").is_file() or (root / "setup.py").is_file():
        st.languages.append("Python")
        st.need("python")
        if req.is_file():
            st.install.append("pip install -r requirements.txt")
            heavy = sorted({m.lower() for m in HEAVY_PY.findall(req.read_text(errors="replace"))})
            if heavy:
                st.need("build-essential", "binutils")
                st.notes.append(f"Compiled Python deps: {', '.join(heavy)}. Try `pkg search python-<name>` "
                                "for a prebuilt Termux package first. Rust-based ones need `pkg install rust`.")
        if (root / "pyproject.toml").is_file() or (root / "setup.py").is_file():
            st.install.append("pip install -e .")
        st.run += [f"python {f}" for f in PY_ENTRIES if (root / f).is_file()]

    if (root / "Cargo.toml").is_file():
        st.languages.append("Rust"); st.need("rust")
        st.install.append("cargo build --release"); st.run.append("cargo run --release")
    if (root / "go.mod").is_file():
        st.languages.append("Go"); st.need("golang")
        st.install.append("go build ./..."); st.run.append("go run .")
    if (root / "CMakeLists.txt").is_file():
        st.languages.append("CMake"); st.need("cmake", "clang", "make")
        st.install.append("cmake -B build && cmake --build build -j2")
    if (root / "Makefile").is_file():
        st.languages.append("Make"); st.need("make", "clang")
        st.install.append("make -j2")
    if (root / ".env.example").is_file() and not (root / ".env").exists():
        st.install.append("cp .env.example .env   # then fill in the values")
    if (root / "Dockerfile").is_file():
        st.notes.append("Dockerfile present. Docker does not run in Termux (no root): use proot-distro "
                        "or follow the Dockerfile steps by hand.")

    scripts = sorted(root.glob("*.sh"))
    if scripts:
        st.languages.append("Shell")
    for script in scripts:
        target = st.install if script.name.startswith(("install", "setup", "bootstrap")) else st.run
        target.append(f"bash {script.name}")
    return st
