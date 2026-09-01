# Golden eval failure modes — v2 (5/20, 25%)

**Date:** 2026-07-28  
**Adapter:** `outputs/mistral7b-mdmp-lora` (153 train pairs)  
**Baseline:** 1/20 (5%)

## Summary by category

| Category | Failures | Root cause |
|----------|----------|------------|
| Step number format | 6 | Says "4th step" or "Step 3" instead of "Step 4" / "Step 2" / "Step 6" |
| War-gaming methods | 1 | Invents "Serial/Parallel" instead of belt, avenue, box |
| FASDC / screening | 1 | Describes "4-step process" without Feasible/Acceptable/Suitable |
| Decision matrix / Step 5 | 2 | Confuses war gaming (Step 4) with COA Comparison (Step 5) |
| OPORD / Orders Production | 2 | Wrong product for Step 7 or post-approval |
| Glossary (COA) | 1 | Vague definition; missing scheme of maneuver |
| Synchronization / ARC | 2 | Missing exact terms "war game" or "synchronization" |
| Repetition / hallucination | 1 | Mission analysis answer loops on "drafting evaluation criteria" |

## Per-question failures

| Question | Issue | Model said (excerpt) |
|----------|-------|----------------------|
| What MDMP step is war gaming? | Missing "Step 4", "COA Analysis" | "4th step — visualizing the battlefield…" |
| At which step do staff compare COAs against criteria? | Missing "Step 5" | "5. COA Comparison" (no "Step 5") |
| Should staff rank COAs during the war game? | Missing "Step 5" | "Yes… compare after" (wrong; also missing Step 5) |
| What is the purpose of COA screening? | Missing FASDC terms | "4-step process to screen COAs…" |
| Name three war-gaming methods. | Missing belt, avenue | Invented Serial/Parallel methods |
| What is action-reaction-counteraction used for? | Missing "war game", "synchronization" | "3-step war gaming to visualize…" |
| Where are evaluation criteria developed? | Wrong step (said Step 3) | "developed during Mission Analysis (Step 3)" |
| What is a decision matrix used for? | Missing "COA Comparison" | "4-step war gaming tool…" |
| COA development vs COA analysis? | Missing Step 3 | Described as "Step 4" process only |
| What happens after COA approval? | Missing OPORD | "Orders Production (Step 7)" only |
| When does commander select final COA? | Missing Step 6 | "4th MDMP step — COA Approval" |
| What product is produced in Step 7? | Wrong product | "1st draft of the COA Comparison Matrix" |
| What is a synchronization matrix? | Missing "war game" | Says "war gaming" but scorer needs "war game" |
| What is mission analysis in MDMP? | Missing "Step 2" | "2. Mission Analysis" without "Step 2" |
| What is a course of action (COA)? | Missing mission, scheme | "1 of the 5 MDMP steps… broad concept" |

## Fixes applied (v3 data pass)

Targeted training pairs added to teach:

- Explicit **"Step N"** phrasing (not ordinal alone)
- **belt, avenue-in-depth, box** war-gaming methods
- **Feasible, Acceptable, Suitable** in screening answers
- **war game** and **synchronization** in ARC / sync matrix answers
- **COA Comparison (Step 5)** for decision matrix
- **OPORD** and **order** for Step 7 / post-approval
- **scheme of maneuver** and **mission** in COA definitions

## v3 results (after targeted pairs)

**Date:** 2026-07-29  
**Training:** 210 pairs (178 train), train loss 2.22, eval loss 3.23  
**Overfit sanity:** eval loss 5.90 → 4.55 on 10 examples (loss drops ✓)

| Model | Golden pass |
|-------|-------------|
| Baseline | 1/20 (5%) |
| v2 | 5/20 (25%) |
| **v3** | **6/20 (30%)** |

**v3 gains vs v2:** improved on some Step-number / screening questions; still weak on war-gaming methods, ARC, sync matrix, COA definition.

**v3 regression vs v2:** lost "Can staff compare COAs head-to-head during Step 4?" (was passing).

Report: `eval/reports/v3_20260729T184358Z.json`
