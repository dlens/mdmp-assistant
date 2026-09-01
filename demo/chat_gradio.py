#!/usr/bin/env python3
"""Browser chat for the MDMP Staff Planning Assistant (Gradio).

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

from demo.backend import (  # noqa: E402
    BackendError,
    ThreadOwnedRuntime,
    load_runtime,
    resolve_backend,
)

_DESCRIPTION = (
    "Unofficial educational tool. Not affiliated with the U.S. Army. "
    "Verify answers against FM 5-0 / ADP 5-0. Each turn is independent "
    "(the adapter is not multi-turn chat-tuned)."
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Browser chat with the MDMP planning assistant (Gradio)."
    )
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
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7860)
    args = parser.parse_args()

    try:
        import gradio as gr
    except ImportError:
        print(
            "Gradio is not installed in this venv.\n"
            "pip install gradio",
            file=sys.stderr,
        )
        return 1

    try:
        backend, reason = resolve_backend(args.backend)
        print(f"Loading backend={backend} ({reason})")

        def loader():
            return load_runtime(
                backend=backend,
                backend_reason=reason,
                config_path=args.config,
                adapter_path=args.adapter,
                base=args.base,
            )

        # MLX must load+generate on one thread (Gradio otherwise uses a worker
        # with no MLX stream). Unsloth/CUDA is fine on Gradio's thread pool.
        if backend == "mlx":
            runtime = ThreadOwnedRuntime(loader)
        else:
            runtime = loader()
    except BackendError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"Loaded {runtime.load_label()}")

    def reply(message: str, history: list) -> str:
        del history
        return runtime.generate(
            message,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
        )

    gr.ChatInterface(
        fn=reply,
        title="MDMP Staff Planning Assistant",
        description=_DESCRIPTION,
    ).launch(server_name=args.host, server_port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
