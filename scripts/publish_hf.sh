#!/usr/bin/env bash
# Publish MDMP LoRA adapter and dataset to Hugging Face.
# Requires .env with HF_TOKEN and HF_ORG. Aborts if preflight golden eval < 14/20.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

GOLDEN_MIN_PASSED=14
ADAPTER="${ADAPTER:-outputs/mistral7b-mdmp-lora}"
DEFAULT_SOURCE_ADAPTER="/home/wjadams/Documents/bitbucket/rddocs/papers/2026/mdmp-staff-planning-assistant/outputs/mistral7b-mdmp-lora"
MODEL_REPO="${MODEL_REPO:-mistral7b-mdmp-lora}"
DATASET_REPO="${DATASET_REPO:-mdmp-staff-planning-pairs}"
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

export TRITON_PTXAS_PATH="${TRITON_PTXAS_PATH:-/usr/local/cuda/bin/ptxas}"

echo "== Preflight: leak review =="
python scripts/leak_review.py data/pairs.jsonl data/train.jsonl data/eval.jsonl

echo "== Preflight: copy-clean check =="
python scripts/copy_clean_check.py

if [[ ! -e "$ADAPTER/adapter_model.safetensors" ]]; then
  echo "Linking adapter from ${DEFAULT_SOURCE_ADAPTER}"
  mkdir -p outputs
  ln -sfn "$DEFAULT_SOURCE_ADAPTER" "$ADAPTER"
fi

PREFLIGHT_REPORT="eval/reports/v7-pre-publish.json"

if [[ "$SKIP_PREFLIGHT" != "1" ]]; then
  echo "== Preflight: golden eval (gate >= ${GOLDEN_MIN_PASSED}/20) =="
  python eval/run_golden.py \
    --adapter "$ADAPTER" \
    --label v7-pre-publish \
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
    print(f"ABORT: golden eval {passed}/{total} < {min_passed}/{total}", file=sys.stderr)
    sys.exit(1)
PY
)"
  echo "Golden gate passed: ${PASSED}/20"
else
  echo "SKIP_PREFLIGHT=1 — skipping golden eval gate"
fi

echo "== Stage artifacts =="
python scripts/stage_hf_publish.py --adapter "$DEFAULT_SOURCE_ADAPTER" --clean

if [[ "$SKIP_UPLOAD" == "1" ]]; then
  echo "SKIP_UPLOAD=1 — staging complete, upload skipped"
  exit 0
fi

echo "== Hugging Face auth check =="
hf auth whoami

MODEL_ID="${HF_ORG}/${MODEL_REPO}"
DATASET_ID="${HF_ORG}/${DATASET_REPO}"

create_repo_if_missing() {
  local repo_id="$1"
  local repo_type="$2"
  if hf repo create "$repo_id" --type "$repo_type" --exist-ok 2>/dev/null; then
    echo "Repo ready: ${repo_id} (${repo_type})"
  else
    echo "Repo create skipped or already exists: ${repo_id}"
  fi
}

echo "== Create HF repos (if needed) =="
create_repo_if_missing "$MODEL_ID" model
create_repo_if_missing "$DATASET_ID" dataset

echo "== Upload model adapter =="
hf upload "$MODEL_ID" staging/hf-model . --repo-type model

echo "== Upload dataset =="
hf upload "$DATASET_ID" staging/hf-dataset . --repo-type dataset

echo "== Post-upload verification =="
rm -rf outputs/hf-download-test
hf download "$MODEL_ID" --local-dir outputs/hf-download-test

POST_REPORT="eval/reports/hf-smoke-test.json"
python eval/run_golden.py \
  --adapter outputs/hf-download-test \
  --label hf-smoke-test \
  --out "$POST_REPORT"

python - "$POST_REPORT" "$GOLDEN_MIN_PASSED" <<'PY'
import json, sys
report_path, min_passed = sys.argv[1], int(sys.argv[2])
with open(report_path, encoding="utf-8") as f:
    report = json.load(f)
passed = int(report["passed"])
total = int(report["total"])
print(f"Post-upload golden: {passed}/{total}")
if passed < min_passed:
    print(f"ABORT: post-upload golden {passed}/{total} < {min_passed}/{total}", file=sys.stderr)
    print("Do not mark v0.1 Done or commit README HF links until fixed.", file=sys.stderr)
    sys.exit(1)
PY

echo ""
echo "Publish complete."
echo "  Model:   https://huggingface.co/${MODEL_ID}"
echo "  Dataset: https://huggingface.co/datasets/${DATASET_ID}"
