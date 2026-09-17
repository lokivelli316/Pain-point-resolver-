"""Append-only, hash-chained register.

Each JSON line carries the hash of the line before it, so any edit or deletion
is detectable with `ppr register verify`. Nothing in this project rewrites a
register; a correction is a new entry that references the old sequence number.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

GENESIS = "0" * 64


def _digest(entry: dict) -> str:
    body = {k: v for k, v in entry.items() if k != "hash"}
    blob = json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


class Register:
    def __init__(self, path: Path):
        self.path = Path(path)

    def entries(self) -> Iterator[dict]:
        if not self.path.exists():
            return
        with self.path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    yield json.loads(line)

    def tail(self, n: int = 5, **match: str) -> list[dict]:
        hits = [e for e in self.entries() if all(e.get(k) == v for k, v in match.items())]
        return hits[-n:]

    def _last(self) -> dict | None:
        last = None
        for last in self.entries():
            pass
        return last

    def append(self, record: dict) -> dict:
        last = self._last()
        entry = {
            "seq": (last["seq"] + 1) if last else 1,
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            **record,
            "prev": last["hash"] if last else GENESIS,
        }
        entry["hash"] = _digest(entry)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry

    def verify(self) -> tuple[bool, int | None]:
        """Return (True, None) if the chain is intact, else (False, first_bad_seq)."""
        prev, expected = GENESIS, 1
        try:
            for entry in self.entries():
                if (
                    entry.get("seq") != expected
                    or entry.get("prev") != prev
                    or _digest(entry) != entry.get("hash")
                ):
                    return False, expected
                prev, expected = entry["hash"], expected + 1
        except json.JSONDecodeError:
            return False, expected
        return True, None
