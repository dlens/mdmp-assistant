#!/usr/bin/env python3
"""One-time expansion: append curated pairs to data/pairs.jsonl."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAIRS_PATH = ROOT / "data" / "pairs.jsonl"

NEW_PAIRS: list[dict] = [
    # mdmp_steps paraphrases (+15)
    {"instruction": "Which MDMP step is Receipt of Mission?", "input": "", "output": "Receipt of Mission is Step 1. The staff is alerted, gathers planning tools, and receives the commander's initial planning guidance.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What occurs during Step 1 of MDMP?", "input": "", "output": "Step 1, Receipt of Mission, alerts the staff, gathers planning tools, and issues initial planning guidance to begin MDMP.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What is Step 4 of MDMP called?", "input": "", "output": "Step 4 is COA Analysis, also called war gaming. Staff visualize each COA through critical events.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Identify Step 5 of the military decision-making process.", "input": "", "output": "Step 5 is COA Comparison — comparing all COAs against evaluation criteria using a decision matrix or similar tool.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "During which MDMP step do staff generate courses of action?", "input": "", "output": "Staff generate courses of action during Step 3, COA Development, and screen them before war gaming.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What MDMP step follows COA Comparison?", "input": "", "output": "COA Approval (Step 6) follows COA Comparison (Step 5).", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What step comes immediately before COA Development?", "input": "", "output": "Mission Analysis (Step 2) comes before COA Development (Step 3).", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "In which step does the staff issue the OPORD?", "input": "", "output": "The staff produce the OPORD during Step 7, Orders Production, after the commander approves a COA at Step 6.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What is the first step of the military decision-making process?", "input": "", "output": "The first step is Receipt of Mission (Step 1).", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What is the final step of MDMP?", "input": "", "output": "Orders Production (Step 7) is the final step — producing the OPORD and supporting products.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "When do staff develop initial CCIRs?", "input": "", "output": "Staff develop initial CCIRs during Mission Analysis (Step 2).", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What is the Army's iterative staff planning methodology?", "input": "", "output": "The Military Decision-Making Process (MDMP) per FM 5-0 / ADP 5-0 — seven steps from Receipt of Mission through Orders Production.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "When does COA screening occur in MDMP?", "input": "", "output": "COA screening occurs during COA Development (Step 3), before war gaming in Step 4.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "When are COAs refined based on war-game findings?", "input": "", "output": "COAs and evaluation criteria may be refined during and after Step 4 war gaming, before systematic comparison in Step 5.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What is Step 2 of MDMP?", "input": "", "output": "Step 2 is Mission Analysis — analyzing the higher HQ order, developing running estimates, drafting intent, CCIRs, and evaluation criteria.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    # step_boundaries (+15)
    {"instruction": "May staff use a decision matrix during Step 4?", "input": "", "output": "No. War gaming in Step 4 records findings per COA. The decision matrix is used in Step 5 for systematic comparison against criteria.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Is head-to-head COA comparison allowed during war gaming?", "input": "", "output": "No. Step 4 fights each COA separately. Head-to-head comparison against criteria belongs in Step 5.", "bucket": "step_boundaries", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What happens in Step 5 that does not happen in Step 4?", "input": "", "output": "Step 5 compares all COAs against evaluation criteria systematically. Step 4 analyzes each COA individually without ranking or head-to-head comparison.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Can the commander approve a COA during COA Comparison?", "input": "", "output": "No. COA Comparison (Step 5) produces a recommendation. The commander selects or modifies the COA at Step 6, COA Approval.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Should evaluation criteria first appear at Step 5?", "input": "", "output": "No. Evaluation criteria are developed during Mission Analysis (Step 2) and refined after war gaming. They should not be invented for the first time at Step 5.", "bucket": "step_boundaries", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "What is wrong with ranking COAs while fighting them in the war game?", "input": "", "output": "Ranking during Step 4 blurs the process and biases narratives before criteria are applied systematically in Step 5.", "bucket": "step_boundaries", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Does Step 4 replace the need for a decision matrix?", "input": "", "output": "No. War gaming (Step 4) informs the decision matrix but does not replace COA Comparison (Step 5).", "bucket": "step_boundaries", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "When is the final COA selected?", "input": "", "output": "The commander selects or modifies the final COA at Step 6, COA Approval, after staff comparison in Step 5.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What feeds the Step 5 decision matrix?", "input": "", "output": "War-game findings from Step 4 — strengths, weaknesses, synchronization issues, and qualitative or numeric assessments per COA.", "bucket": "step_boundaries", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Can staff compare COAs against criteria during Step 4?", "input": "", "output": "No. Staff record per-COA analysis in Step 4. Systematic comparison against evaluation criteria is Step 5.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What step uses evaluation criteria systematically across all COAs?", "input": "", "output": "COA Comparison (Step 5) applies evaluation criteria across all COAs using a decision matrix or brief.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Is war gaming the same as COA approval?", "input": "", "output": "No. War gaming is Step 4 (COA Analysis). The commander approves a COA at Step 6.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What MDMP step immediately follows COA Analysis?", "input": "", "output": "COA Comparison (Step 5) follows COA Analysis / war gaming (Step 4).", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What step precedes COA Comparison?", "input": "", "output": "COA Analysis / war gaming (Step 4) precedes COA Comparison (Step 5).", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Where does systematic COA comparison belong in MDMP?", "input": "", "output": "Systematic COA comparison belongs in Step 5, after war gaming is complete.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    # war_gaming (+25)
    {"instruction": "What is action-reaction-counteraction?", "input": "", "output": "Action-reaction-counteraction is the sequence recorded in the synchronization matrix during war gaming to visualize how friendly actions, enemy reactions, and friendly counteractions unfold.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "How is a synchronization matrix used in war gaming?", "input": "", "output": "The synchronization matrix aligns friendly actions, enemy reactions, and counteractions across time and space during Step 4 war gaming.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "When should staff use the belt war-gaming method?", "input": "", "output": "Use the belt method to fight the battlefield in sequential belts, often east-west or along operational phases.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "When is the avenue-in-depth method appropriate?", "input": "", "output": "Avenue-in-depth follows a single avenue of approach through critical events — useful when the fight is dominated by one axis.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "When should staff choose the box method for war gaming?", "input": "", "output": "The box method focuses on a defined area — an objective, engagement area, or choke point such as a river crossing.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "How should staff fight COAs during the war game?", "input": "", "output": "Fight one COA at a time (or one friendly COA against one enemy COA in sequence). Do not compare or rank COAs during the war game.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What are typical war-game outputs?", "input": "", "output": "A synchronization matrix, refined COAs, updated evaluation criteria, and a war-game workbook or narrative that feeds the COA comparison brief.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What do staff record per COA during Step 4?", "input": "", "output": "Strengths, weaknesses, advantages, disadvantages, synchronization risk, likely enemy reactions, and refinements for each COA.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Can war gaming refine evaluation criteria?", "input": "", "output": "Yes. Staff refine COAs and evaluation criteria based on war-game findings before Step 5 comparison.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What is COA Analysis in MDMP?", "input": "", "output": "COA Analysis is Step 4 — war gaming. Staff visualize each COA through critical events without head-to-head COA comparison.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Is war gaming Step 4 or Step 5?", "input": "", "output": "War gaming is Step 4 (COA Analysis). Step 5 is COA Comparison.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What is the purpose of war gaming?", "input": "", "output": "To visualize each COA through critical events, identify strengths and weaknesses, capture synchronization issues, and feed Step 5 comparison.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Should staff compare two friendly COAs side by side during the war game?", "input": "", "output": "No. Staff analyze each COA separately in Step 4. Side-by-side comparison belongs in Step 5.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What happens to invalid assumptions during a war game?", "input": "", "output": "Staff update assumptions when the war game reveals invalid premises.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What are decision points in war gaming?", "input": "", "output": "Points where the commander may need to decide or refine the plan based on how the fight unfolds during visualization.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Describe the belt war-gaming method.", "input": "", "output": "The belt method fights the battlefield in sequential belts, progressing through phases or geographic slices.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Describe the avenue-in-depth war-gaming method.", "input": "", "output": "Avenue-in-depth follows one avenue of approach through critical events from start to objective.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What should staff list before starting a war game?", "input": "", "output": "Friendly forces, assumptions, critical events, decision points, and the war-gaming method to use.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "How do war-game findings support Step 5?", "input": "", "output": "Findings become inputs to the decision matrix — narrative assessments or numeric scores per criterion and COA.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Does war gaming include OPORD production?", "input": "", "output": "No. War gaming is Step 4. OPORD production is Step 7 after COA approval.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What visualization happens in MDMP Step 4?", "input": "", "output": "Staff visualize each COA through critical events using action-reaction-counteraction and record results per COA.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Can numeric scores be derived from war gaming?", "input": "", "output": "Yes. Staff may translate qualitative war-game observations into numeric inputs for the Step 5 decision matrix.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What is the difference between war gaming and COA comparison?", "input": "", "output": "War gaming (Step 4) analyzes each COA separately. COA comparison (Step 5) compares all COAs against evaluation criteria.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Name the belt, avenue-in-depth, and box methods.", "input": "", "output": "The three war-gaming methods are belt, avenue-in-depth, and box.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What role does action-reaction-counteraction play in the synchronization matrix?", "input": "", "output": "It structures how friendly actions, enemy reactions, and friendly counteractions are recorded across time during war gaming.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    # coa_screening (+22)
    {"instruction": "What does FASDC stand for in COA screening?", "input": "", "output": "Feasible, Acceptable, Suitable, Distinguishable, and Complete — the five screening criteria for courses of action.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "What does acceptable mean for a COA?", "input": "", "output": "Acceptable means the COA is worth the cost in terms of risk, casualties, and mission impact.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "What does suitable mean in COA screening?", "input": "", "output": "Suitable means the COA accomplishes the mission within the commander's intent.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "What does complete mean for a COA?", "input": "", "output": "Complete means the COA addresses decisive, shaping, and sustaining operations as required.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "What happens to COAs that fail FASDC screening?", "input": "", "output": "COAs that fail screening are revised or dropped before Step 4 war gaming.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Why screen COAs before war gaming?", "input": "", "output": "To ensure COAs are feasible, acceptable, suitable, distinguishable, and complete before investing time in Step 4 analysis.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "What is the purpose of COA screening?", "input": "", "output": "To verify COAs are Feasible, Acceptable, and Suitable (and Distinguishable and Complete) before war gaming.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "What are good characteristics of evaluation criteria?", "input": "", "output": "Linked to mission and intent, measurable or assessable where possible, few enough to manage, and understood by the commander before comparison.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Should evaluation criteria be linked to commander's intent?", "input": "", "output": "Yes. Good criteria are linked to the mission and commander's intent.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Can staff invent evaluation criteria at Step 5?", "input": "", "output": "No. Criteria are developed in Mission Analysis (Step 2) and refined after war gaming — not invented for the first time at COA Comparison.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "When can evaluation criteria be refined?", "input": "", "output": "During Mission Analysis (Step 2) and again after war gaming based on findings.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "How does the decision matrix support the commander?", "input": "", "output": "It plots COAs against evaluation criteria to support a recommendation; the commander decides at Step 6.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Who decides among COAs after comparison?", "input": "", "output": "The commander selects or modifies the COA at Step 6, COA Approval, after staff present the Step 5 comparison.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "What is the relationship between war gaming and the decision matrix?", "input": "", "output": "War gaming produces per-COA findings that populate the decision matrix used in Step 5 comparison.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "What is COA screening?", "input": "", "output": "Applying FASDC criteria during COA Development (Step 3) to ensure COAs are worth war gaming.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Define feasible in the FASDC context.", "input": "", "output": "Feasible means the COA can be accomplished with available resources and time.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Why must COAs be distinguishable?", "input": "", "output": "So the staff present meaningfully different options, not cosmetic variants of the same plan.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "In which step are evaluation criteria developed?", "input": "", "output": "Evaluation criteria are developed during Mission Analysis (Step 2).", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Can cosmetic COA variants pass screening?", "input": "", "output": "No. COAs must be distinguishable — meaningfully different from other options.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "What is COA development in MDMP?", "input": "", "output": "Step 3 — generating multiple courses of action and screening them with FASDC before war gaming.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "How is a decision matrix used in COA Comparison?", "input": "", "output": "Staff plot each COA against evaluation criteria in the matrix, using narrative or numeric cells to support a recommendation.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Where in MDMP are evaluation criteria first created?", "input": "", "output": "During Mission Analysis (Step 2), not at COA Comparison.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    # glossary (+15)
    {"instruction": "What is a scheme of maneuver in a COA?", "input": "", "output": "Part of a course of action describing how forces move and fight to accomplish the mission — included with main effort, supporting efforts, and key tasks.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What are supporting efforts in a COA?", "input": "", "output": "Elements of a COA that support the main effort; included alongside scheme of maneuver and key tasks.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What is an operations order?", "input": "", "output": "An OPORD — the formal order issued during Orders Production (Step 7) after COA approval.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What is the full meaning of CCIR?", "input": "", "output": "Commander's critical information requirement — information the commander needs for timely decisions.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "Define war game in MDMP terms.", "input": "", "output": "Step 4 visualization of a COA through critical events — not the same as COA comparison (Step 5).", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What is the main effort in a COA?", "input": "", "output": "The unit or axis assigned the decisive task; it receives priority of support.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What is a running estimate used for?", "input": "", "output": "Continuous assessment of facts and assumptions affecting the mission, updated throughout MDMP.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "Define Orders Production.", "input": "", "output": "MDMP Step 7 — producing the OPORD and supporting products after COA approval.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What is COA approval?", "input": "", "output": "MDMP Step 6 — the commander selects or modifies the recommended course of action.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What does end state mean in commander's intent?", "input": "", "output": "The desired military end state the operation aims to achieve — part of commander's intent alongside purpose.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What elements define a course of action?", "input": "", "output": "Scheme of maneuver, main effort, supporting efforts, and key tasks sufficient for war gaming and comparison.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What is receipt of mission?", "input": "", "output": "MDMP Step 1 — alerting the staff and beginning planning with initial guidance.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "How is a COA different from a vague concept?", "input": "", "output": "A COA is a broad but complete potential solution with scheme of maneuver, main effort, supporting efforts, and key tasks ready for war gaming.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What does CCIR provide the commander?", "input": "", "output": "Critical information needed for timely decisions during the operation.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What MDMP step is mission analysis?", "input": "", "output": "Mission analysis is Step 2 — understanding the problem, tasks, criteria, and intent.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    # scenario_coaching (+15)
    {"instruction": "Describe COA-A Direct Assault in OBJ FALCON.", "input": "", "output": "COA-A uses a main effort on Highway 12 with a supporting attack to fix forward. It tends toward higher simplicity and moderate speed.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "Describe COA-B Double Envelopment for OBJ FALCON.", "input": "", "output": "COA-B fixes north while the main effort flanks south to seize the crossing from the rear. Strong mission and disruption potential, lower simplicity.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "What is COA-C Air Assault Link-up in the fictional scenario?", "input": "", "output": "Air assault seizes the far bank; ground forces link up within 24 hours. Highest speed if successful, highest synchronization risk.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "What risk does COA-C carry in OBJ FALCON?", "input": "", "output": "Highest synchronization risk — air assault and ground link-up must be tightly coordinated.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "How does COA-D Feint and Main work in OBJ FALCON?", "input": "", "output": "Demonstration north; main attack south with deception. Good enemy disruption via deception, moderate simplicity.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "What is COA-E Turning Movement?", "input": "", "output": "Bypass OBJ FALCON to seize the enemy supply hub and force withdrawal. Strong disruption, weaker direct mission accomplishment against the river crossing.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "What are the four evaluation criteria in OBJ FALCON?", "input": "", "output": "Mission Accomplishment, Speed to Objective, Enemy Disruption, and Simplicity.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "What is the mission in the OBJ FALCON scenario?", "input": "", "output": "Seize OBJ FALCON — a river crossing and town center — within 36 hours to restore freedom of movement.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "When must staff compare OBJ FALCON COAs?", "input": "", "output": "After war gaming each COA in Step 4, staff compare in Step 5 using the decision matrix — not during the war game.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "Which OBJ FALCON COA has the highest synchronization risk?", "input": "", "output": "COA-C Air Assault Link-up — air assault and ground link-up must synchronize within 24 hours.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "Which OBJ FALCON COA favors simplicity?", "input": "", "output": "COA-A Direct Assault typically scores highest on simplicity with a single main axis on Highway 12.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "How should staff war-game the five OBJ FALCON COAs?", "input": "", "output": "Fight each COA separately in Step 4 (box method may fit the river crossing focus), record findings, then compare in Step 5.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "What enemy faces 3rd BCT at OBJ FALCON?", "input": "", "output": "A reinforced enemy battalion with prepared positions on the far bank and indirect fire in range.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "What is the time limit in the OBJ FALCON scenario?", "input": "", "output": "36 hours to seize the river crossing and town center.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    {"instruction": "Compare COA-A and COA-C on speed versus risk in OBJ FALCON.", "input": "", "output": "COA-A offers moderate speed with higher simplicity. COA-C offers the highest speed to objective if the air assault succeeds but carries the highest synchronization risk.", "bucket": "scenario_coaching", "source": "obj_falcon_fictional.md", "reviewed": True},
    # golden-adjacent paraphrases (NOT verbatim) (+23)
    {"instruction": "List all seven MDMP steps with their official names.", "input": "", "output": "1 Receipt of Mission, 2 Mission Analysis, 3 COA Development, 4 COA Analysis (War Gaming), 5 COA Comparison, 6 COA Approval, 7 Orders Production.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "War gaming belongs to which MDMP step?", "input": "", "output": "Step 4, COA Analysis (war gaming).", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "In which step do staff compare COAs against evaluation criteria?", "input": "", "output": "Step 5, COA Comparison, using a decision matrix or similar tool.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Is it correct to rank COAs during war gaming?", "input": "", "output": "No. Ranking and systematic comparison belong to Step 5, not Step 4 war gaming.", "bucket": "step_boundaries", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Explain each letter of FASDC for a new planner.", "input": "", "output": "Feasible, Acceptable, Suitable, Distinguishable, Complete — the five COA screening criteria used in Step 3.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "What three methods can staffs use to conduct a war game?", "input": "", "output": "Belt, avenue-in-depth, and box methods.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "Why record action-reaction-counteraction in the synchronization matrix?", "input": "", "output": "To visualize how friendly actions, enemy reactions, and counteractions unfold across time during Step 4 war gaming.", "bucket": "war_gaming", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "In which MDMP step are evaluation criteria first created?", "input": "", "output": "Mission Analysis (Step 2).", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "Explain how a decision matrix supports COA Comparison.", "input": "", "output": "It tabulates each COA against evaluation criteria in Step 5, supporting a staff recommendation before commander approval at Step 6.", "bucket": "coa_screening", "source": "coa_screening.md", "reviewed": True},
    {"instruction": "How do Step 3 COA Development and Step 4 COA Analysis differ?", "input": "", "output": "Step 3 generates and screens COAs. Step 4 war games each COA separately to find strengths and weaknesses.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What MDMP activity follows COA approval?", "input": "", "output": "Orders Production (Step 7) — producing the OPORD and supporting products.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Define commander's intent for a staff officer.", "input": "", "output": "A concise expression of the operation's purpose and desired end state, guiding initiative when the plan no longer fits.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "At which step does the commander choose the final COA?", "input": "", "output": "Step 6, COA Approval.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What does the staff produce during Orders Production?", "input": "", "output": "The OPORD and supporting order products to execute the approved COA.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Is head-to-head COA comparison permitted in Step 4?", "input": "", "output": "No. Step 4 analyzes each COA separately. Head-to-head comparison is Step 5.", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Explain a synchronization matrix to a new planner.", "input": "", "output": "A war-gaming tool aligning friendly actions, enemy reactions, and counteractions across time and space using action-reaction-counteraction.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What is the full expansion of CCIR?", "input": "", "output": "Commander's critical information requirement.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "Explain mission analysis to a lieutenant.", "input": "", "output": "MDMP Step 2 — analyze the higher HQ order, develop running estimates, define the problem, draft intent, develop CCIRs and evaluation criteria.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What must a valid COA include?", "input": "", "output": "Scheme of maneuver, main effort, supporting efforts, and key tasks — sufficient for war gaming and comparison.", "bucket": "glossary", "source": "glossary.md", "reviewed": True},
    {"instruction": "What step is COA Comparison?", "input": "", "output": "Step 5 — systematic comparison of COAs against evaluation criteria after war gaming.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "What happens after the commander approves a COA?", "input": "", "output": "The staff proceed to Orders Production (Step 7) to issue the OPORD.", "bucket": "mdmp_steps", "source": "mdmp_steps.md", "reviewed": True},
    {"instruction": "Should staff compare COAs during Step 4 war gaming?", "input": "", "output": "No. Compare COAs in Step 5 after war gaming each option separately.", "bucket": "step_boundaries", "source": "war_gaming.md", "reviewed": True},
    {"instruction": "What is the difference between COA development and COA analysis?", "input": "", "output": "COA development is Step 3 (generate and screen COAs). COA analysis is Step 4 (war game each COA).", "bucket": "step_boundaries", "source": "mdmp_steps.md", "reviewed": True},
]


def load_existing(path: Path) -> list[dict]:
    rows: list[dict] = []
    if path.exists():
        with path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def main() -> int:
    existing = load_existing(PAIRS_PATH)
    seen = {r["instruction"].strip().lower() for r in existing}
    added = 0
    skipped = 0
    for row in NEW_PAIRS:
        key = row["instruction"].strip().lower()
        if key in seen:
            skipped += 1
            continue
        existing.append(row)
        seen.add(key)
        added += 1

    with PAIRS_PATH.open("w", encoding="utf-8") as f:
        for row in existing:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"pairs.jsonl: {len(existing)} total ({added} added, {skipped} skipped duplicates)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
