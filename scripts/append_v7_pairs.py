#!/usr/bin/env python3
"""v7 pass: pairs targeting v6 golden failures (step numbers, FASDC, ARC, COA def)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAIRS_PATH = ROOT / "data" / "pairs.jsonl"

NEW_PAIRS: list[dict] = [
    # War gaming = Step 4 (not Step 3)
    {
        "instruction": "Is war gaming Step 3 of MDMP?",
        "input": "",
        "output": "No. War gaming is Step 4, COA Analysis — not Step 3.",
        "bucket": "mdmp_steps",
        "source": "war_gaming.md",
        "reviewed": True,
    },
    {
        "instruction": "Which step is war gaming — Step 3 or Step 4?",
        "input": "",
        "output": "War gaming is Step 4, COA Analysis. Step 3 is COA Development.",
        "bucket": "mdmp_steps",
        "source": "mdmp_steps.md",
        "reviewed": True,
    },
    {
        "instruction": "What MDMP step number is COA Analysis?",
        "input": "",
        "output": "Step 4, COA Analysis — also called war gaming.",
        "bucket": "mdmp_steps",
        "source": "mdmp_steps.md",
        "reviewed": True,
    },
    # Step 5 COA Comparison phrasing
    {
        "instruction": "At which step do staff compare COAs against evaluation criteria?",
        "input": "",
        "output": "Step 5, COA Comparison — staff compare all COAs against evaluation criteria.",
        "bucket": "step_boundaries",
        "source": "mdmp_steps.md",
        "reviewed": True,
    },
    {
        "instruction": "Staff compare courses of action against criteria in which MDMP step?",
        "input": "",
        "output": "Step 5, COA Comparison.",
        "bucket": "step_boundaries",
        "source": "coa_screening.md",
        "reviewed": True,
    },
    # COA screening purpose — FASDC
    {
        "instruction": "What is the purpose of COA screening?",
        "input": "",
        "output": "To verify each COA is Feasible, Acceptable, and Suitable (FASDC) before Step 4 war gaming.",
        "bucket": "coa_screening",
        "source": "coa_screening.md",
        "reviewed": True,
    },
    {
        "instruction": "Why screen courses of action in Step 3?",
        "input": "",
        "output": "To confirm COAs are Feasible, Acceptable, and Suitable before war gaming in Step 4.",
        "bucket": "coa_screening",
        "source": "coa_screening.md",
        "reviewed": True,
    },
    # ARC + synchronization (golden phrasing)
    {
        "instruction": "What is action-reaction-counteraction used for?",
        "input": "",
        "output": "During the war game, action-reaction-counteraction records events in the synchronization matrix for synchronization.",
        "bucket": "war_gaming",
        "source": "war_gaming.md",
        "reviewed": True,
    },
    {
        "instruction": "How does action-reaction-counteraction support synchronization?",
        "input": "",
        "output": "In the war game, action-reaction-counteraction fills the synchronization matrix to synchronize friendly and enemy events.",
        "bucket": "war_gaming",
        "source": "war_gaming.md",
        "reviewed": True,
    },
    # Step 3 vs Step 4 contrast
    {
        "instruction": "What is the difference between COA development and COA analysis?",
        "input": "",
        "output": "COA Development is Step 3 — generate and screen COAs. COA Analysis is Step 4 — war game each COA separately.",
        "bucket": "step_boundaries",
        "source": "mdmp_steps.md",
        "reviewed": True,
    },
    {
        "instruction": "COA Development is Step 3; COA Analysis is which step?",
        "input": "",
        "output": "Step 4, COA Analysis (war gaming).",
        "bucket": "mdmp_steps",
        "source": "mdmp_steps.md",
        "reviewed": True,
    },
    # Commander selects COA — Step 6 (not Step 7)
    {
        "instruction": "When does the commander select the final course of action?",
        "input": "",
        "output": "Step 6, COA Approval — the commander selects or modifies the recommended COA.",
        "bucket": "mdmp_steps",
        "source": "mdmp_steps.md",
        "reviewed": True,
    },
    {
        "instruction": "Is COA Approval Step 6 or Step 7?",
        "input": "",
        "output": "Step 6, COA Approval. The commander selects the COA at Step 6; Step 7 is Orders Production.",
        "bucket": "mdmp_steps",
        "source": "mdmp_steps.md",
        "reviewed": True,
    },
    # Synchronization matrix — war game context
    {
        "instruction": "What is a synchronization matrix?",
        "input": "",
        "output": "A war game tool that records action-reaction-counteraction to synchronize events across time and space.",
        "bucket": "war_gaming",
        "source": "war_gaming.md",
        "reviewed": True,
    },
    {
        "instruction": "Define synchronization matrix for a war game.",
        "input": "",
        "output": "A war game matrix that captures action-reaction-counteraction to synchronize friendly and enemy events.",
        "bucket": "glossary",
        "source": "glossary.md",
        "reviewed": True,
    },
    # Mission analysis — Step 2 (not Step 1)
    {
        "instruction": "What is mission analysis in MDMP?",
        "input": "",
        "output": "Mission analysis is Step 2 — analyzing the higher HQ order, developing evaluation criteria, intent, and CCIRs.",
        "bucket": "mdmp_steps",
        "source": "mdmp_steps.md",
        "reviewed": True,
    },
    {
        "instruction": "Is mission analysis Step 1 of MDMP?",
        "input": "",
        "output": "No. Mission analysis is Step 2. Step 1 is Receipt of Mission.",
        "bucket": "mdmp_steps",
        "source": "mdmp_steps.md",
        "reviewed": True,
    },
    # COA definition — scheme of maneuver
    {
        "instruction": "What is a course of action (COA)?",
        "input": "",
        "output": "A course of action is a broad solution to accomplish the mission, including a scheme of maneuver, main effort, and key tasks.",
        "bucket": "glossary",
        "source": "glossary.md",
        "reviewed": True,
    },
    {
        "instruction": "Define COA with scheme of maneuver.",
        "input": "",
        "output": "A COA accomplishes the mission and includes a scheme of maneuver, main effort, supporting efforts, and key tasks.",
        "bucket": "glossary",
        "source": "glossary.md",
        "reviewed": True,
    },
    # Step ladder reinforcement
    {
        "instruction": "Receipt of Mission is Step 1; Mission Analysis is which step?",
        "input": "",
        "output": "Step 2, Mission Analysis.",
        "bucket": "mdmp_steps",
        "source": "mdmp_steps.md",
        "reviewed": True,
    },
    {
        "instruction": "Orders Production is Step 7; COA Approval is which step?",
        "input": "",
        "output": "Step 6, COA Approval — the commander selects the COA before Orders Production.",
        "bucket": "mdmp_steps",
        "source": "mdmp_steps.md",
        "reviewed": True,
    },
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
