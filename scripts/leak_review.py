#!/usr/bin/env python3
"""Scan JSONL training files for forbidden terms (leak guard)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FORBIDDEN_PATTERNS = [
    r"where-wins",
    r"where wins",
    r"Decision Lens",
    r"\bDLX\b",
    r"DataHub",
    r"AppHub",
    r"\bOPNAV\b",
    r"win-percent",
    r"polytope",
    r"Monte Carlo",
    r"OBJ EAGLE",
    r"2nd BCT",
    r"wherewins",
]

COMPILED = [re.compile(p, re.IGNORECASE) for p in FORBIDDEN_PATTERNS]


def check_text(text: str, path: str, line_no: int) -> list[str]:
    hits = []
    for pattern in COMPILED:
        if pattern.search(text):
            hits.append(f"{path}:{line_no}: matched {pattern.pattern!r}")
    return hits


def review_file(path: Path) -> list[str]:
    errors: list[str] = []
    with path.open(encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"{path}:{i}: invalid JSON: {e}")
                continue
            blob = json.dumps(obj, ensure_ascii=False)
            errors.extend(check_text(blob, str(path), i))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Leak review for training JSONL files.")
    parser.add_argument("paths", nargs="+", type=Path, help="JSONL files to scan")
    args = parser.parse_args()

    all_errors: list[str] = []
    for path in args.paths:
        if not path.exists():
            all_errors.append(f"{path}: file not found")
            continue
        all_errors.extend(review_file(path))

    if all_errors:
        print("LEAK REVIEW FAILED:", file=sys.stderr)
        for err in all_errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print(f"OK: {len(args.paths)} file(s) passed leak review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
