#!/usr/bin/env python3
"""Run golden-question eval against base model or fine-tuned adapter."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from eval.scoring import score_response  # noqa: E402
from train.inference import generate_answer, load_model  # noqa: E402


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_golden(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description="Golden-question eval for MDMP assistant.")
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "train" / "config.yaml",
    )
    parser.add_argument(
        "--golden",
        type=Path,
        default=ROOT / "eval" / "golden_questions.json",
    )
    parser.add_argument(
        "--adapter",
        type=Path,
        help="LoRA adapter directory (omit for base-model baseline)",
    )
    parser.add_argument(
        "--label",
        default="",
        help="Report label (e.g. baseline, v1)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="JSON report path (default: eval/reports/<label>_<timestamp>.json)",
    )
    parser.add_argument("--limit", type=int, help="Run only first N questions")
    parser.add_argument("--max-new-tokens", type=int, default=256)
    args = parser.parse_args()

    cfg = load_config(args.config)
    questions = load_golden(args.golden)
    if args.limit:
        questions = questions[: args.limit]

    label = args.label or ("finetuned" if args.adapter else "baseline")
    print(f"Loading model: {cfg['model_name']}" + (f" + {args.adapter}" if args.adapter else " (base)"))
    model, tokenizer = load_model(
        model_name=cfg["model_name"],
        adapter_path=args.adapter,
        max_seq_length=cfg["max_seq_length"],
        load_in_4bit=cfg.get("load_in_4bit", True),
    )

    results: list[dict] = []
    passed = 0
    for i, item in enumerate(questions, start=1):
        question = item["question"]
        print(f"[{i}/{len(questions)}] {question}")
        response = generate_answer(
            model,
            tokenizer,
            question,
            max_new_tokens=args.max_new_tokens,
        )
        score = score_response(
            response,
            must_mention=item.get("must_mention", []),
            must_not_mention=item.get("must_not_mention", []),
        )
        if score.passed:
            passed += 1
        results.append(
            {
                "question": question,
                "passed": score.passed,
                "response": response,
                "missing_must_mention": score.missing_must_mention,
                "forbidden_mentions": score.forbidden_mentions,
                "expected_sources": item.get("expected_sources", []),
            }
        )
        status = "PASS" if score.passed else "FAIL"
        print(f"  {status}")

    total = len(questions)
    pass_rate = passed / total if total else 0.0
    report = {
        "label": label,
        "model": cfg["model_name"],
        "adapter": str(args.adapter) if args.adapter else None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "total": total,
        "pass_rate": round(pass_rate, 4),
        "results": results,
    }

    if args.out:
        out_path = args.out
    else:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_path = ROOT / "eval" / "reports" / f"{label}_{ts}.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\nPass rate: {passed}/{total} ({pass_rate:.0%})")
    print(f"Report: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
