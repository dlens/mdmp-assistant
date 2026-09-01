"""Rule-based scoring for golden-question evaluation."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class ScoreResult:
    passed: bool
    missing_must_mention: list[str] = field(default_factory=list)
    forbidden_mentions: list[str] = field(default_factory=list)


def _contains_term(text: str, term: str) -> bool:
    lowered = text.lower()
    term_lower = term.lower()
    if term_lower == "no":
        if lowered.strip().startswith("≠"):
            return True
        return bool(re.search(r"\bno\b", lowered)) or bool(re.search(r"\bnot\b", lowered))
    if term_lower == "war game":
        return bool(re.search(r"\bwar[\s-]?(?:games?|gaming)\b", lowered))
    step_match = re.fullmatch(r"step (\d+)", term_lower)
    if step_match:
        n = step_match.group(1)
        patterns = [
            rf"\bstep\s*{n}\b",
            rf"\b{n}(?:st|nd|rd|th)\s+step\b",
            rf"\b{n}(?:st|nd|rd|th)\s+mdmp\s+step\b",
        ]
        return any(re.search(p, lowered) for p in patterns)
    return term_lower in lowered


def score_response(
    response: str,
    *,
    must_mention: list[str],
    must_not_mention: list[str],
) -> ScoreResult:
    missing = [term for term in must_mention if not _contains_term(response, term)]
    forbidden = [term for term in must_not_mention if _contains_term(response, term)]
    return ScoreResult(
        passed=not missing and not forbidden,
        missing_must_mention=missing,
        forbidden_mentions=forbidden,
    )
