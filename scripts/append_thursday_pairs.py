#!/usr/bin/env python3
"""Thursday pass: pairs targeting v3 golden failures."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAIRS_PATH = ROOT / "data" / "pairs.jsonl"

NEW_PAIRS: list[dict] = [
    # Step 4 / COA Analysis phrasing
    {"instruction": "State the step number and name for war gaming.", "input": "", "output": "War gaming is Step 4, COA Analysis.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "MDMP war gaming equals which step?", "input": "", "output": "Step 4, COA Analysis (war gaming).", "bucket": "mdmp_steps", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What is the official name of MDMP Step 4?", "input": "", "output": "Step 4 is COA Analysis, also called war gaming.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    # Step 5 without mentioning Step 4
    {"instruction": "When do staff compare all COAs against criteria?", "input": "", "output": "During Step 5, COA Comparison, using a decision matrix.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Evaluation criteria are applied across COAs in which step?", "input": "", "output": "Step 5, COA Comparison.", "bucket": "step_boundaries", "source": "coa_screening.md", "reviewed": True},
    # COA screening purpose — FASDC terms
    {"instruction": "What does COA screening verify before war gaming?", "input": "", "output": "That each COA is Feasible, Acceptable, and Suitable, plus Distinguishable and Complete (FASDC).", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Why screen COAs in Step 3?", "input": "", "output": "To confirm COAs are Feasible, Acceptable, and Suitable before Step 4 war gaming.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    # action-reaction-counteraction
    {"instruction": "What is action-reaction-counteraction in the war game?", "input": "", "output": "During the war game, action-reaction-counteraction records events in the synchronization matrix.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "How does ARC relate to synchronization?", "input": "", "output": "Action-reaction-counteraction fills the synchronization matrix during the war game.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    # Decision matrix — COA Comparison
    {"instruction": "What MDMP step uses the decision matrix?", "input": "", "output": "The decision matrix supports Step 5, COA Comparison, by comparing COAs against criteria.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Purpose of the decision matrix?", "input": "", "output": "COA Comparison (Step 5) — systematic comparison of COAs against evaluation criteria.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    # Step 3 vs Step 4
    {"instruction": "COA Development is which step number?", "input": "", "output": "Step 3, COA Development — generate and screen COAs before war gaming.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Contrast Step 3 and Step 4 in one sentence each.", "input": "", "output": "Step 3, COA Development, generates and screens COAs. Step 4, COA Analysis, war games each COA separately.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    # After COA approval — OPORD
    {"instruction": "What order is published after COA approval?", "input": "", "output": "The staff produce the OPORD during Step 7, Orders Production.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What follows Step 6 COA Approval?", "input": "", "output": "Orders Production (Step 7) — the staff issue the OPORD.", "bucket": "mdmp_steps", "source": "glossary.md", "reviewed": True},
    # Commander's intent — purpose
    {"instruction": "What two ideas does commander's intent express?", "input": "", "output": "The purpose of the operation and the desired end state.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "How should a staff officer state commander's intent?", "input": "", "output": "As a concise statement of purpose and desired end state that guides initiative.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    # Commander selects — Step 6, avoid Step 5 in short answers
    {"instruction": "Which step is COA Approval?", "input": "", "output": "Step 6, COA Approval — the commander selects the final course of action.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "The commander picks the COA at which step?", "input": "", "output": "Step 6, COA Approval.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    # Step 7 product
    {"instruction": "What does Orders Production deliver?", "input": "", "output": "The OPORD — an operations order — plus supporting order products.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Name the primary product of MDMP Step 7.", "input": "", "output": "The OPORD (operations order).", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    # Head-to-head Step 4 — lead with No
    {"instruction": "May COAs be compared head-to-head in Step 4?", "input": "", "output": "No. Step 4 war games each COA separately. Head-to-head comparison is Step 5.", "bucket": "step_boundaries", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Is side-by-side COA comparison allowed in war gaming?", "input": "", "output": "No. War gaming is Step 4; side-by-side comparison belongs in Step 5, COA Comparison.", "bucket": "step_boundaries", "source": "war_gaming.md", "reviewed": True},
    # Synchronization matrix — war game
    {"instruction": "Define synchronization matrix for Step 4.", "input": "", "output": "A war game tool that records action-reaction-counteraction to align events across time.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What is a synchronization matrix in MDMP?", "input": "", "output": "A war game matrix aligning friendly actions, reactions, and counteractions across time and space.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    # Mission analysis — Step 2
    {"instruction": "Mission analysis corresponds to which MDMP step?", "input": "", "output": "Mission analysis is Step 2 of MDMP.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What step number is Mission Analysis?", "input": "", "output": "Step 2 — Mission Analysis.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    # COA definition
    {"instruction": "Define COA for a staff planner.", "input": "", "output": "A course of action is a broad solution to accomplish the mission, with a scheme of maneuver, main effort, and key tasks.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What makes a valid COA for comparison?", "input": "", "output": "It must accomplish the mission and include a scheme of maneuver sufficient for war gaming and COA Comparison.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
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
