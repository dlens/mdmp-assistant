#!/usr/bin/env python3
"""Expand pairs.jsonl to ~300 with v4 failure-targeted and paraphrase pairs."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAIRS_PATH = ROOT / "data" / "pairs.jsonl"
TARGET = 300

NEW_PAIRS: list[dict] = [
    # Step 5 / COA Comparison (avoid forbidden "war game" in some answers)
    {"instruction": "Staff apply evaluation criteria to all COAs in what step?", "input": "", "output": "Step 5, COA Comparison, using a decision matrix or staff brief.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What is the fifth step of MDMP?", "input": "", "output": "Step 5 is COA Comparison — comparing all COAs against evaluation criteria.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "When is the decision matrix completed?", "input": "", "output": "During Step 5, COA Comparison, after each COA has been analyzed separately in Step 4.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Explain Step 5 to a new captain.", "input": "", "output": "Step 5, COA Comparison, is when staff compare all surviving COAs against the evaluation criteria developed in Step 2.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "COA Comparison happens at which numbered step?", "input": "", "output": "Step 5.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    # Rank COAs — No + Step 5
    {"instruction": "Is ranking COAs part of Step 4?", "input": "", "output": "No. Ranking or comparing COAs belongs to Step 5, COA Comparison, not Step 4.", "bucket": "step_boundaries", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "When do staff rank courses of action?", "input": "", "output": "Staff rank or compare COAs in Step 5 after completing Step 4 analysis of each COA.", "bucket": "step_boundaries", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Can the war game produce a COA winner?", "input": "", "output": "No. Step 4 records strengths and weaknesses per COA. A recommendation comes from Step 5 comparison; the commander decides at Step 6.", "bucket": "step_boundaries", "source": "war_gaming.md", "reviewed": True},
    # FASDC / screening purpose
    {"instruction": "What is COA screening looking for?", "input": "", "output": "COAs that are Feasible, Acceptable, Suitable, Distinguishable, and Complete before Step 4.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Why use Feasible, Acceptable, and Suitable in Step 3?", "input": "", "output": "To ensure each COA can be executed, is worth the cost, and fits the mission and intent before war gaming.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Screen COAs for what three qualities at minimum?", "input": "", "output": "Feasible, Acceptable, and Suitable — core FASDC screening checks.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "How does FASDC help the staff in COA Development?", "input": "", "output": "FASDC confirms each COA is Feasible, Acceptable, Suitable, Distinguishable, and Complete before analysis.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    # War-gaming methods — belt, avenue, box
    {"instruction": "What war-gaming method uses sequential belts?", "input": "", "output": "The belt method — progressing through the battlefield in belts during Step 4.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Give an example of when to use the box method.", "input": "", "output": "Use the box method to focus Step 4 analysis on a defined objective area such as a river crossing or engagement area.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What three methods does FM 5-0 describe for war gaming?", "input": "", "output": "Belt, avenue-in-depth, and box methods.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "How does avenue-in-depth differ from the belt method?", "input": "", "output": "Avenue-in-depth follows one avenue through critical events; the belt method advances through sequential geographic belts.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Which war-gaming methods should I list on an exam?", "input": "", "output": "Belt, avenue-in-depth, and box.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    # ARC + synchronization
    {"instruction": "Why record action, reaction, and counteraction?", "input": "", "output": "To capture how the fight unfolds in the synchronization matrix during the war game.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What tool captures action-reaction-counteraction?", "input": "", "output": "The synchronization matrix during the war game in Step 4.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "How does synchronization support Step 4?", "input": "", "output": "The synchronization matrix aligns friendly actions, reactions, and counteractions across time during the war game.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Describe action-reaction-counteraction briefly.", "input": "", "output": "Friendly action, enemy reaction, friendly counteraction — recorded in the synchronization matrix during the war game.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    # Evaluation criteria — Step 2, Mission Analysis
    {"instruction": "Where do COA evaluation criteria originate?", "input": "", "output": "In Mission Analysis, Step 2, and they may be refined after Step 4.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Are evaluation criteria created in COA Comparison?", "input": "", "output": "No. They are developed in Mission Analysis (Step 2) and applied in Step 5.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Mission Analysis produces what comparison inputs?", "input": "", "output": "Evaluation criteria developed in Step 2 for use in Step 5 COA Comparison.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Step 2 outputs that Step 5 needs?", "input": "", "output": "Evaluation criteria — developed during Mission Analysis (Step 2) and refined after war gaming.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    # Decision matrix — COA Comparison
    {"instruction": "What step owns the decision matrix?", "input": "", "output": "Step 5, COA Comparison — the matrix compares COAs against criteria.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "How does staff use a decision matrix?", "input": "", "output": "In COA Comparison (Step 5) to compare each COA against evaluation criteria and support a recommendation.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Is the decision matrix a Step 4 product?", "input": "", "output": "No. War gaming in Step 4 feeds it, but the decision matrix is used in Step 5, COA Comparison.", "bucket": "step_boundaries", "source": "coa_screening.md", "reviewed": True},
    # After COA approval / OPORD
    {"instruction": "What step issues the OPORD?", "input": "", "output": "Step 7, Orders Production, after COA Approval at Step 6.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "After Step 6 what does the staff produce?", "input": "", "output": "Orders Production (Step 7) — the OPORD and supporting order products.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What happens in Orders Production?", "input": "", "output": "The staff produce the OPORD and supporting products to execute the approved COA.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Name the order type from Step 7.", "input": "", "output": "OPORD — operations order.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    # Commander's intent — purpose, end state
    {"instruction": "What should commander's intent include?", "input": "", "output": "The purpose of the operation and the desired end state.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "Why does the staff need commander's intent?", "input": "", "output": "Intent states purpose and end state so subordinates exercise initiative when the plan changes.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "Is commander's intent the same as the OPORD?", "input": "", "output": "No. Intent is drafted in Mission Analysis; the OPORD is produced in Step 7 after COA approval.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    # CCIR
    {"instruction": "Define CCIR for a staff brief.", "input": "", "output": "Commander's critical information requirement — critical information the Commander needs for timely decisions.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What information does a CCIR provide?", "input": "", "output": "Critical information the Commander needs to decide in time.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "When are CCIRs first developed?", "input": "", "output": "During Mission Analysis (Step 2) as part of the running estimate and planning products.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    # Synchronization matrix
    {"instruction": "What is the synchronization matrix used for in Step 4?", "input": "", "output": "A war game tool recording action-reaction-counteraction to align events across time and space.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "How do staff use a synchronization matrix?", "input": "", "output": "During the war game to track friendly actions, enemy reactions, and counteractions over time.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    # COA definition
    {"instruction": "What is included in a course of action?", "input": "", "output": "A scheme of maneuver, main effort, supporting efforts, and key tasks to accomplish the mission.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "How is a COA different from a concept of operations sketch?", "input": "", "output": "A COA is a complete planning solution with scheme of maneuver and tasks sufficient to accomplish the mission and support comparison.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What does scheme of maneuver mean in a COA?", "input": "", "output": "How friendly forces move and fight to accomplish the mission — a core element of every COA.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    # Scenario coaching — expand OBJ FALCON
    {"instruction": "Which OBJ FALCON COA uses deception?", "input": "", "output": "COA-D Feint and Main — demonstration north, main attack south with deception.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "How does COA-B score on simplicity in OBJ FALCON?", "input": "", "output": "COA-B Double Envelopment typically scores lower on simplicity due to fixing and flanking coordination.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "What is the main effort in COA-A for OBJ FALCON?", "input": "", "output": "Highway 12 axis direct assault with a supporting attack to fix forward.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "Why might staff reject COA-E for OBJ FALCON mission accomplishment?", "input": "", "output": "COA-E Turning Movement bypasses the crossing and may score lower on seizing OBJ FALCON directly.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "What criteria apply in the OBJ FALCON decision matrix?", "input": "", "output": "Mission Accomplishment, Speed to Objective, Enemy Disruption, and Simplicity — applied in Step 5.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "Should OBJ FALCON COAs be compared during Step 4?", "input": "", "output": "No. War game each COA in Step 4, then compare in Step 5 using the four evaluation criteria.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "Which COA best balances disruption and simplicity at OBJ FALCON?", "input": "", "output": "COA-A tends toward simplicity; COA-B toward disruption — compare both in Step 5 against those criteria.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "What is the 3rd BCT mission at OBJ FALCON?", "input": "", "output": "Seize the river crossing and town center within 36 hours to restore freedom of movement.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    # Additional step boundary paraphrases
    {"instruction": "Does Step 4 include COA Comparison?", "input": "", "output": "No. Step 4 is COA Analysis (war gaming). COA Comparison is Step 5.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Is Mission Analysis Step 1 or Step 2?", "input": "", "output": "Step 2. Step 1 is Receipt of Mission.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What step is Receipt of Mission?", "input": "", "output": "Step 1 — alerting the staff and beginning MDMP.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What step is Orders Production?", "input": "", "output": "Step 7 — producing the OPORD after COA Approval.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Between which steps does the commander approve a COA?", "input": "", "output": "Step 6, COA Approval, between Step 5 comparison and Step 7 orders production.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    # War gaming process
    {"instruction": "What do staff do first in Step 4?", "input": "", "output": "List forces, assumptions, critical events, and decision points; choose a war-gaming method; then fight each COA.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Can staff refine COAs after war gaming?", "input": "", "output": "Yes. Step 4 findings refine COAs and evaluation criteria before Step 5 comparison.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What is a critical event in war gaming?", "input": "", "output": "A key point in the operation where the COA succeeds, fails, or requires a decision — visualized in Step 4.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    # FASDC complete/distinguishable
    {"instruction": "What does Complete mean in FASDC?", "input": "", "output": "The COA addresses decisive, shaping, and sustaining operations as required.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Why must COAs be Distinguishable?", "input": "", "output": "So the staff compare meaningfully different options, not minor variants of the same plan.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "How many COAs should survive FASDC screening?", "input": "", "output": "Typically two to three viable COAs worth war gaming in Step 4, though staff may start with more.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    # Mixed paraphrase drills
    {"instruction": "Quick answer: MDMP step for COA Comparison?", "input": "", "output": "Step 5.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Quick answer: three war-gaming methods?", "input": "", "output": "Belt, avenue-in-depth, box.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Quick answer: FASDC letters?", "input": "", "output": "Feasible, Acceptable, Suitable, Distinguishable, Complete.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Quick answer: Step 7 product?", "input": "", "output": "OPORD.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Quick answer: where are criteria developed?", "input": "", "output": "Step 2, Mission Analysis.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
]


def main() -> int:
    existing: list[dict] = []
    if PAIRS_PATH.exists():
        with PAIRS_PATH.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    existing.append(json.loads(line))
    seen = {r["instruction"].strip().lower() for r in existing}
    added = 0
    for row in NEW_PAIRS:
        key = row["instruction"].strip().lower()
        if key in seen:
            continue
        if len(existing) >= TARGET:
            break
        existing.append(row)
        seen.add(key)
        added += 1
    with PAIRS_PATH.open("w", encoding="utf-8") as f:
        for row in existing:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Added {added} pairs → {len(existing)} total (target {TARGET})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
