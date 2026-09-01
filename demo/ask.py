#!/usr/bin/env python3
"""CLI chat demo for the MDMP Staff Planning Assistant."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from train.inference import generate_answer, load_model  # noqa: E402


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description="Chat with the MDMP planning assistant.")
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "train" / "config.yaml",
    )
    parser.add_argument(
        "--adapter",
        type=Path,
        default=ROOT / "outputs" / "mistral7b-mdmp-lora",
        help="LoRA adapter directory (omit with --base for baseline model)",
    )
    parser.add_argument(
        "--base",
        action="store_true",
        help="Use base model only (no adapter)",
    )
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.1)
    args = parser.parse_args()

    cfg = load_config(args.config)
    adapter = None if args.base else args.adapter
    if adapter and not adapter.exists():
        print(f"Adapter not found: {adapter}", file=sys.stderr)
        print("Train first: python train/finetune.py", file=sys.stderr)
        return 1

    label = "base" if args.base else str(adapter)
    print(f"Loading {cfg['model_name']}" + ("" if args.base else f" + {adapter}"))
    model, tokenizer = load_model(
        model_name=cfg["model_name"],
        adapter_path=adapter,
        max_seq_length=cfg["max_seq_length"],
        load_in_4bit=cfg.get("load_in_4bit", True),
    )

    print("MDMP Staff Planning Assistant — type a question, empty line to quit.")
    print("Unofficial educational tool. Verify against FM 5-0 / ADP 5-0.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return 0
        if not question:
            print("Bye.")
            return 0
        answer = generate_answer(
            model,
            tokenizer,
            question,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
        )
        print(f"Assistant: {answer}\n")


if __name__ == "__main__":
    raise SystemExit(main())
