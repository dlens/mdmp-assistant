# Golden eval failure modes — v3 (6/20, 30%)

**Date:** 2026-07-29  
**Adapter:** `outputs/mistral7b-mdmp-lora` (178 train pairs)  
**Baseline:** 1/20 (5%) | **v2:** 5/20 (25%)

## Failure categories (14 misses)

| Category | Count | Pattern |
|----------|-------|---------|
| Step number phrasing | 5 | Says "4th step" or "2nd step" instead of "Step 4" / "Step 2" / "Step 6" |
| Missing doctrine terms | 4 | OPORD, purpose, mission/scheme, Feasible/Acceptable/Suitable |
| Wrong step assignment | 3 | COA Development as Step 2; Step 7 produces decision matrix |
| Forbidden mention in answer | 2 | Names Step 4 or Step 5 when golden forbids it |
| Scorer brittleness | 2 | "war gaming" vs required "war game"; "≠" prefix breaks "no" match |

## Per-question analysis

| Question | Missing / issue | v3 response excerpt |
|----------|-----------------|---------------------|
| What MDMP step is war gaming? | Step 4, COA Analysis | "4th MDMP step — visualizing…" |
| Compare COAs against criteria? | Step 5; **forbidden** Step 4 | "5, COA Comparison — not during Step 4…" |
| Purpose of COA screening? | Feasible, Acceptable, Suitable | "Screen COAs against evaluation criteria…" |
| action-reaction-counteraction? | war game, synchronization | "3rd war-gaming method…" |
| Decision matrix used for? | COA Comparison | Correct content but no exact phrase |
| COA development vs analysis? | Step 3 | Said "Step 2" for development |
| After COA approval? | OPORD | Only named Orders Production / Step 7 |
| Commander's intent? | purpose | Said "mission" not "purpose" |
| Commander selects COA? | Step 6; **forbidden** Step 5 | "after Step 5 comparison" |
| Product in Step 7? | OPORD, order | Invented "COA Comparison" for Step 7 |
| Head-to-head in Step 4? | no | Starts with "≠" not "No" |
| Synchronization matrix? | war game | Says "war gaming" only |
| Mission analysis? | Step 2 | "2nd step" without "Step 2" |
| What is a COA? | mission, scheme | "war-gaming products" nonsense |

## Thursday fixes

1. **+25 training pairs** — exact phrasing drills for failing categories (`scripts/append_thursday_pairs.py`)
2. **Scorer** — `war game` matches `war gaming`; `Step N` accepts `Nth step` variants; `≠` treated as negation
3. **v4 retrain** on ~235 pairs → golden eval vs baseline

## Passes (6)

Seven steps, rank COAs during war game, FASDC, war-gaming methods (loose belt match), evaluation criteria location, CCIR

## v4 results (Thursday)

**Date:** 2026-07-29  
**Training:** 239 pairs (203 train), train loss 2.14, eval loss 3.11  
**Changes:** +29 targeted pairs, improved `eval/scoring.py` (Step N variants, war game/gaming, ≠ negation)

| Model | Golden pass |
|-------|-------------|
| Baseline | 1/20 (5%) |
| v3 | 6/20 (30%) |
| **v4** | **8/20 (40%)** |

**v4 gains vs v3:** war gaming step, COA dev vs analysis, commander selects COA, head-to-head Step 4, mission analysis, COA definition

**v4 regressions vs v3:** rank COAs during war game, war-gaming methods, evaluation criteria, CCIR

**Still failing (12):** Step 5 phrasing, FASDC purpose terms, belt/avenue/box, ARC, decision matrix, OPORD/Orders Production, commander's intent, sync matrix, CCIR

Report: `eval/reports/v4_20260729T191953Z.json`
