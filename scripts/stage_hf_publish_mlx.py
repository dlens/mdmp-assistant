#!/usr/bin/env python3
"""Stage the MLX LoRA adapter for Hugging Face upload.

Does not stage the dataset (already on the Hub) and does not touch the
Unsloth/PEFT staging path used by stage_hf_publish.py.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_ADAPTER = ROOT / "outputs" / "mlx-mistral7b-mdmp-lora-v4"
FALLBACK_ADAPTER = Path(
    "/Users/wjadams/Repos/bitbucket/rddocs/papers/2026/"
    "mdmp-staff-planning-assistant/outputs/mlx-mistral7b-mdmp-lora-v4"
)

MODEL_FILES = (
    "adapter_config.json",
    "adapters.safetensors",
)

STAGING_MODEL = ROOT / "staging" / "hf-model-mlx"


def resolve_source(adapter: Path) -> Path:
    if adapter.is_dir():
        return adapter
    if adapter == DEFAULT_ADAPTER and FALLBACK_ADAPTER.is_dir():
        return FALLBACK_ADAPTER
    raise FileNotFoundError(f"Adapter directory not found: {adapter}")


def copy_adapter(source: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for name in MODEL_FILES:
        src = source / name
        if not src.is_file():
            raise FileNotFoundError(f"Missing MLX adapter file: {src}")
        shutil.copy2(src, dest / name)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage MDMP MLX adapter for HF upload (adapter only)."
    )
    parser.add_argument(
        "--adapter",
        type=Path,
        default=DEFAULT_ADAPTER,
        help="Source MLX LoRA adapter directory",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove staging/hf-model-mlx/ before copying (does not wipe Unsloth staging)",
    )
    args = parser.parse_args()

    if args.clean and STAGING_MODEL.exists():
        shutil.rmtree(STAGING_MODEL)

    source = resolve_source(args.adapter)
    copy_adapter(source, STAGING_MODEL)
    shutil.copy2(ROOT / "docs" / "hf-model-card-mlx.md", STAGING_MODEL / "README.md")

    print(f"Staged MLX adapter from {source}: {STAGING_MODEL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
