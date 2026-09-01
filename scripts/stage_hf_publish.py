#!/usr/bin/env python3
"""Stage adapter weights and dataset for Hugging Face upload."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_ADAPTER = Path(
    "/home/wjadams/Documents/bitbucket/rddocs/papers/2026/"
    "mdmp-staff-planning-assistant/outputs/mistral7b-mdmp-lora"
)

MODEL_FILES = (
    "adapter_config.json",
    "adapter_model.safetensors",
    "chat_template.jinja",
    "tokenizer.json",
    "tokenizer_config.json",
    "tokenizer.model",
)

STAGING_MODEL = ROOT / "staging" / "hf-model"
STAGING_DATASET = ROOT / "staging" / "hf-dataset"


def copy_adapter(source: Path, dest: Path) -> None:
    if not source.is_dir():
        raise FileNotFoundError(f"Adapter directory not found: {source}")
    dest.mkdir(parents=True, exist_ok=True)
    for name in MODEL_FILES:
        src = source / name
        if not src.is_file():
            raise FileNotFoundError(f"Missing adapter file: {src}")
        shutil.copy2(src, dest / name)


def stage_dataset(pairs_path: Path, dest: Path) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    count = 0
    out_path = dest / "pairs.jsonl"
    with pairs_path.open(encoding="utf-8") as src, out_path.open("w", encoding="utf-8") as out:
        for line in src:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if not row.get("reviewed"):
                continue
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def copy_card(source: Path, dest: Path) -> None:
    shutil.copy2(source, dest)


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage MDMP adapter and dataset for HF upload.")
    parser.add_argument(
        "--adapter",
        type=Path,
        default=DEFAULT_ADAPTER,
        help="Source LoRA adapter directory",
    )
    parser.add_argument(
        "--pairs",
        type=Path,
        default=ROOT / "data" / "pairs.jsonl",
        help="Source pairs.jsonl",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove staging/ before copying",
    )
    args = parser.parse_args()

    if args.clean and (ROOT / "staging").exists():
        shutil.rmtree(ROOT / "staging")

    copy_adapter(args.adapter, STAGING_MODEL)
    copy_card(ROOT / "docs" / "hf-model-card.md", STAGING_MODEL / "README.md")

    pair_count = stage_dataset(args.pairs, STAGING_DATASET)
    copy_card(ROOT / "docs" / "hf-dataset-card.md", STAGING_DATASET / "README.md")

    print(f"Staged model adapter: {STAGING_MODEL}")
    print(f"Staged dataset ({pair_count} reviewed pairs): {STAGING_DATASET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
