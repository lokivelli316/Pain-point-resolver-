"""Regenerate docs/PAIN_POINTS.md from data/pain_points.json.  Usage: python scripts/gen_pain_points_md.py [--check]"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src/pain_point_resolver/data/pain_points.json"
DST = ROOT / "docs/PAIN_POINTS.md"


def render() -> str:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    items = data["pain_points"]
    counts = {}
    for p in items:
        counts[p["status"]] = counts.get(p["status"], 0) + 1
    out = [
        "# Pain point map",
        "",
        "_Generated from `src/pain_point_resolver/data/pain_points.json`. Edit that file, then run "
        "`python scripts/gen_pain_points_md.py`._",
        "",
        "Status: " + " · ".join(f"**{k}** {v}" for k, v in sorted(counts.items())),
        "",
        f"Leverage point: **#{data['leverage_point']}**",
    ]
    group = None
    for p in items:
        if p["group"] != group:
            group = p["group"]
            out += ["", f"## {group}", "", "| # | Pain point | Contract | Status | Modules |", "|---|---|---|---|---|"]
        mods = ", ".join(f"`{m}`" for m in p["modules"]) or "help wanted"
        note = f" ({p['note']})" if p.get("note") else ""
        out.append(f"| {p['id']} | {p['title']}{note} | {p['contract']} | {p['status']} | {mods} |")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    text = render()
    if "--check" in sys.argv:
        if not DST.exists() or DST.read_text(encoding="utf-8") != text:
            sys.exit("docs/PAIN_POINTS.md is stale: run python scripts/gen_pain_points_md.py")
        print("docs/PAIN_POINTS.md is current")
    else:
        DST.write_text(text, encoding="utf-8")
        print(f"wrote {DST.relative_to(ROOT)}")
