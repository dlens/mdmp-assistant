"""Prompt formatting for Mistral-7B-Instruct fine-tuning and inference."""

from __future__ import annotations


def build_user_prompt(instruction: str, input_text: str = "") -> str:
    instruction = (instruction or "").strip()
    input_text = (input_text or "").strip()
    if input_text:
        return f"{instruction}\n{input_text}"
    return instruction


def format_training_text(instruction: str, output: str, input_text: str = "") -> str:
    user = build_user_prompt(instruction, input_text)
    return f"<s>[INST] {user} [/INST] {output.strip()}</s>"


def format_inference_prompt(instruction: str, input_text: str = "") -> str:
    user = build_user_prompt(instruction, input_text)
    return f"<s>[INST] {user} [/INST] "
