# AppHub deploy plan — MDMP Staff Planning Assistant

**Updated:** 2026-09-01  
**Status:** plan only; no AppHub app exists yet  
**Target repo:** `apphub` (`apps/<name>/` Flask blueprints on AppHost)

This expert is a **LoRA-adapted Mistral-7B**, not a prompt on Bedrock/OpenAI. AppHub should not load those weights in the Flask process. The app is a thin chat UI; inference stays a sidecar.

Spark Unsloth remains the **publish** artifact. Mac mlx-v4 (`outputs/mlx-mistral7b-mdmp-lora-v4`) is the **laptop demo** artifact. Adapters are not interchangeable. See [spark-vs-mac-training.md](spark-vs-mac-training.md).

## Architecture

```text
Browser  →  AppHub app  /mdmp-staff-planning/
                POST /api/chat
                    →  inference sidecar  (mlx-lm server | Ollama | vLLM)
                         base Mistral-7B + LoRA
```

Keep doctrine, disclaimer, and golden eval in this research repo. Keep serving URL and UI in `apphub`. Do not commit `outputs/*.safetensors` into AppHub.

Existing AppHub LLM apps already follow this split:

| App | Chat UI | Inference |
|-----|---------|-----------|
| `apps/opnav-n80` | `/api/llm/chat` | Bedrock or OpenAI `/v1/chat/completions` |
| `apps/datahub-llm` | `/api/chat` | local Ollama |

Closest copy target for this expert: **opnav-n80’s OpenAI client**, with `OPENAI_BASE_URL` aimed at a local or hosted OpenAI-compatible server.

A Bedrock-only clone (generic Llama/Claude + doctrine pasted into the prompt) is **not** deploying this expert. That is a different model with RAG.

## What not to do

- Import `train/mlx_inference.py`, Unsloth, or `mlx-lm` into `apps/`. Wrong process, wrong deps, request timeouts.
- Mix `requirements-mlx.txt` / `requirements-ml.txt` into AppHub’s environment.
- Train inside the app. Train stays here; AppHub only calls a served model.
- Put 4-bit weights in git.

## Local Mac (first working app)

### 1. Serve the v4 adapter

From this repo, with a venv that has `mlx-lm`:

```bash
python -m mlx_lm server \
  --model mlx-community/Mistral-7B-Instruct-v0.3-4bit \
  --adapter-path outputs/mlx-mistral7b-mdmp-lora-v4 \
  --port 8080
```

`mlx_lm.server` speaks `/v1/chat/completions`. Fuse first if a single directory is easier to point at:

```bash
python -m mlx_lm fuse \
  --model mlx-community/Mistral-7B-Instruct-v0.3-4bit \
  --adapter-path outputs/mlx-mistral7b-mdmp-lora-v4 \
  --save-path outputs/mlx-mistral7b-mdmp-fused
```

### 2. New AppHub app on its own branch

AppHub auto-discovers `apps/<name>/app.json`. Author the app on a feature branch off `local-integration` (see apphub `.cursor/rules/apphub-branch-workflow.mdc`). Preferred builder path: **Create Application** in the AppHub UI, then add chat routes. Do not author from `main`.

```bash
cd apphub
git checkout local-integration
git pull
git checkout -b feature/mdmp-staff-planning
```

Required layout (`apphub/.cursor/rules/app-creation-rules.mdc`):

```text
apps/mdmp-staff-planning/
  app.json
  app.py
  templates/index.html
  __init__.py
```

Suggested `app.json` config (no DataHub required for v1):

```json
{
  "name": "mdmp-staff-planning",
  "description": "MDMP staff-planning coaching assistant (unofficial; public doctrine LoRA)",
  "route": "/mdmp-staff-planning",
  "module": "app",
  "icon": "bot",
  "category": "Custom Apps",
  "config": {
    "domain": [],
    "DATAHUB_URL": "",
    "APP_TITLE": "MDMP Staff Planning Assistant",
    "LLM_BASE_URL": "http://127.0.0.1:8080/v1",
    "LLM_MODEL": "mlx-community/Mistral-7B-Instruct-v0.3-4bit",
    "LLM_API_KEY": "not-needed",
    "REQUEST_TIMEOUT_SECONDS": "90"
  }
}
```

`app.py` should:

- Build a Flask `Blueprint`, `get_all_config("/mdmp-staff-planning")`, `current_app.logger`.
- `GET /` → chat page with the FM 5-0 / unofficial-tool disclaimer (same language as this README).
- `POST /api/chat` with `{message, history}` → sidecar `/v1/chat/completions`.
- `GET /api/status` → sidecar reachable or a clear “start mlx_lm.server” error.
- Not load the model in-process.

Copy chat plumbing from `apps/opnav-n80/openai_llm.py` and `apps/opnav-n80/app.py` (`/api/llm/chat`). Leave OPNAV Excel/traceability out.

No DataHub tables unless saved transcripts are needed (`datahub-llm` already does that).

### 3. Run both processes

```bash
# terminal 1 — expert (this repo)
python -m mlx_lm server --model ... --adapter-path outputs/mlx-mistral7b-mdmp-lora-v4 --port 8080

# terminal 2 — AppHub
cd apphub && ./runLocal.sh
```

Open `/mdmp-staff-planning/`. After `app.json` changes, restart `./runLocal.sh`. Merge into `local-integration` when the app should appear next to the others.

## Production AppHub

AppHost in Docker will not run MLX or Unsloth. A shared tenant needs a **hosted** OpenAI-compatible endpoint; the same app sets `LLM_BASE_URL` to that host.

| Where the expert lives | How |
|------------------------|-----|
| Spark GPU | vLLM / TGI serving the Unsloth adapter (publish path) |
| Hugging Face | Adapter + dataset published Sep 1, 2026 ([mistral7b-mdmp-lora](https://huggingface.co/decisionlens/mistral7b-mdmp-lora)); optional Inference Endpoint for hosted GPU demo |
| Bedrock | custom-model import — not `BEDROCK_MODEL_ID` for stock Llama |

Then set `config.domain` to tenant hostnames when the app should be visible there (leave `[]` until that is intentional).

## App behavior (v1 is enough)

- Single-turn and short multi-turn Q&A (history cap ~10 messages, same idea as OPNAV).
- Temperature ~0.1 to match `demo/ask.py` / golden eval.
- Always show: unofficial educational tool; not a substitute for staff planning; verify against FM 5-0 / ADP 5-0.
- Empty and error states if the sidecar is down or times out.
- Optional later: paste `corpus/doctrine/*.md` into context as belt-and-suspenders with the LoRA. Not required for the 17/20 Mac result.

## Sequencing

1. Confirm `mlx_lm.server` answers a curl to `/v1/chat/completions` with a golden-style question.
2. Scaffold `feature/mdmp-staff-planning` in apphub; wire OpenAI-compatible client.
3. Demo on `local-integration` via `./runLocal.sh`.
4. For a shared demo, serve the **Spark** adapter on GPU and point `LLM_BASE_URL` at that server; keep Mac sidecar for laptop-only use.
5. Hugging Face adapter publish is **done** (Sep 1, 2026). Optional: Inference Endpoint for a hosted GPU demo, independent of the AppHub UI.

## Leak / classification

Same pre-commit rules as this repo: no customer names, no OPNAV capture data, no proprietary algorithm terms. The AppHub app is a UI over the open-doctrine model. Classification banner, if any, should stay UNCLASSIFIED / synthetic-or-doctrinal — this is not a classified planning system.
