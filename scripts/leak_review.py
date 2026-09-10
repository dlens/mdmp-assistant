#!/usr/bin/env python3
"""Scan training JSONL and/or the tracked public tree for forbidden leak terms."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Rejected in training/eval JSONL (instruction data must stay open-doctrine).
TRAINING_FORBIDDEN_PATTERNS = [
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

# Rejected in tracked docs/code (internal platform / capture IP).
# "Decision Lens" is allowed as company affiliation in the paper; HF org slug
# "decisionlens" is also allowed. Monte Carlo stays training-only (legit OR term).
TREE_FORBIDDEN_PATTERNS = [
    r"where-wins",
    r"where wins",
    r"\bDLX\b",
    r"DataHub",
    r"AppHub",
    r"\bOPNAV\b",
    r"win-percent",
    r"polytope",
    r"OBJ EAGLE",
    r"2nd BCT",
    r"wherewins",
    r"opnav-n80",
    r"local-integration",
    r"apphub-deploy-plan",
]

TREE_EXTENSIONS = {
    ".md",
    ".tex",
    ".py",
    ".json",
    ".jsonl",
    ".yml",
    ".yaml",
    ".sh",
    ".txt",
    ".toml",
    ".example",
}

# Policy / eval files that necessarily name forbidden terms.
TREE_ALLOWLIST = {
    Path("scripts/leak_review.py"),
    Path("scripts/copy_clean_check.py"),
    Path("eval/golden_questions.json"),
}

TRAINING_COMPILED = [re.compile(p, re.IGNORECASE) for p in TRAINING_FORBIDDEN_PATTERNS]
TREE_COMPILED = [re.compile(p, re.IGNORECASE) for p in TREE_FORBIDDEN_PATTERNS]


def check_text(text: str, path: str, line_no: int, patterns: list[re.Pattern[str]]) -> list[str]:
    hits = []
    for pattern in patterns:
        if pattern.search(text):
            hits.append(f"{path}:{line_no}: matched {pattern.pattern!r}")
    return hits


def review_jsonl(path: Path) -> list[str]:
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
            errors.extend(check_text(blob, str(path), i, TRAINING_COMPILED))
    return errors


def review_text_file(path: Path, *, relative: Path) -> list[str]:
    if relative in TREE_ALLOWLIST:
        return []
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"{relative}: not valid UTF-8 text"]
    for i, line in enumerate(text.splitlines(), start=1):
        errors.extend(check_text(line, str(relative), i, TREE_COMPILED))
    return errors


def tracked_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    files: list[Path] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        rel = Path(raw.decode())
        if rel.suffix.lower() in TREE_EXTENSIONS or rel.name == ".env.example":
            files.append(rel)
    return files


def review_tree(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in tracked_files(root):
        path = root / rel
        if not path.is_file():
            continue
        if rel.suffix.lower() == ".jsonl":
            # JSONL already covered by training rules when passed explicitly;
            # still scan tree copies with training patterns for safety.
            errors.extend(review_jsonl(path))
            continue
        errors.extend(review_text_file(path, relative=rel))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Leak review for training JSONL and/or the tracked public tree."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="JSONL files to scan (training rules). Omit with --tree only.",
    )
    parser.add_argument(
        "--tree",
        action="store_true",
        help="Also scan tracked docs/code for internal platform / capture terms.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Project root for --tree (default: this project)",
    )
    args = parser.parse_args()

    if not args.paths and not args.tree:
        parser.error("provide JSONL paths and/or --tree")

    all_errors: list[str] = []
    scanned = 0

    for path in args.paths:
        if not path.exists():
            all_errors.append(f"{path}: file not found")
            continue
        all_errors.extend(review_jsonl(path))
        scanned += 1

    if args.tree:
        all_errors.extend(review_tree(args.root.resolve()))
        scanned += 1

    if all_errors:
        print("LEAK REVIEW FAILED:", file=sys.stderr)
        for err in all_errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print(f"OK: leak review passed ({scanned} scan target(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
