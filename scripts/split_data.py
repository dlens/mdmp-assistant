#!/usr/bin/env python3
"""Split data/pairs.jsonl into train.jsonl and eval.jsonl."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_pairs(path: Path, *, reviewed_only: bool) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if reviewed_only and not row.get("reviewed"):
                raise SystemExit(
                    f"{path}:{i}: row not reviewed — set reviewed=true or use --include-unreviewed"
                )
            rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Split pairs.jsonl into train/eval.")
    parser.add_argument(
        "--in",
        dest="in_path",
        type=Path,
        default=ROOT / "data" / "pairs.jsonl",
        help="Source pairs file (default: data/pairs.jsonl)",
    )
    parser.add_argument(
        "--train-out",
        type=Path,
        default=ROOT / "data" / "train.jsonl",
    )
    parser.add_argument(
        "--eval-out",
        type=Path,
        default=ROOT / "data" / "eval.jsonl",
    )
    parser.add_argument(
        "--eval-ratio",
        type=float,
        default=0.15,
        help="Fraction held out for eval (default: 0.15)",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--include-unreviewed",
        action="store_true",
        help="Allow unreviewed rows in the split",
    )
    args = parser.parse_args()

    if not args.in_path.exists():
        raise SystemExit(f"Missing {args.in_path}")

    rows = load_pairs(args.in_path, reviewed_only=not args.include_unreviewed)
    if len(rows) < 2:
        raise SystemExit("Need at least 2 pairs to split")

    rng = random.Random(args.seed)
    shuffled = rows[:]
    rng.shuffle(shuffled)

    n_eval = max(1, int(round(len(shuffled) * args.eval_ratio)))
    n_eval = min(n_eval, len(shuffled) - 1)
    eval_rows = shuffled[:n_eval]
    train_rows = shuffled[n_eval:]

    write_jsonl(args.train_out, train_rows)
    write_jsonl(args.eval_out, eval_rows)

    print(f"Source: {args.in_path} ({len(rows)} reviewed pairs)")
    print(f"Train:  {args.train_out} ({len(train_rows)} rows)")
    print(f"Eval:   {args.eval_out} ({len(eval_rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
