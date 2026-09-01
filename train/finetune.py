#!/usr/bin/env python3
"""Unsloth SFT fine-tune for MDMP Staff Planning Assistant."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from train.formatting import format_training_text  # noqa: E402


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def build_dataset(rows: list[dict]):
    from datasets import Dataset

    texts = [
        format_training_text(
            row["instruction"],
            row["output"],
            row.get("input", ""),
        )
        for row in rows
    ]
    return Dataset.from_dict({"text": texts})


def main() -> int:
    parser = argparse.ArgumentParser(description="Fine-tune Mistral-7B with Unsloth LoRA.")
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "train" / "config.yaml",
    )
    parser.add_argument(
        "--train-file",
        type=Path,
        help="Override train_file from config",
    )
    parser.add_argument(
        "--eval-file",
        type=Path,
        help="Override eval_file from config",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Override output_dir from config",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        help="Limit training rows (for overfit sanity checks)",
    )
    parser.add_argument(
        "--overfit",
        action="store_true",
        help="Shortcut: train on 10 examples for 3 epochs",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    train_path = args.train_file or ROOT / cfg["train_file"]
    eval_path = args.eval_file or ROOT / cfg["eval_file"]
    output_dir = args.output_dir or ROOT / cfg["output_dir"]

    train_rows = load_jsonl(train_path)
    if args.overfit:
        train_rows = train_rows[:10]
        cfg["num_train_epochs"] = 3
        output_dir = output_dir.parent / "overfit-sanity"
    elif args.max_samples:
        train_rows = train_rows[: args.max_samples]

    if not train_rows:
        raise SystemExit(f"No training rows in {train_path}")

    eval_rows = load_jsonl(eval_path) if eval_path.exists() else []
    train_dataset = build_dataset(train_rows)
    eval_dataset = build_dataset(eval_rows) if eval_rows else None

    from unsloth import FastLanguageModel
    from trl import SFTConfig, SFTTrainer
    import torch

    use_bf16 = torch.cuda.is_available() and torch.cuda.is_bf16_supported()

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=cfg["model_name"],
        max_seq_length=cfg["max_seq_length"],
        dtype=None,
        load_in_4bit=cfg.get("load_in_4bit", True),
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r=cfg["lora_r"],
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
        lora_alpha=cfg["lora_alpha"],
        lora_dropout=cfg["lora_dropout"],
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=42,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    sft_args = SFTConfig(
        output_dir=str(output_dir),
        num_train_epochs=cfg["num_train_epochs"],
        per_device_train_batch_size=cfg["per_device_train_batch_size"],
        gradient_accumulation_steps=cfg["gradient_accumulation_steps"],
        learning_rate=cfg["learning_rate"],
        warmup_ratio=cfg["warmup_ratio"],
        logging_steps=5,
        save_strategy="epoch",
        eval_strategy="epoch" if eval_dataset else "no",
        load_best_model_at_end=bool(eval_dataset),
        metric_for_best_model="eval_loss" if eval_dataset else None,
        greater_is_better=False,
        bf16=use_bf16,
        fp16=not use_bf16 and torch.cuda.is_available(),
        optim="adamw_8bit",
        seed=42,
        report_to="none",
        dataset_text_field="text",
        max_length=cfg["max_seq_length"],
    )

    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        args=sft_args,
    )

    print(f"Training on {len(train_rows)} examples → {output_dir}")
    if eval_dataset:
        print(f"Eval set: {len(eval_rows)} examples")
    trainer.train()
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))
    print(f"Saved adapter to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
