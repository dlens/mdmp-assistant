#!/usr/bin/env python3
"""Convert train.jsonl / eval.jsonl into mlx-lm JSONL (train.jsonl + valid.jsonl).

Default export is chat messages so mlx-lm can apply Mistral's template and
mask the prompt in the loss. Pass --format text to keep the Unsloth [INST]
string used by train/finetune.py.

Does not export golden questions. Run after scripts/split_data.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from train.formatting import build_user_prompt, format_training_text  # noqa: E402


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def to_mlx_row(row: dict, *, fmt: str) -> dict:
    if fmt == "text":
        return {
            "text": format_training_text(
                row["instruction"],
                row["output"],
                row.get("input", ""),
            )
        }
    user = build_user_prompt(row["instruction"], row.get("input", ""))
    return {
        "messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": (row.get("output") or "").strip()},
        ]
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export MDMP train/eval JSONL to data/mlx for mlx-lm."
    )
    parser.add_argument(
        "--train-file",
        type=Path,
        default=ROOT / "data" / "train.jsonl",
    )
    parser.add_argument(
        "--eval-file",
        type=Path,
        default=ROOT / "data" / "eval.jsonl",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "data" / "mlx",
    )
    parser.add_argument(
        "--format",
        choices=["messages", "text"],
        default="messages",
        help="messages: chat JSONL for mlx-lm template + prompt masking. "
        "text: Unsloth <s>[INST] ... string.",
    )
    args = parser.parse_args()

    if not args.train_file.is_file():
        raise SystemExit(f"Missing {args.train_file} — run scripts/split_data.py first.")

    train_rows = [to_mlx_row(r, fmt=args.format) for r in load_jsonl(args.train_file)]
    write_jsonl(args.out_dir / "train.jsonl", train_rows)
    print(
        f"Wrote {len(train_rows)} {args.format} rows → {args.out_dir / 'train.jsonl'}"
    )

    if args.eval_file.is_file():
        valid_rows = [to_mlx_row(r, fmt=args.format) for r in load_jsonl(args.eval_file)]
        write_jsonl(args.out_dir / "valid.jsonl", valid_rows)
        print(
            f"Wrote {len(valid_rows)} {args.format} rows → {args.out_dir / 'valid.jsonl'}"
        )
    else:
        print(f"No {args.eval_file}; skipped valid.jsonl")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
