#!/usr/bin/env python3
"""Add targeted pairs to fix v2 golden-eval failure modes."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAIRS_PATH = ROOT / "data" / "pairs.jsonl"

NEW_PAIRS: list[dict] = [
    # Step number format — war gaming
    {"instruction": "Which step number is war gaming in MDMP?", "input": "", "output": "War gaming is Step 4, COA Analysis. Staff visualize each COA through critical events without head-to-head comparison.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Is war gaming Step 4 or COA Analysis?", "input": "", "output": "Yes — war gaming is Step 4, also called COA Analysis.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Give the step name and number for war gaming.", "input": "", "output": "Step 4, COA Analysis (war gaming).", "bucket": "mdmp_steps", "source": "war_gaming.md", "reviewed": True},
    # Step 5 / COA Comparison
    {"instruction": "What step number is COA Comparison?", "input": "", "output": "COA Comparison is Step 5. Staff compare all COAs against evaluation criteria using a decision matrix.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Staff compare COAs against evaluation criteria in which step?", "input": "", "output": "Step 5, COA Comparison — not during Step 4 war gaming.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "During which step do staff apply evaluation criteria across all COAs?", "input": "", "output": "Step 5, COA Comparison, using a decision matrix or staff brief.", "bucket": "step_boundaries", "source": "coa_screening.md", "reviewed": True},
    # Rank COAs during war game
    {"instruction": "Do staff rank COAs while conducting the war game?", "input": "", "output": "No. Do not rank COAs during the war game. Ranking and comparison belong to Step 5, COA Comparison.", "bucket": "step_boundaries", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "When should COAs be ranked against each other?", "input": "", "output": "Not during Step 4 war gaming. Staff rank or compare COAs in Step 5, COA Comparison.", "bucket": "step_boundaries", "source": "war_gaming.md", "reviewed": True},
    # COA screening / FASDC purpose
    {"instruction": "Why do staffs screen COAs with FASDC before war gaming?", "input": "", "output": "To ensure each COA is Feasible, Acceptable, and Suitable (and Distinguishable and Complete) before investing in Step 4 war gaming.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "What three FASDC criteria relate to mission worth and fit?", "input": "", "output": "Feasible (can be done with resources/time), Acceptable (worth the cost), and Suitable (accomplishes the mission within intent).", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    # War-gaming methods — belt, avenue, box
    {"instruction": "List the three doctrinal war-gaming methods.", "input": "", "output": "The belt method, avenue-in-depth method, and box method.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What are belt, avenue-in-depth, and box?", "input": "", "output": "They are the three war-gaming methods used in Step 4 COA Analysis.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Which war-gaming method uses sequential battlefield belts?", "input": "", "output": "The belt method — fighting the battlefield in sequential belts during Step 4 war gaming.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Which method follows one avenue of approach through critical events?", "input": "", "output": "The avenue-in-depth method — a Step 4 war-gaming technique.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    # Action-reaction-counteraction / synchronization
    {"instruction": "How does action-reaction-counteraction support the synchronization matrix?", "input": "", "output": "During the war game, action-reaction-counteraction records friendly actions, enemy reactions, and counteractions in the synchronization matrix across time.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What is recorded in the synchronization matrix during a war game?", "input": "", "output": "Action-reaction-counteraction sequences that align friendly and enemy events across time and space during the war game.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Describe the synchronization matrix for Step 4.", "input": "", "output": "A war game tool that uses action-reaction-counteraction to align events across time; it supports synchronization during COA Analysis.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    # Evaluation criteria — Step 2
    {"instruction": "At what step are evaluation criteria first developed?", "input": "", "output": "During Mission Analysis, Step 2. Criteria are refined after war gaming but not invented at Step 5.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Is Mission Analysis Step 2 or Step 3?", "input": "", "output": "Mission Analysis is Step 2 — where evaluation criteria are first developed.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    # Decision matrix — COA Comparison
    {"instruction": "What is the decision matrix used for in MDMP?", "input": "", "output": "The decision matrix is used in Step 5, COA Comparison, to compare COAs against evaluation criteria.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "In which step do staff use a decision matrix?", "input": "", "output": "Step 5, COA Comparison — the decision matrix compares COAs against criteria developed in Step 2.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    # COA development vs analysis — Step 3 vs Step 4
    {"instruction": "How does Step 3 COA Development differ from Step 4 COA Analysis?", "input": "", "output": "Step 3 generates and screens COAs with FASDC. Step 4 war games each COA separately to find strengths and weaknesses.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Which step generates COAs and which step war games them?", "input": "", "output": "Step 3, COA Development, generates and screens COAs. Step 4, COA Analysis, war games each COA.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    # After COA approval / Step 7 OPORD
    {"instruction": "What does the staff do after the commander approves a COA?", "input": "", "output": "The staff proceed to Step 7, Orders Production, and issue the OPORD.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What order product comes from Orders Production?", "input": "", "output": "The OPORD — an operations order produced in Step 7 after COA approval.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What is the main output of Step 7?", "input": "", "output": "Step 7, Orders Production, produces the OPORD and supporting order products.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    # Commander selects COA — Step 6
    {"instruction": "At what step does the commander select the final COA?", "input": "", "output": "Step 6, COA Approval — the commander selects or modifies the recommended COA after Step 5 comparison.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What is Step 6 of MDMP?", "input": "", "output": "Step 6 is COA Approval — the commander selects the final course of action.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    # Mission analysis — Step 2
    {"instruction": "Define mission analysis with the correct step number.", "input": "", "output": "Mission analysis is Step 2 of MDMP — analyzing the order, developing running estimates, intent, CCIRs, and evaluation criteria.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    # COA definition — mission, scheme
    {"instruction": "What is a course of action in planning terms?", "input": "", "output": "A course of action (COA) is a broad solution to accomplish the mission, including a scheme of maneuver, main effort, supporting efforts, and key tasks.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What elements must a COA include for war gaming?", "input": "", "output": "A scheme of maneuver, main effort, supporting efforts, and key tasks — enough detail to accomplish the mission and support comparison.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
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
        existing.append(row)
        seen.add(key)
        added += 1
    with PAIRS_PATH.open("w", encoding="utf-8") as f:
        for row in existing:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Added {added} pairs → {len(existing)} total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
