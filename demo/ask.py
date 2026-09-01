#!/usr/bin/env python3
"""CLI chat demo for the MDMP Staff Planning Assistant.

GPU (Unsloth) and Mac MLX are separate stacks and separate venvs. Adapters
are not interchangeable. Omit --backend to auto-detect Apple Silicon vs NVIDIA.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from demo.backend import BackendError, load_runtime, resolve_backend  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Chat with the MDMP planning assistant.")
    parser.add_argument(
        "--backend",
        choices=("gpu", "mlx"),
        default=None,
        help="Inference stack (default: mlx on Apple Silicon, gpu when nvidia-smi is present)",
    )
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument(
        "--adapter",
        type=Path,
        default=None,
        help="LoRA adapter directory (backend default if omitted; unused with --base)",
    )
    parser.add_argument(
        "--base",
        action="store_true",
        help="Use base model only (no adapter)",
    )
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.1)
    args = parser.parse_args()

    try:
        backend, reason = resolve_backend(args.backend)
        print(f"Loading backend={backend} ({reason})")
        runtime = load_runtime(
            backend=backend,
            backend_reason=reason,
            config_path=args.config,
            adapter_path=args.adapter,
            base=args.base,
        )
    except BackendError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"Loaded {runtime.load_label()}")
    print("MDMP Staff Planning Assistant — type a question, empty line to quit.")
    print("Unofficial educational tool. Verify against FM 5-0 / ADP 5-0.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return 0
        if not question:
            print("Bye.")
            return 0
        answer = runtime.generate(
            question,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
        )
        print(f"Assistant: {answer}\n")


if __name__ == "__main__":
    raise SystemExit(main())
