---
license: apache-2.0
base_model: mistralai/Mistral-7B-Instruct-v0.3
tags:
- lora
- peft
- mdmp
- instruction-tuning
- unsloth
- military
pipeline_tag: text-generation
library_name: peft
---

# mistral7b-mdmp-lora

LoRA adapter for **MDMP staff-planning coaching** — public U.S. Army doctrine only, no proprietary algorithms or customer data.

**Disclaimer:** Unofficial educational tool. Not affiliated with the U.S. Army. Not a substitute for qualified staff planning or classified planning systems. Ground answers in FM 5-0 / ADP 5-0 and verify citations.

## Model description

This is a parameter-efficient fine-tune (LoRA) of [Mistral-7B-Instruct-v0.3](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) trained on leak-reviewed instruction pairs derived from open MDMP doctrine summaries and fictional scenarios.

- **Base model:** `mistralai/Mistral-7B-Instruct-v0.3`
- **Method:** 4-bit QLoRA via Unsloth / PEFT
- **Training data:** [mdmp-staff-planning-pairs](https://huggingface.co/datasets/decisionlens/mdmp-staff-planning-pairs) (324 reviewed pairs)
- **GitHub:** [dlens/mdmp-assistant](https://github.com/dlens/mdmp-assistant)

## Training hyperparameters

| Parameter | Value |
|-----------|-------|
| LoRA rank (r) | 16 |
| LoRA alpha | 32 |
| LoRA dropout | 0.05 |
| Epochs | 2 |
| Learning rate | 2e-4 |
| Batch size | 2 × 4 grad accum |
| Max sequence length | 2048 |

Target modules: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` (all layers).

## Evaluation

Held-out golden set (20 questions, separate from training data):

| Run | Pass rate |
|-----|-----------|
| Base Mistral-7B-Instruct-v0.3 | 1/20 (5%) |
| This adapter (Spark Unsloth v7) | 14/20 (70%) |

Eval script: [eval/run_golden.py](https://github.com/dlens/mdmp-assistant/blob/main/eval/run_golden.py)

**Quick start (inference only, no training):** [hf-quick-start.md](https://github.com/dlens/mdmp-assistant/blob/main/docs/hf-quick-start.md)

## Usage

Clone the [GitHub repo](https://github.com/dlens/mdmp-assistant), install `requirements-ml.txt`, download this adapter, then:

```python
from train.inference import load_model, generate_answer

model, tokenizer = load_model(
    model_name="mistralai/Mistral-7B-Instruct-v0.3",
    adapter_path="path/to/mistral7b-mdmp-lora",
    load_in_4bit=True,
)
answer = generate_answer(model, tokenizer, "What MDMP step is war gaming?")
print(answer)
```

Prompt format: Mistral Instruct — `<s>[INST] {question} [/INST] {answer}`

Generation defaults (match golden eval): `temperature=0.1`, `top_p=0.9`, `max_new_tokens=256`.

CLI demo:

```bash
export TRITON_PTXAS_PATH=/usr/local/cuda/bin/ptxas
python demo/ask.py --adapter path/to/mistral7b-mdmp-lora
```

**Hardware:** ~5–8 GB VRAM for 4-bit inference with adapter.

## Limitations

- Small golden eval set (n=20), English-only, U.S. MDMP framing
- Coaching assistant only — not operational planning or classified scenarios
- Automatic scoring can be brittle to near-synonyms (e.g. "synchronization" vs "synchronize")
- Users must verify operationally consequential answers against authoritative doctrine

## License

Apache 2.0 for this adapter and training data. Base model subject to [Mistral license](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3).
