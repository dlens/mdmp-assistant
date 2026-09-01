"""Shared GPU / MLX loading for demo chat scripts.

Do not import Unsloth or mlx-lm at module level — those stacks must stay
in separate venvs. Load the chosen backend only after it is resolved.
"""

from __future__ import annotations

import platform
import queue
import shutil
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Literal

import yaml

ROOT = Path(__file__).resolve().parent.parent

BackendName = Literal["gpu", "mlx"]

_GPU_HINT = "gpu backend requires: pip install -r requirements-ml.txt"
_MLX_HINT = "mlx backend requires: pip install -r requirements-mlx.txt (separate venv)"


class BackendError(Exception):
    """User-facing failure selecting or loading an inference backend."""


def detect_backend() -> tuple[BackendName, str]:
    """Pick gpu vs mlx from the machine. Does not probe Python packages."""
    system = platform.system()
    machine = platform.machine().lower()
    apple_silicon = system == "Darwin" and machine in {"arm64", "aarch64"}
    has_nvidia = shutil.which("nvidia-smi") is not None

    if apple_silicon:
        return "mlx", "Apple Silicon"
    if has_nvidia:
        return "gpu", "NVIDIA GPU (nvidia-smi)"
    raise BackendError(
        "Could not detect inference backend. "
        "Pass --backend mlx (Apple Silicon) or --backend gpu (NVIDIA + Unsloth)."
    )


def resolve_backend(explicit: str | None) -> tuple[BackendName, str]:
    if explicit == "gpu":
        return "gpu", "--backend gpu"
    if explicit == "mlx":
        return "mlx", "--backend mlx"
    if explicit:
        raise BackendError(f"Unknown backend {explicit!r}. Use gpu or mlx.")
    return detect_backend()


def default_config_path(backend: BackendName) -> Path:
    if backend == "gpu":
        return ROOT / "train" / "config.yaml"
    return ROOT / "train" / "mlx_config.yaml"


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise BackendError(f"Config is not a mapping: {path}")
    return data


def default_adapter_path(backend: BackendName, cfg: dict) -> Path:
    raw = cfg.get("adapter_path") if backend == "mlx" else cfg.get("output_dir")
    if not raw:
        name = "adapter_path" if backend == "mlx" else "output_dir"
        raise BackendError(f"{name} missing from config for {backend} backend.")
    path = Path(raw)
    return path if path.is_absolute() else ROOT / path


def _model_name(backend: BackendName, cfg: dict) -> str:
    key = "model_name" if backend == "gpu" else "model"
    name = cfg.get(key)
    if not isinstance(name, str) or not name.strip():
        raise BackendError(f"{key} missing from config for {backend} backend.")
    return name.strip()


def _adapter_missing_hint(backend: BackendName, adapter: Path) -> str:
    if backend == "gpu":
        train = "python train/finetune.py"
        download = (
            "hf download decisionlens/mistral7b-mdmp-lora "
            f"--local-dir {adapter}"
        )
        return f"Adapter not found: {adapter}\nTrain first: {train}\nOr download: {download}"
    train = "python -m mlx_lm lora -c train/mlx_config.yaml"
    download = (
        "hf download decisionlens/mistral7b-mdmp-lora-mlx "
        f"--local-dir {adapter}"
    )
    return (
        f"Adapter not found: {adapter}\n"
        f"Train first: {train}\n"
        f"Or download: {download}"
    )


@dataclass
class ChatRuntime:
    backend: BackendName
    backend_reason: str
    model_name: str
    adapter: Path | None
    model: Any
    tokenizer: Any
    _generate: Callable[..., str]

    def generate(
        self,
        question: str,
        *,
        max_new_tokens: int = 256,
        temperature: float = 0.1,
    ) -> str:
        return self._generate(
            self.model,
            self.tokenizer,
            question,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
        )

    def load_label(self) -> str:
        suffix = "" if self.adapter is None else f" + {self.adapter}"
        return f"{self.model_name}{suffix} [{self.backend}: {self.backend_reason}]"


class ThreadOwnedRuntime:
    """Load and generate on one thread.

    MLX streams are thread-local. Gradio runs the chat fn on a worker that
    has no ``Stream(cpu, 0)`` — same failure as calling mlx-lm from any
    other thread than the one that loaded the weights.
    """

    def __init__(self, loader: Callable[[], ChatRuntime]) -> None:
        self._jobs: queue.Queue[tuple[str, dict, queue.Queue] | None] = queue.Queue()
        self._ready = threading.Event()
        self._error: BaseException | None = None
        self.runtime: ChatRuntime | None = None
        thread = threading.Thread(target=self._loop, args=(loader,), daemon=True)
        thread.start()
        self._ready.wait()
        if self._error is not None:
            raise self._error
        if self.runtime is None:
            raise BackendError("MLX owner thread started without a runtime.")

    def _loop(self, loader: Callable[[], ChatRuntime]) -> None:
        try:
            self.runtime = loader()
        except BaseException as exc:
            self._error = exc
            self._ready.set()
            return
        self._ready.set()
        while True:
            job = self._jobs.get()
            if job is None:
                return
            question, kwargs, reply = job
            try:
                text = self.runtime.generate(question, **kwargs)
                reply.put((True, text))
            except BaseException as exc:
                reply.put((False, exc))

    def generate(
        self,
        question: str,
        *,
        max_new_tokens: int = 256,
        temperature: float = 0.1,
    ) -> str:
        reply: queue.Queue[tuple[bool, Any]] = queue.Queue()
        self._jobs.put(
            (
                question,
                {"max_new_tokens": max_new_tokens, "temperature": temperature},
                reply,
            )
        )
        ok, payload = reply.get()
        if not ok:
            raise payload
        return str(payload)

    def load_label(self) -> str:
        if self.runtime is None:
            return "unloaded"
        return self.runtime.load_label()


def load_runtime(
    *,
    backend: BackendName,
    backend_reason: str,
    config_path: Path | None,
    adapter_path: Path | None,
    base: bool,
) -> ChatRuntime:
    cfg_path = config_path or default_config_path(backend)
    if not cfg_path.exists():
        raise BackendError(f"Config not found: {cfg_path}")
    cfg = load_config(cfg_path)
    model_name = _model_name(backend, cfg)

    adapter: Path | None = None
    if not base:
        adapter = adapter_path or default_adapter_path(backend, cfg)
        if not adapter.exists():
            raise BackendError(_adapter_missing_hint(backend, adapter))

    if backend == "gpu":
        try:
            from train.inference import generate_answer, load_model
        except ImportError as exc:
            raise BackendError(f"Failed to import Unsloth stack. {_GPU_HINT}") from exc
        model, tokenizer = load_model(
            model_name=model_name,
            adapter_path=adapter,
            max_seq_length=int(cfg.get("max_seq_length", 2048)),
            load_in_4bit=bool(cfg.get("load_in_4bit", True)),
        )
        generate = generate_answer
    elif backend == "mlx":
        try:
            from train.mlx_inference import generate_answer, load_mlx
        except ImportError as exc:
            raise BackendError(f"Failed to import MLX stack. {_MLX_HINT}") from exc
        model, tokenizer = load_mlx(model_name=model_name, adapter_path=adapter)
        generate = generate_answer
    else:
        raise BackendError(f"Unknown backend {backend!r}. Use gpu or mlx.")

    return ChatRuntime(
        backend=backend,
        backend_reason=backend_reason,
        model_name=model_name,
        adapter=adapter,
        model=model,
        tokenizer=tokenizer,
        _generate=generate,
    )
