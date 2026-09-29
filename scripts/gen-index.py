#!/usr/bin/env python3
"""
Regenerate icons_database.json by scanning iconbin/ and pfpbin/.

Usage:  python3 scripts/gen-index.py

Emits one record per image: filename, source dir, byte size, extension, and a
small set of tags (best-effort) derived from the filename / directory so the
gallery can filter with @tag queries.
"""
from __future__ import annotations

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "icons_database.json")
BINS = {"iconbin": "icon", "pfpbin": "pfp"}
EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".svg"}

# subject keywords sniffed from filenames (case-insensitive substring)
KEYWORDS = [
    "agitkrakk", "camera", "celestine", "cnth", "edna", "ernest", "fox",
    "halftone", "jar", "jara", "kaguya", "long", "man", "mari", "owl",
    "screenshot", "smirk", "tape", "talis", "uri", "warframe", "yachiyo",
]

# artist patterns: "... - by 焦茶", "...by-NAME"
BY_PATTERNS = [
    re.compile(r"by\s+([a-z0-9_]+)", re.IGNORECASE),
    re.compile(r"-by-([a-z0-9]+)", re.IGNORECASE),
]


def derive_tags(name: str, bin_dir: str) -> list[str]:
    lower = name.lower()
    tags = {BINS[bin_dir]}

    # explicit resolution in the name (e.g. 26x25, 300x300, 600x600)
    m = re.search(r"(\d{2,5})x(\d{2,5})", lower)
    if m:
        tags.add(m.group(0))

    # rounded / edit markers
    if "rounded" in lower:
        tags.add("rounded")
    if "halftone" in lower:
        tags.add("halftone")

    # artist credits
    for pat in BY_PATTERNS:
        m = pat.search(name)
        if m:
            tags.add("by-" + m.group(1).lower())
            break

    # subject keywords
    for kw in KEYWORDS:
        if kw in lower:
            tags.add(kw)

    return sorted(tags)


def main() -> None:
    db: dict[str, dict] = {}
    for bin_dir, _ in BINS.items():
        path = os.path.join(ROOT, bin_dir)
        for entry in sorted(os.listdir(path)):
            ext = os.path.splitext(entry)[1].lower()
            if ext not in EXTS:
                continue
            full = os.path.join(path, entry)
            db[entry] = {
                "filename": entry,
                "dir": bin_dir,
                "size": os.path.getsize(full),
                "ext": ext.lstrip("."),
                "tags": derive_tags(entry, bin_dir),
            }

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(db, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"wrote {len(db)} images -> {OUT}")


if __name__ == "__main__":
    main()
