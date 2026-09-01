---
license: apache-2.0
tags:
- mdmp
- instruction-tuning
- military
task_categories:
- question-answering
language:
- en
size_categories:
- n<1K
---

# mdmp-staff-planning-pairs

Leak-reviewed instruction-tuning pairs for MDMP staff-planning coaching. Public doctrine summaries and fictional scenarios only — no proprietary algorithms, customer data, or classified content.

**Disclaimer:** Unofficial educational dataset. Not affiliated with the U.S. Army.

## Dataset description

324 human-reviewed `{instruction, input, output}` pairs for fine-tuning a Mistral-7B instruct model on Military Decision-Making Process vocabulary, step boundaries, and coaching responses.

- **GitHub source:** [dlens/mdmp-assistant](https://github.com/dlens/mdmp-assistant)
- **Model trained on this data:** [mistral7b-mdmp-lora](https://huggingface.co/decisionlens/mistral7b-mdmp-lora)

## Fields

| Field | Description |
|-------|-------------|
| `instruction` | User question or task prompt |
| `input` | Extra context (empty string if none) |
| `output` | Ideal assistant response |
| `bucket` | Category for balancing (see below) |
| `source` | Corpus filename the answer is grounded in |
| `reviewed` | `true` after human leak + doctrine review |

## Buckets

- `mdmp_steps` — step identification and ordering
- `step_boundaries` — Step 4 vs Step 5 and related traps
- `glossary` — term definitions
- `war_gaming` — methods, synchronization matrix
- `coa_screening` — FASDC, criteria development
- `scenario_coaching` — fictional scenario trade-offs

## Example

```json
{"instruction": "What MDMP step is war gaming?", "input": "", "output": "War gaming is Step 4, COA Analysis. Staff visualize each COA through critical events and record strengths and weaknesses without head-to-head COA comparison; comparison belongs in Step 5.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": true}
```

## Leak-review policy

Before inclusion, each pair is checked for:

- Customer names, OPNAV, or real unit designations
- Proprietary algorithm or product terms
- Verbatim golden-eval questions (held out in `eval/golden_questions.json` on GitHub)

See [scripts/leak_review.py](https://github.com/dlens/mdmp-assistant/blob/main/scripts/leak_review.py).

## Usage

```python
import json

pairs = []
with open("pairs.jsonl", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            pairs.append(json.loads(line))
```

Split into train/eval with [scripts/split_data.py](https://github.com/dlens/mdmp-assistant/blob/main/scripts/split_data.py) (85% / 15%).

## License

Apache 2.0
