# MDMP Staff Planning Assistant (O1)

Open-source fine-tuned LLM for **Military Decision-Making Process** coaching — public doctrine only, no proprietary algorithms or customer data.

**Disclaimer:** Unofficial educational tool. Not affiliated with the U.S. Army. Not a substitute for qualified staff planning or classified planning systems. Ground answers in FM 5-0 / ADP 5-0 and verify citations.

## Sprint status

| Milestone | Target | Status |
|-----------|--------|--------|
| Day 1 — corpus + 50 draft pairs + golden eval | Jul 28 | Done |
| Data + baseline + v4 train (40% golden) | Jul 29 | Done |
| Training data expanded to 303 pairs (harmonized) | Jul 31 | Done |
| Sprint MVP — LoRA + demo | Aug 1 | Done (v7: 70% golden; baseline 5%) |
| Public v0.1 — Hugging Face | Week of Aug 4 | Pending (adapter weights) |

**Sprint 1 summary:** [eval/sprint1-summary.md](eval/sprint1-summary.md)

**Paper 1 (methods):** [docs/paper1-open-mdmp-lora.tex](docs/paper1-open-mdmp-lora.tex)

**Spark vs Mac training (iters, scale, implications):** [docs/spark-vs-mac-training.md](docs/spark-vs-mac-training.md)

**AppHub deploy plan:** [docs/apphub-deploy-plan.md](docs/apphub-deploy-plan.md)

## Layout

```text
corpus/doctrine/     Public MDMP reference markdown
corpus/scenarios/    Fictional training scenarios
data/                pairs.jsonl (source of truth), train.jsonl, eval.jsonl
eval/                golden_questions.json, run_golden.py, run_golden_mlx.py, reports/
scripts/             split_data.py, export_mlx_data.py, generate_pairs.py, leak_review.py, copy_clean_check.py
train/               config.yaml, finetune.py, formatting.py, inference.py, mlx_config.yaml, mlx_inference.py
demo/                ask.py — CLI chat demo
docs/                paper1-open-mdmp-lora.tex; spark-vs-mac-training.md; apphub-deploy-plan.md
```

## Data workflow

`data/pairs.jsonl` is the single source of truth. Edit it directly (or append reviewed rows from suggestions).

```bash
# Optional: corpus-driven suggestions (reviewed=false) — does not touch pairs.jsonl
python scripts/generate_pairs.py

# Split reviewed pairs → train / eval (85% / 15%)
python scripts/split_data.py

# Leak review before commit
python scripts/leak_review.py data/pairs.jsonl data/train.jsonl
```

Golden questions in `eval/golden_questions.json` stay separate and must never appear verbatim in training files.

## Training and eval

From the project root:

```bash
export TRITON_PTXAS_PATH=/usr/local/cuda/bin/ptxas

# 1. Baseline — base Mistral-7B, no adapter (~15–30 min first run for model download)
python eval/run_golden.py --label baseline

# 2. Overfit sanity check — 10 examples, 3 epochs (proves training loop)
python train/finetune.py --overfit

# 3. Eval the overfit adapter (expect high pass rate on training-like questions)
python eval/run_golden.py --adapter outputs/overfit-sanity --label overfit

# 4. Full train (after expanding pairs.jsonl to 150–200 rows)
python scripts/split_data.py
python train/finetune.py

# 5. Golden eval vs fine-tuned model
python eval/run_golden.py --adapter outputs/mistral7b-mdmp-lora --label v1
```

Reports land in `eval/reports/`. Latest: **v7 — 14/20 (70%)** vs baseline **1/20 (5%)**. Full progression in [eval/sprint1-summary.md](eval/sprint1-summary.md).

## Mac / MLX sidecar

Apple Silicon QLoRA via `mlx-lm`. Does **not** replace Spark Unsloth (`train/finetune.py`). Adapters are not interchangeable. Use a separate venv from `requirements-ml.txt`.

Spark Unsloth remains the publish path. Mac golden (same 20 questions):

| Run | Notes | Golden |
|-----|--------|--------|
| Spark Unsloth v7 | r=16, α=32, lr 2e-4, 2 epochs | **14/20 (70%)** |
| mlx-v1 | copied α as MLX `scale=32` | 0/20 (NaN) |
| mlx-v2 | mlx defaults, 16 layers, 200 iters | 4/20 (20%) |
| mlx-v3 | Spark lr 2e-4 + prompt mask | 0/20 (empty) |
| **mlx-v4** | r=16, scale=2.0, all layers, lr 5e-5, 600 iters | **17/20 (85%)** |

`mlx-lm` applies LoRA `scale` directly. PEFT/Unsloth apply `(alpha / rank)`, so Spark's 16/32 maps to **scale 2.0**, not 32.

```bash
pip install -r requirements-mlx.txt
python scripts/split_data.py
python scripts/export_mlx_data.py          # chat messages JSONL (default)

# overfit sanity
python -m mlx_lm lora --model mlx-community/Mistral-7B-Instruct-v0.3-4bit \
  --data data/mlx --train --adapter-path outputs/mlx-overfit-sanity \
  --batch-size 1 --num-layers 16 --iters 30 --grad-checkpoint

# full train (see train/mlx_config.yaml)
python -m mlx_lm lora -c train/mlx_config.yaml

python eval/run_golden_mlx.py --label mlx-baseline
python eval/run_golden_mlx.py --adapter outputs/mlx-mistral7b-mdmp-lora-v4 --label mlx-v4
```

Hyperparameters live in `train/mlx_config.yaml`. Export writes `data/mlx/train.jsonl` and `data/mlx/valid.jsonl` (generated; gitignored). Why Mac used 600 iters vs Spark’s ~70 updates: [docs/spark-vs-mac-training.md](docs/spark-vs-mac-training.md). Serving this adapter from AppHub: [docs/apphub-deploy-plan.md](docs/apphub-deploy-plan.md).

## Demo

```bash
export TRITON_PTXAS_PATH=/usr/local/cuda/bin/ptxas
python demo/ask.py                    # fine-tuned adapter
python demo/ask.py --base               # base Mistral-7B (no adapter)
```

Type a question at the `You:` prompt; empty line or Ctrl+D to quit.

## ML stack

NVIDIA GB10 Spark workstation. Pins: `requirements-ml.txt`

```bash
export TRITON_PTXAS_PATH=/usr/local/cuda/bin/ptxas
pip install -r requirements-ml.txt
```

Mac sidecar (separate venv): `pip install -r requirements-mlx.txt`

## Pre-commit leak checklist

- [ ] No customer names, OPNAV, or real unit designations tied to capture work
- [ ] No proprietary algorithm or product terms (see `scripts/leak_review.py`)
- [ ] Scenario is fictional or purely doctrinal
- [ ] Golden questions not copied verbatim into `train.jsonl`
- [ ] `python scripts/copy_clean_check.py` — no expert-review packet, overlay, or proprietary corpus
