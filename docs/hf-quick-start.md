# Hugging Face quick start

Use the published **MDMP Staff Planning Assistant** adapter for inference only. No training, no dataset prep, no golden eval.

**Disclaimer:** Unofficial educational tool. Not affiliated with the U.S. Army. Verify answers against FM 5-0 / ADP 5-0.

## What is published

| Artifact | URL |
|----------|-----|
| LoRA adapter | [decisionlens/mistral7b-mdmp-lora](https://huggingface.co/decisionlens/mistral7b-mdmp-lora) |
| Training pairs (optional) | [decisionlens/mdmp-staff-planning-pairs](https://huggingface.co/datasets/decisionlens/mdmp-staff-planning-pairs) |

You only need the **adapter** (~168 MB). The base model (`mistralai/Mistral-7B-Instruct-v0.3`) downloads automatically on first run.

## Prerequisites

- **GPU:** NVIDIA with ~5–8 GB VRAM (4-bit inference)
- **Python:** 3.10+ (3.13 tested on Spark)
- **CUDA** and `TRITON_PTXAS_PATH` set (see below)

Apple Silicon? This adapter targets the Spark/Unsloth stack. Mac users need the separate MLX path — see [README.md](../README.md#mac--mlx-sidecar) (different weights, not interchangeable).

## Five-minute local chat

```bash
git clone https://github.com/dlens/mdmp-assistant.git
cd mdmp-assistant

python -m venv .venv && source .venv/bin/activate
pip install -r requirements-ml.txt

pip install huggingface_hub
hf download decisionlens/mistral7b-mdmp-lora --local-dir outputs/mistral7b-mdmp-lora

export TRITON_PTXAS_PATH=/usr/local/cuda/bin/ptxas   # adjust if your CUDA install differs
python demo/ask.py --adapter outputs/mistral7b-mdmp-lora
```

Type a question at the `You:` prompt. Empty line or Ctrl+D to quit.

First run downloads the base Mistral-7B weights (~4 GB) in addition to the adapter.

## One question from Python

From the repo root after install and download:

```python
from train.inference import load_model, generate_answer

model, tokenizer = load_model(
    model_name="mistralai/Mistral-7B-Instruct-v0.3",
    adapter_path="outputs/mistral7b-mdmp-lora",
    load_in_4bit=True,
)
print(generate_answer(model, tokenizer, "What MDMP step is war gaming?"))
```

Prompt format: `<s>[INST] {question} [/INST] `. Defaults: `temperature=0.1`, `max_new_tokens=256`.

## What you do not need

| Skip | Why |
|------|-----|
| `data/pairs.jsonl` | Training data — not required for inference |
| `python train/finetune.py` | Adapter is already trained |
| `python scripts/split_data.py` | Data pipeline — training only |
| `eval/run_golden.py` | Maintainer eval — not required to chat |
| Hugging Face write token | Read/download is public; token only for re-publish |

## Not available yet

There is **no hosted try-it-now option** today:

- No **Hugging Face Space** (browser chat)
- No **Inference Endpoint** (managed GPU API)

Using the model still requires a local machine (or your own server) with a suitable GPU.

## Coming later (optional)

| Option | Purpose |
|--------|---------|
| HF Space | Browser demo without local GPU setup |
| HF Inference Endpoint | API access for apps and integrations |

Track progress in [apphub-deploy-plan.md](apphub-deploy-plan.md). AppHub sidecar deployment is separate from HF hosting.

## More detail

- Model card: [hf-model-card.md](hf-model-card.md)
- Full repo README: [README.md](../README.md)
- Re-publish adapter: [README.md#publishing](../README.md#publishing)
