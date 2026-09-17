#!/usr/bin/env sh
# Pain Point Resolver installer. Run from the repo root:  sh install.sh
set -eu

say() { printf '[install] %s\n' "$*"; }

if [ -n "${TERMUX_VERSION:-}" ] || [ -d /data/data/com.termux/files/usr ]; then
  say "Termux detected"
  command -v python >/dev/null 2>&1 || pkg install -y python
  command -v git >/dev/null 2>&1 || pkg install -y git
  pip install --upgrade .
  if [ ! -d "$HOME/storage/downloads" ]; then
    say "Linking shared storage so reports can reach your Download folder. Tap Allow."
    termux-setup-storage || say "Skipped. Run termux-setup-storage later."
  fi
elif command -v pipx >/dev/null 2>&1; then
  say "Installing with pipx"
  pipx install --force .
else
  venv="${XDG_DATA_HOME:-$HOME/.local/share}/ppr-venv"
  say "Installing into a private virtual environment: $venv"
  python3 -m venv "$venv"
  "$venv/bin/pip" install --upgrade .
  mkdir -p "$HOME/.local/bin"
  ln -sf "$venv/bin/ppr" "$HOME/.local/bin/ppr"
  case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) say "Add ~/.local/bin to your PATH." ;; esac
fi

say "Done. Try: ppr doctor"
