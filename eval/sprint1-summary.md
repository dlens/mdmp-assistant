# Sprint 1 Summary — MDMP Staff Planning Assistant (O1)

**Label:** sprint1  
**Sprint window:** Jul 28 – Jul 31, 2026  
**Hardware:** NVIDIA GB10 (128 GB)  
**Base model:** `mistralai/Mistral-7B-Instruct-v0.3` (4-bit, Unsloth LoRA)  
**Overview:** [README.md](../README.md)

---

## Executive summary

Sprint 1 delivered a working fine-tuning and evaluation pipeline, a 303-pair reviewed training dataset, a CLI demo, and seven golden-eval runs. Fine-tuning consistently beats the base model (5% → 55% on 20 held-out golden questions). The sprint exit target of **≥70% golden pass** was not met; best result is **v6 at 55%**.

| Goal | Target | Sprint 1 outcome |
|------|--------|----------------|
| Corpus + training pairs | 150–200 reviewed pairs | **303** reviewed pairs |
| Fine-tuned beats baseline | Yes | **Yes** (55% vs 5%) |
| Golden pass rate | ≥70% | **55%** (v6) |
| Local demo | CLI chat | **Done** (`demo/ask.py`) |
| Public v0.1 (HF publish) | Week of Aug 4 | **Not started** |

---

## Deliverables

### Corpus and data

| Asset | Count / location |
|-------|------------------|
| Doctrine markdown | 5 files (`corpus/doctrine/`) |
| Fictional scenario | 1 file (`corpus/scenarios/obj_falcon_fictional.md`) |
| Training pairs (source of truth) | **303** (`data/pairs.jsonl`) |
| Train / eval split | 258 / 45 (`scripts/split_data.py`, 85% / 15%) |
| Golden questions (held out) | 20 (`eval/golden_questions.json`) |

### Code and tooling

| Component | Path |
|-----------|------|
| Pair expansion scripts | `scripts/append_*.py`, `scripts/generate_pairs.py` |
| Conflict harmonization | `scripts/fix_conflict_pairs.py` |
| Leak guard | `scripts/leak_review.py` |
| Fine-tune | `train/finetune.py`, `train/config.yaml` |
| Golden eval + scoring | `eval/run_golden.py`, `eval/scoring.py` |
| CLI demo | `demo/ask.py` |

### Model artifacts

| Artifact | Location |
|----------|----------|
| Latest LoRA adapter | `outputs/mistral7b-mdmp-lora` |
| Overfit sanity adapter | `outputs/overfit-sanity` |
| Training / eval logs | `outputs/train_v*.log`, `outputs/eval_v*.log` |
| JSON eval reports | `eval/reports/` |

---

## Golden eval progression

All runs use the same 20 golden questions. Reports are timestamped JSON in `eval/reports/`.

| Run | Date | Train pairs | Golden pass | Notes |
|-----|------|-------------|-------------|-------|
| baseline | Jul 28 | — | 1/20 (5%) | Base Mistral-7B, no adapter |
| v1 | Jul 28 | 42 | 0/20 (0%) | Early overfit-scale train |
| v2 | Jul 28 | 153 | 5/20 (25%) | First meaningful lift |
| v3 | Jul 29 | 178 | 6/20 (30%) | Scorer improvements |
| v4 | Jul 29 | 203 | 8/20 (40%) | Best before pair harmonization |
| v5 | Jul 31 | 255 | 7/20 (35%) | 300-pair expansion; regression |
| **v6** | **Jul 31** | **258** | **11/20 (55%)** | **Pair conflict fixes + retrain** |

**v6 report:** `eval/reports/v6_20260731T223314Z.json`

### v6 passes (11)

1. Seven steps of MDMP in order  
2. Should staff rank COAs during the war game?  
3. FASDC in COA screening  
4. Three war-gaming methods  
5. Where evaluation criteria are developed  
6. Decision matrix purpose  
7. What happens after COA approval  
8. Commander's intent  
9. Product produced in Step 7  
10. Head-to-head COA comparison in Step 4  
11. CCIR meaning  

### v6 failures (9)

| Question | Failure mode |
|----------|--------------|
| What MDMP step is war gaming? | Wrong step (said Step 3, not Step 4) |
| Compare COAs against evaluation criteria? | Missing `Step 5` phrasing (`5, COA Comparison`) |
| Purpose of COA screening? | Missing FASDC terms (Feasible, Acceptable, Suitable) |
| Action-reaction-counteraction? | Describes methods, not synchronization |
| COA development vs COA analysis? | "3 steps vs 4 steps" instead of Step 3 / Step 4 |
| Commander selects final COA? | Wrong step (said Step 7, not Step 6) |
| Synchronization matrix? | Wrong step context (Step 6, not war game) |
| Mission analysis in MDMP? | Wrong step (said Step 1, not Step 2) |
| What is a COA? | Missing "scheme of maneuver" |

**Dominant remaining failure mode:** step-number phrasing — the model often prefixes answers with ordinal numbers (`3.`, `7.`) or assigns the wrong step, even when doctrinal content is partially correct.

---

## Data quality work (end of sprint)

A read-only review of 300 pairs found no hard doctrinal contradictions, but three **medium–high** conflicts on Step 4 / Step 5 boundaries:

