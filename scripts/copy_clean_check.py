#!/usr/bin/env python3
"""Fail if this open-doctrine tree is not safe to copy into a blank public repo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_NAME_FRAGMENTS = (
    "expert-review",
    "overlay.jsonl",
    "apphub-deploy-plan",
)

SKIP_DIR_NAMES = {
    ".git",
    ".venv",
    ".venv-mlx",
    "__pycache__",
    "outputs",
    "staging",
    "node_modules",
}


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy-clean check for the open MDMP assistant folder."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Project root (default: this project)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    for path in (
        root / "docs" / "expert-review",
        root / "docs" / "apphub-deploy-plan.md",
        root / "data" / "overlay.jsonl",
        root / "corpus" / "proprietary",
    ):
        if path.exists():
            errors.append(f"forbidden path exists: {path.relative_to(root)}")

    for path in iter_files(root):
        rel = str(path.relative_to(root))
        for fragment in FORBIDDEN_NAME_FRAGMENTS:
            if fragment in rel:
                errors.append(f"forbidden name fragment {fragment!r} in {rel}")
                break

    if errors:
        print("COPY-CLEAN CHECK FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print(f"OK: {root} is copy-clean for a blank public repo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
