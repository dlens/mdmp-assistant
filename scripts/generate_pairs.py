#!/usr/bin/env python3
"""Suggest new training pairs from corpus markdown (does not modify pairs.jsonl)."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIRS = [ROOT / "corpus" / "doctrine", ROOT / "corpus" / "scenarios"]

FRONT_MATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
HEADING_RE = re.compile(r"^(#{2,3})\s+(.+)$", re.MULTILINE)

BUCKET_BY_FILE = {
    "mdmp_steps.md": "mdmp_steps",
    "war_gaming.md": "war_gaming",
    "coa_screening.md": "coa_screening",
    "glossary.md": "glossary",
    "sources.md": "glossary",
    "obj_falcon_fictional.md": "scenario_coaching",
}


def strip_front_matter(text: str) -> str:
    return FRONT_MATTER_RE.sub("", text, count=1).lstrip()


def first_paragraph(body: str) -> str:
    for block in body.split("\n\n"):
        block = block.strip()
        if not block or block.startswith("|") or block.startswith("#"):
            continue
        block = re.sub(r"^[-*]\s+", "", block, flags=re.MULTILINE)
        return block.replace("\n", " ").strip()
    return ""


def sections_from_markdown(path: Path) -> list[tuple[str, str]]:
    text = strip_front_matter(path.read_text(encoding="utf-8"))
    matches = list(HEADING_RE.finditer(text))
    if not matches:
        para = first_paragraph(text)
        return [("Overview", para)] if para else []

    sections: list[tuple[str, str]] = []
    for i, match in enumerate(matches):
        title = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        para = first_paragraph(body)
        if para:
            sections.append((title, para))
    return sections


def suggest_pairs(corpus_dirs: list[Path]) -> list[dict]:
    suggestions: list[dict] = []
    for corpus_dir in corpus_dirs:
        if not corpus_dir.exists():
            continue
        for path in sorted(corpus_dir.glob("*.md")):
            if path.name == "sources.md":
                continue
            bucket = BUCKET_BY_FILE.get(path.name, "mdmp_steps")
            for title, para in sections_from_markdown(path):
                instruction = f"Explain: {title}"
                suggestions.append(
                    {
                        "instruction": instruction,
                        "input": "",
                        "output": para,
                        "bucket": bucket,
                        "source": path.name,
                        "reviewed": False,
                    }
                )
                suggestions.append(
                    {
                        "instruction": f"What should a staff officer know about {title}?",
                        "input": "",
                        "output": para,
                        "bucket": bucket,
                        "source": path.name,
                        "reviewed": False,
                    }
                )
    return suggestions


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest training pairs from corpus (review before adding to pairs.jsonl)."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "data" / "pairs_suggested.jsonl",
        help="Output path for suggestions (default: data/pairs_suggested.jsonl)",
    )
    args = parser.parse_args()

    rows = suggest_pairs(CORPUS_DIRS)
    write_jsonl(args.out, rows)
    print(f"Wrote {len(rows)} suggestions to {args.out}")
    print("Review each row, set reviewed=true, then append to data/pairs.jsonl")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