| Removed pair | Issue |
|--------------|-------|
| OBJ FALCON criteria timing | Self-contradiction (assess in Step 4 war game *and* "not during the war game") |
| COA/criteria refinement timing | "During and after Step 4" vs corpus saying after war gaming |
| Decision matrix during war gaming | "Built during war gaming" vs pairs forbidding matrix use in Step 4 |

**Fix:** `scripts/fix_conflict_pairs.py` removed 3 conflicting pairs and added 6 harmonized replacements (net **303** pairs). Doctrine alignment:

- Step 4: per-COA qualitative notes against criteria are OK; no head-to-head COA comparison  
- Step 5: systematic cross-COA comparison and decision matrix use  
- Refinement: COAs and criteria updated **after** Step 4 completes, before Step 5  

Leak review passed on `pairs.jsonl`, `train.jsonl`, and `eval.jsonl`.

---

## Scorer and failure-mode iterations

Scoring improvements across the sprint (`eval/scoring.py`):

- `Step N` accepts variants (`Nth step`, `N. Step name`)  
- `war game` matches `war gaming`  
- `≠` prefix treated as negation for yes/no questions  

Failure-mode write-ups (pre-v6):

- `eval/failure_modes_v2.md`  
- `eval/failure_modes_v3.md` (includes v4 analysis)

---

## Training configuration (v6)

From `train/config.yaml`:

| Parameter | Value |
|-----------|-------|
| LoRA r / alpha | 16 / 32 |
| Epochs | 2 |
| Batch size | 2 × 4 grad accum = effective 8 |
| Learning rate | 2.0e-4 |
| Train loss (v6) | 1.987 |
| Eval loss (v6) | 3.352 |
| Train runtime (v6) | ~109 s on GB10 |

---

## Git history (committed)

| Commit | Summary |
|--------|---------|
| `c3905df0` | Sprint scaffold, corpus, 180 pairs, train/eval pipeline |
| `08efb972` | Expand to 239 pairs; golden eval improvements for v4 |
| `ef1c096a` | Expand to 300 pairs; scorer enhancements; CLI demo |

**Uncommitted at sprint close:** pair harmonization (303 pairs), v6 train/eval, `scripts/fix_conflict_pairs.py`, this summary.

---

## Sprint exit assessment

| Criterion | Met? |
|-----------|------|
| Working LoRA adapter | Yes |
| Local demo | Yes |
| Fine-tuned beats base on golden set | Yes (+50 pp vs baseline) |
| ≥70% golden pass | **No** (55%) |
| Leak-review clean | Yes |
| Hugging Face publish | No (deferred to public v0.1) |

---

## Recommended next steps (Sprint 2 / public v0.1)

1. **Step-number drill pairs** — targeted Q&A requiring exact `Step N` phrasing for Steps 2, 4, 5, 6, 7  
2. **COA definition and screening** — pairs with FASDC terms and "scheme of maneuver"  
3. **ARC / synchronization matrix** — tie action-reaction-counteraction to synchronization matrix in Step 4  
4. **Retrain (v7)** and re-run golden eval; target ≥70% sprint / ≥80% public v0.1  
5. **Update README** golden-eval table to reflect v6 as current best  
6. **Commit** harmonized pairs + sprint1 summary  
7. **HF publish** — model card, dataset, adapter weights (public v0.1 milestone)

---

## Key commands

```bash
export TRITON_PTXAS_PATH=/usr/local/cuda/bin/ptxas
cd mdmp-staff-planning-assistant

python scripts/split_data.py
python train/finetune.py
python eval/run_golden.py --adapter outputs/mistral7b-mdmp-lora --label vN
python demo/ask.py
python scripts/leak_review.py data/pairs.jsonl data/train.jsonl data/eval.jsonl
```

---

## v7 cycle (Aug 3, 2026)

**Target:** Close v6 golden gaps with 21 targeted pairs → retrain → eval.

| Metric | v6 | v7 |
|--------|----|----|
| Training pairs | 258 | 275 |
| Golden pass | 11/20 (55%) | **14/20 (70%)** |
| Sprint ≥70% target | No | **Yes** |

**Script:** `scripts/append_v7_pairs.py` (21 pairs, 303 → 324 total)

### v7 gains vs v6 (+5)

- What MDMP step is war gaming?
- What is the difference between COA development and COA analysis?
- What is a synchronization matrix?
- What is mission analysis in MDMP?
- What is a course of action (COA)?

### v7 regressions vs v6 (−2)

- Where are evaluation criteria developed?
- What is a decision matrix used for?

### v7 remaining failures (6)

| Question | Issue |
|----------|-------|
| Compare COAs against criteria? | `5, COA Comparison` — scorer wants `Step 5` |
| Purpose of COA screening? | Missing FASDC terms |
| Action-reaction-counteraction? | Says "synchronize" not "synchronization" (scorer brittleness) |
| Where are evaluation criteria developed? | Wrong step (Step 3 vs Step 2) |
| Decision matrix used for? | Wrong step (Step 4 vs Step 5) |
| Commander selects COA? | `6.3, COA Approval` — scorer wants `Step 6` |

**v7 report:** `eval/reports/v7_20260803T160101Z.json`

**Next for public v0.1 (≥80%):** Fix 6 remaining failures; consider scorer tweak for `synchronize`/`synchronization`; expand golden set to 25–30 after stable pass on original 20.
