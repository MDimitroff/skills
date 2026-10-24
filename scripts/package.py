#!/usr/bin/env python3
"""Build one distributable zip per skill into dist/ (stdlib only).

Each zip has the skill folder at its root (<name>/SKILL.md), which is the
layout expected by Claude.ai / Claude Desktop "Upload skill" and is trivially
unzippable into any skills directory. Output is deterministic.
"""
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def frontmatter_name(skill_md: Path) -> str:
    m = re.match(r"---\n(.*?)\n---", skill_md.read_text(encoding="utf-8"), re.S)
    n = re.search(r"^name:\s*(\S+)\s*$", m.group(1), re.M) if m else None
    return n.group(1).strip("\"'") if n else ""


def main() -> int:
    DIST.mkdir(exist_ok=True)
    status = 0
    for d in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        md = d / "SKILL.md"
        if not md.is_file():
            print(f"SKIP  {d.name}: no SKILL.md")
            continue
        if frontmatter_name(md) != d.name:
            print(f"FAIL  {d.name}: frontmatter name != directory name")
            status = 1
            continue
        out = DIST / f"{d.name}.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(p for p in d.rglob("*") if p.is_file()):
                zi = zipfile.ZipInfo(f"{d.name}/{f.relative_to(d).as_posix()}", FIXED_TIME)
                zi.external_attr = 0o644 << 16
                z.writestr(zi, f.read_bytes(), zipfile.ZIP_DEFLATED)
        print(f"OK    {out.relative_to(ROOT)}")
    return status


if __name__ == "__main__":
    sys.exit(main())
