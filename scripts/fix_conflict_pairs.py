#!/usr/bin/env python3
"""Remove conflicting pairs and add doctrine-consistent replacements."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAIRS_PATH = ROOT / "data" / "pairs.jsonl"

REMOVE_INSTRUCTIONS = {
    "in obj falcon, when do staff apply the four evaluation criteria across coas?",
    "when are coas refined based on war-game findings?",
    "should the decision matrix be built during war gaming?",
}

REPLACEMENTS: list[dict] = [
  {
    "instruction": "In OBJ FALCON, when do staff compare COAs against the four evaluation criteria?",
    "input": "",
    "output": "In Step 5, COA Comparison. During Step 4, staff war-game each COA separately and record how that COA might perform against each criterion — without comparing COAs head-to-head.",
    "bucket": "scenario_coaching",
    "source": "obj_falcon_fictional.md",
    "reviewed": True,
  },
  {
    "instruction": "How should OBJ FALCON staff handle criteria during Step 4 versus Step 5?",
    "input": "",
    "output": "Step 4: assess each COA alone against Mission Accomplishment, Speed to Objective, Enemy Disruption, and Simplicity. Step 5: compare all COAs systematically in the decision matrix.",
    "bucket": "scenario_coaching",
    "source": "obj_falcon_fictional.md",
    "reviewed": True,
  },
  {
    "instruction": "When are COAs and evaluation criteria updated after war gaming?",
    "input": "",
    "output": "After Step 4 war gaming is complete, staff may refine COAs and evaluation criteria before Step 5 COA Comparison.",
    "bucket": "mdmp_steps",
    "source": "mdmp_steps.md",
    "reviewed": True,
  },
  {
    "instruction": "Does Step 4 refine evaluation criteria during the war game?",
    "input": "",
    "output": "Step 4 may reveal needed refinements, but staff update COAs and criteria after completing war gaming and before Step 5 comparison.",
    "bucket": "war_gaming",
    "source": "war_gaming.md",
    "reviewed": True,
  },
  {
    "instruction": "Where do decision matrix inputs come from?",
    "input": "",
    "output": "From Step 4 war-game findings — strengths, weaknesses, and per-COA observations. Staff enter those inputs into the decision matrix during Step 5, COA Comparison.",
    "bucket": "step_boundaries",
    "source": "coa_screening.md",
    "reviewed": True,
  },
  {
    "instruction": "Is the decision matrix completed in Step 4 or Step 5?",
    "input": "",
    "output": "Step 5, COA Comparison. Step 4 produces per-COA analysis that feeds the matrix; staff do not complete systematic COA comparison in Step 4.",
    "bucket": "step_boundaries",
    "source": "coa_screening.md",
    "reviewed": True,
  },
]


def main() -> int:
    rows: list[dict] = []
    removed = 0
    with PAIRS_PATH.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            key = row["instruction"].strip().lower()
            if key in REMOVE_INSTRUCTIONS:
                removed += 1
                continue
            rows.append(row)

    seen = {r["instruction"].strip().lower() for r in rows}
    added = 0
    for row in REPLACEMENTS:
        key = row["instruction"].strip().lower()
        if key in seen:
            continue
        rows.append(row)
        seen.add(key)
        added += 1

    with PAIRS_PATH.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Removed {removed} conflicting pairs")
    print(f"Added {added} replacement pairs")
    print(f"Total: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
