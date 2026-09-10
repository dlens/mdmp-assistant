#!/usr/bin/env bash
# Publish the MDMP MLX LoRA adapter to Hugging Face.
# Requires .env with HF_TOKEN and HF_ORG. Aborts if MLX golden eval < 14/20.
# Does not upload the dataset or touch decisionlens/mistral7b-mdmp-lora.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

GOLDEN_MIN_PASSED=14
ADAPTER="${ADAPTER:-outputs/mlx-mistral7b-mdmp-lora-v4}"
MODEL_REPO="${MODEL_REPO:-mistral7b-mdmp-lora-mlx}"
SKIP_PREFLIGHT="${SKIP_PREFLIGHT:-0}"
SKIP_UPLOAD="${SKIP_UPLOAD:-0}"

if [[ ! -f .env ]]; then
  echo "ERROR: .env not found. Copy .env.example and set HF_TOKEN and HF_ORG." >&2
  exit 1
fi

set -a
# shellcheck disable=SC1091
source .env
set +a

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "ERROR: HF_TOKEN not set in .env" >&2
  exit 1
fi

if [[ -z "${HF_ORG:-}" ]]; then
  HF_ORG="decisionlens"
  echo "HF_ORG not set; defaulting to ${HF_ORG}"
fi

echo "== Preflight: leak review =="
python scripts/leak_review.py --tree data/pairs.jsonl data/train.jsonl data/eval.jsonl

echo "== Preflight: copy-clean check =="
python scripts/copy_clean_check.py

if [[ ! -e "$ADAPTER/adapters.safetensors" ]]; then
  echo "ERROR: MLX adapter not found at ${ADAPTER}" >&2
  echo "Train: python -m mlx_lm lora -c train/mlx_config.yaml" >&2
  exit 1
fi

PREFLIGHT_REPORT="eval/reports/mlx-v4-pre-publish.json"

if [[ "$SKIP_PREFLIGHT" != "1" ]]; then
  echo "== Preflight: MLX golden eval (gate >= ${GOLDEN_MIN_PASSED}/20) =="
  python eval/run_golden_mlx.py \
    --adapter "$ADAPTER" \
    --label mlx-v4-pre-publish \
    --out "$PREFLIGHT_REPORT"

  PASSED="$(python - "$PREFLIGHT_REPORT" "$GOLDEN_MIN_PASSED" <<'PY'
import json, sys
report_path, min_passed = sys.argv[1], int(sys.argv[2])
with open(report_path, encoding="utf-8") as f:
    report = json.load(f)
passed = int(report["passed"])
total = int(report["total"])
print(passed)
if passed < min_passed:
    print(f"ABORT: MLX golden eval {passed}/{total} < {min_passed}/{total}", file=sys.stderr)
    sys.exit(1)
PY
)"
  echo "Golden gate passed: ${PASSED}/20"
else
  echo "SKIP_PREFLIGHT=1 — skipping golden eval gate"
fi

echo "== Stage MLX artifacts =="
python scripts/stage_hf_publish_mlx.py --adapter "$ADAPTER" --clean

if [[ "$SKIP_UPLOAD" == "1" ]]; then
  echo "SKIP_UPLOAD=1 — staging complete, upload skipped"
  exit 0
fi

echo "== Hugging Face auth check =="
hf auth whoami

MODEL_ID="${HF_ORG}/${MODEL_REPO}"

create_repo_if_missing() {
  local repo_id="$1"
  if hf repo create "$repo_id" --type model --exist-ok 2>/dev/null; then
    echo "Repo ready: ${repo_id} (model)"
  else
    echo "Repo create skipped or already exists: ${repo_id}"
  fi
}

echo "== Create HF model repo (if needed) =="
create_repo_if_missing "$MODEL_ID"

echo "== Upload MLX adapter =="
hf upload "$MODEL_ID" staging/hf-model-mlx . --repo-type model

echo "== Post-upload verification =="
rm -rf outputs/hf-download-test-mlx
hf download "$MODEL_ID" --local-dir outputs/hf-download-test-mlx

POST_REPORT="eval/reports/hf-smoke-test-mlx.json"
python eval/run_golden_mlx.py \
  --adapter outputs/hf-download-test-mlx \
  --label hf-smoke-test-mlx \
  --out "$POST_REPORT"

python - "$POST_REPORT" "$GOLDEN_MIN_PASSED" <<'PY'
import json, sys
report_path, min_passed = sys.argv[1], int(sys.argv[2])
with open(report_path, encoding="utf-8") as f:
    report = json.load(f)
passed = int(report["passed"])
total = int(report["total"])
print(f"Post-upload MLX golden: {passed}/{total}")
if passed < min_passed:
    print(f"ABORT: post-upload golden {passed}/{total} < {min_passed}/{total}", file=sys.stderr)
    print("Do not mark MLX Hub publish Done until fixed.", file=sys.stderr)
    sys.exit(1)
PY

echo ""
echo "MLX publish complete."
echo "  Model: https://huggingface.co/${MODEL_ID}"
echo "  Unsloth adapter (unchanged): https://huggingface.co/${HF_ORG}/mistral7b-mdmp-lora"
