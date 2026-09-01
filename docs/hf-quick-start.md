# Hugging Face quick start

Use the published **MDMP Staff Planning Assistant** adapter for inference only. No training, no dataset prep, no golden eval.

**Disclaimer:** Unofficial educational tool. Not affiliated with the U.S. Army. Verify answers against FM 5-0 / ADP 5-0.

## What is published

| Artifact | URL |
|----------|-----|
| LoRA adapter (NVIDIA / Unsloth) | [decisionlens/mistral7b-mdmp-lora](https://huggingface.co/decisionlens/mistral7b-mdmp-lora) |
| LoRA adapter (Apple Silicon / MLX) | [decisionlens/mistral7b-mdmp-lora-mlx](https://huggingface.co/decisionlens/mistral7b-mdmp-lora-mlx) |
| Training pairs (optional) | [decisionlens/mdmp-staff-planning-pairs](https://huggingface.co/datasets/decisionlens/mdmp-staff-planning-pairs) |

GPU users only need the Unsloth adapter (~168 MB). Mac users only need the MLX adapter (`adapters.safetensors` + `adapter_config.json`). The matching base model downloads automatically on first run. Adapters are **not interchangeable**.

## Prerequisites

Pick one stack. Do not mix `requirements-ml.txt` and `requirements-mlx.txt` in the same venv.

- **NVIDIA GPU:** ~5–8 GB VRAM (4-bit Unsloth), Python 3.10+, CUDA and `TRITON_PTXAS_PATH`
- **Apple Silicon:** `mlx-lm` (see Mac section below). Python 3.10+

## Five-minute local chat (NVIDIA)

```bash
git clone https://github.com/dlens/mdmp-assistant.git
cd mdmp-assistant

python -m venv .venv && source .venv/bin/activate
pip install -r requirements-ml.txt

pip install huggingface_hub
hf download decisionlens/mistral7b-mdmp-lora --local-dir outputs/mistral7b-mdmp-lora

export TRITON_PTXAS_PATH=/usr/local/cuda/bin/ptxas   # adjust if your CUDA install differs
python demo/ask.py --adapter outputs/mistral7b-mdmp-lora
# optional browser UI (same GPU stack):
pip install gradio
python demo/chat_gradio.py --backend gpu --adapter outputs/mistral7b-mdmp-lora
```

Type a question at the `You:` prompt. Empty line or Ctrl+D to quit.

Omit `--backend` to auto-detect (`gpu` when `nvidia-smi` is present). First run downloads the base Mistral-7B weights (~4 GB) in addition to the adapter.

## Five-minute local chat (Apple Silicon)

No training. Download the MLX adapter (not the Unsloth one):

```bash
git clone https://github.com/dlens/mdmp-assistant.git
cd mdmp-assistant

python -m venv .venv-mlx && source .venv-mlx/bin/activate
pip install -r requirements-mlx.txt huggingface_hub

hf download decisionlens/mistral7b-mdmp-lora-mlx --local-dir outputs/mlx-mistral7b-mdmp-lora-v4
python demo/ask.py --backend mlx
# optional browser UI:
pip install gradio
python demo/chat_gradio.py --backend mlx
```

First run downloads `mlx-community/Mistral-7B-Instruct-v0.3-4bit` in addition to the adapter.

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

Apple Silicon (`requirements-mlx.txt` venv):

```python
from train.mlx_inference import load_mlx, generate_answer

model, tokenizer = load_mlx(
    model_name="mlx-community/Mistral-7B-Instruct-v0.3-4bit",
    adapter_path="outputs/mlx-mistral7b-mdmp-lora-v4",
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

The Unsloth adapter needs a local NVIDIA GPU (or your own server). The MLX adapter needs Apple Silicon.

## Coming later (optional)

| Option | Purpose |
|--------|---------|
| HF Space | Browser demo without local GPU setup |
| HF Inference Endpoint | API access for apps and integrations |

Track progress in [apphub-deploy-plan.md](apphub-deploy-plan.md). AppHub sidecar deployment is separate from HF hosting.

## More detail

- Model card (Unsloth): [hf-model-card.md](hf-model-card.md)
- Model card (MLX): [hf-model-card-mlx.md](hf-model-card-mlx.md)
- Full repo README: [README.md](../README.md)
- Re-publish Unsloth adapter: [README.md#publishing](../README.md#publishing)
- Re-publish MLX adapter: `./scripts/publish_hf_mlx.sh`
