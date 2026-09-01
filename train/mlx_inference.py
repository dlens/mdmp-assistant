"""MLX model loading and generation for the MDMP Mac sidecar."""

from __future__ import annotations

from pathlib import Path

from train.formatting import build_user_prompt, format_inference_prompt


def load_mlx(
    *,
    model_name: str,
    adapter_path: str | Path | None = None,
):
    from mlx_lm import load

    adapter = str(adapter_path) if adapter_path else None
    return load(model_name, adapter_path=adapter)


def _prompt_tokens(tokenizer, question: str, input_text: str = "") -> list[int] | str:
    user = build_user_prompt(question, input_text)
    apply = getattr(tokenizer, "apply_chat_template", None)
    if callable(apply) and getattr(tokenizer, "has_chat_template", True):
        try:
            return apply(
                [{"role": "user", "content": user}],
                tokenize=True,
                add_generation_prompt=True,
            )
        except Exception:
            pass
    return format_inference_prompt(question, input_text)


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
    from mlx_lm import generate
    from mlx_lm.sample_utils import make_sampler

    prompt = _prompt_tokens(tokenizer, question, input_text)
    sampler = make_sampler(temp=temperature, top_p=top_p)
    text = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=max_new_tokens,
        sampler=sampler,
    )
    return str(text).strip()
