# Training data schema

Each line in `pairs.jsonl`, `train.jsonl`, or `eval.jsonl` is one JSON object (UTF-8).

## Pipeline

1. **`data/pairs.jsonl`** — human-reviewed source of truth (`reviewed: true` when ready)
2. **`python scripts/split_data.py`** — produces `train.jsonl` and `eval.jsonl` (85% / 15%)
3. **`eval/golden_questions.json`** — held-out eval set; never mixed into training

Optional: `python scripts/generate_pairs.py` writes `data/pairs_suggested.jsonl` from corpus headings for human review before appending to `pairs.jsonl`.

## Fields

| Field | Required | Description |
|-------|----------|-------------|
| `instruction` | yes | User question or task prompt |
| `input` | yes | Extra context (empty string if none) |
| `output` | yes | Ideal assistant response |
| `bucket` | yes | Category for balancing (see below) |
| `source` | yes | Corpus filename the answer is grounded in |
| `reviewed` | yes | `true` after human leak + doctrine review |

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

Golden questions in `eval/golden_questions.json` must **never** appear verbatim in training files.
