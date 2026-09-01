"""Model loading and generation for MDMP assistant."""

from __future__ import annotations

from pathlib import Path

from train.formatting import format_inference_prompt


def load_model(
    *,
    model_name: str,
    adapter_path: str | Path | None = None,
    max_seq_length: int = 2048,
    load_in_4bit: bool = True,
):
    from unsloth import FastLanguageModel

    load_path = str(adapter_path) if adapter_path else model_name
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=load_path,
        max_seq_length=max_seq_length,
        dtype=None,
        load_in_4bit=load_in_4bit,
    )
    FastLanguageModel.for_inference(model)
    return model, tokenizer


def generate_answer(
    model,
    tokenizer,
    question: str,
    *,
    input_text: str = "",
    max_new_tokens: int = 256,
    temperature: float = 0.1,
    top_p: float = 0.9,
) -> str:
    prompt = format_inference_prompt(question, input_text)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        do_sample=temperature > 0,
        use_cache=True,
    )
    new_tokens = outputs[0][inputs["input_ids"].shape[1] :]
    text = tokenizer.decode(new_tokens, skip_special_tokens=True)
    return text.strip()
