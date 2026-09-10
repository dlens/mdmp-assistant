---
license: apache-2.0
base_model: mlx-community/Mistral-7B-Instruct-v0.3-4bit
tags:
- lora
- mlx
- mdmp
- instruction-tuning
- military
pipeline_tag: text-generation
library_name: mlx
---

# mistral7b-mdmp-lora-mlx

Apple Silicon **MLX LoRA adapter** for MDMP staff-planning coaching — public U.S. Army doctrine only, no proprietary algorithms or customer data.

**This is not a drop-in for the Unsloth/PEFT adapter.** Use [decisionlens/mistral7b-mdmp-lora](https://huggingface.co/decisionlens/mistral7b-mdmp-lora) on NVIDIA GPUs. Adapters are not interchangeable.

**Disclaimer:** Unofficial educational tool. Not affiliated with the U.S. Army. Not a substitute for qualified staff planning or classified planning systems. Ground answers in FM 5-0 / ADP 5-0 and verify citations.

## Model description

Parameter-efficient fine-tune (LoRA) of [mlx-community/Mistral-7B-Instruct-v0.3-4bit](https://huggingface.co/mlx-community/Mistral-7B-Instruct-v0.3-4bit) via `mlx-lm`, trained on leak-reviewed instruction pairs from open MDMP doctrine summaries and fictional scenarios.

- **Base model:** `mlx-community/Mistral-7B-Instruct-v0.3-4bit`
- **Method:** 4-bit QLoRA via mlx-lm (Mac sidecar / mlx-v4)
- **Training data:** [mdmp-staff-planning-pairs](https://huggingface.co/datasets/decisionlens/mdmp-staff-planning-pairs) (324 reviewed pairs)
- **GPU sibling:** [mistral7b-mdmp-lora](https://huggingface.co/decisionlens/mistral7b-mdmp-lora) (Unsloth / PEFT)
- **GitHub:** [dlens/mdmp-assistant](https://github.com/dlens/mdmp-assistant)

## Training hyperparameters

| Parameter | Value |
|-----------|-------|
| LoRA rank | 16 |
| LoRA scale | 2.0 (`mlx-lm` multiplies the update by scale; PEFT equivalent is alpha/rank = 32/16) |
| LoRA dropout | 0.05 |
| Iters | 600 |
| Learning rate | 5e-5 (cosine decay, 20-step warmup) |
| Batch | 1 × 4 grad accum |
| Max sequence length | 2048 |
| Layers | all (`num_layers: -1`) |

Target modules: `self_attn.q_proj`, `k_proj`, `v_proj`, `o_proj`, `mlp.gate_proj`, `up_proj`, `down_proj`.

## Evaluation

Held-out golden set (20 questions, separate from training data). Score below is **this uploaded artifact** (`eval/run_golden_mlx.py`, 2026-09-01), not a copy of the Unsloth 14/20 result or an older Mac run.

| Run | Pass rate |
|-----|-----------|
| This adapter (mlx-v4, local pre-publish) | 18/20 (90%) |
| This adapter (mlx-v4, Hugging Face download) | **17/20 (85%)** |

Eval script: [eval/run_golden_mlx.py](https://github.com/dlens/mdmp-assistant/blob/main/eval/run_golden_mlx.py)

**Quick start (inference only, no training):** [hf-quick-start.md](https://github.com/dlens/mdmp-assistant/blob/main/docs/hf-quick-start.md)

## Usage

```bash
git clone https://github.com/dlens/mdmp-assistant.git
cd mdmp-assistant
python -m venv .venv-mlx && source .venv-mlx/bin/activate
pip install -r requirements-mlx.txt huggingface_hub

hf download decisionlens/mistral7b-mdmp-lora-mlx --local-dir outputs/mlx-mistral7b-mdmp-lora-v4
python demo/ask.py --backend mlx
```

Or from Python:

```python
from train.mlx_inference import load_mlx, generate_answer

model, tokenizer = load_mlx(
    model_name="mlx-community/Mistral-7B-Instruct-v0.3-4bit",
    adapter_path="outputs/mlx-mistral7b-mdmp-lora-v4",
)
print(generate_answer(model, tokenizer, "What MDMP step is war gaming?"))
```

Generation defaults (match golden eval): `temperature=0.1`, `top_p=0.9`, `max_new_tokens=256`.

**Hardware:** Apple Silicon. First run also downloads the 4-bit base weights from `mlx-community`.

## Limitations

- Small golden eval set (n=20), English-only, U.S. MDMP framing
- **Prompt fragility:** high golden pass rate does not imply robustness to paraphrase. Informal checks show truncated or off-by-one step answers on near-miss wording (e.g. “What are the steps of MDMP?” vs the golden “seven steps … in order”; “What is step 5/7?” mapping to adjacent steps). A RAG control over the same public doctrine corpus is more stable for factual step lookup; this artifact is LoRA-only.
- Coaching assistant only — not operational planning or classified scenarios
- Not interchangeable with the Unsloth adapter on Hugging Face
- Automatic scoring can be brittle to near-synonyms (e.g. "synchronization" vs "synchronize")
- Users must verify operationally consequential answers against authoritative doctrine

## License

Apache 2.0 for this adapter and training data. Base model subject to the [Mistral license](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3).
