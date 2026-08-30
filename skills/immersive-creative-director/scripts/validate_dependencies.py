#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path


REQUIRED = [
    "grilling", "domain-modeling", "impeccable", "design-dna", "scrollcraft",
    "design-loop", "filipe-flow", "watch", "browser-proof",
]
ROOTS = [Path.home() / ".codex" / "skills", Path.home() / ".agents" / "skills"]


def resolve(name):
    for root in ROOTS:
        path = root / name / "SKILL.md"
        if path.is_file():
            return path
    return None


def main():
    rows = []
    missing = []
    for name in REQUIRED:
        path = resolve(name)
        if path is None:
            missing.append(name)
            continue
        content = path.read_bytes()
        rows.append({"name": name, "path": str(path), "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)})
    if missing:
        print("FAIL: missing required capabilities: " + ", ".join(missing))
        return 1
    print("PASS: required capability entrypoints resolved.")
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
