# Spark Unsloth vs Mac MLX training

**Updated:** 2026-08-18  
**Stacks:** Unsloth QLoRA on NVIDIA GB10 vs `mlx-lm` QLoRA on Apple Silicon  
**Same data and eval:** 275 train pairs, 20 held-out golden questions (`eval/golden_questions.json`)

This note records why Mac training needed **many more optimizer iterations** than Spark v7, what that does and does not mean, and what to copy (or not) when moving a run between stacks.

Related: [README Mac / MLX sidecar](../README.md#mac--mlx-sidecar), `train/config.yaml`, `train/mlx_config.yaml`.

## Headline

Spark v7 and Mac mlx-v4 are **not the same training schedule with a different backend**. Spark is epoch-based at a high learning rate; MLX is iteration-based at a lower rate. Matching LoRA *rank* is not matching LoRA *scale*, batch, or step count.

On the same golden set:

| Run | Stack | Optimizer updates | Examples seen | ~Epochs | Golden |
|-----|--------|-------------------|---------------|---------|--------|
| Spark Unsloth v7 | GB10 / Unsloth / PEFT | ~70 | 550 | 2 | **14/20 (70%)** |
| mlx-v1 | Mac 4-bit | 200 (then NaN) | — | — | 0/20 |
| mlx-v2 | Mac 4-bit, mlx defaults | 200 | 200 | 0.7 | 4/20 (20%) |
| mlx-v3 | Mac 4-bit, Spark lr | 250 | 1,000 | 3.6 | 0/20 (empty) |
| **mlx-v4** | Mac 4-bit, lower lr | **600** | **2,400** | **8.7** | **17/20 (85%)** |

Mac v4 **beats** Spark on this 20-question scorer. That is a local-iteration result, not a claim that MLX is a better publish path. Adapters are not interchangeable.

## Units: epochs vs iters

Unsloth (`train/finetune.py`) uses Hugging Face `SFTTrainer` with **epochs**. mlx-lm uses **iters**, and each iter is one optimizer step **after** gradient accumulation.

**Spark v7** (`train/config.yaml`):

- 275 train rows, 2 epochs
- `per_device_train_batch_size: 2` × `gradient_accumulation_steps: 4` → **effective batch 8**
- Optimizer steps ≈ `2 × ceil(275 / 8)` ≈ **70**
- Example-exposures = `2 × 275` = **550**
- Learning rate **2e-4**, warmup ratio 0.03 (~2 steps)

**Mac mlx-v4** (`train/mlx_config.yaml`):

- Same 275 rows
- `batch_size: 1` × `grad_accumulation_steps: 4` → **effective batch 4**
- `iters: 600` → **600 optimizer updates**
- Example-exposures = `600 × 4` = **2,400** ≈ **8.7 epochs**
- Learning rate **5e-5** with cosine decay and 20-step warmup

An MLX `iter` is therefore **not** “one Spark epoch” and not “one training pair.” To match Spark’s *schedule* on MLX you would want about **70 iters at effective batch 8**, not 600. That underfit on 4-bit MLX. 600 iters was the compensating knob.

## LoRA scale is not Unsloth alpha

This is the main hyperparameter trap.

- PEFT / Unsloth apply `(lora_alpha / rank)` to the low-rank update. Spark v7 is r=16, α=32 → effective multiplier **2.0**.
- mlx-lm multiplies the update by `scale` **directly**. Rank 16 with `scale: 32` is ~16× too large relative to Spark.

mlx-v1 copied Spark’s α into MLX `scale` (32) at lr 2e-4. Train loss went NaN by iter 10; golden was all `<unk>` / 0/20.

mlx-v4 uses `scale: 2.0` to match Spark’s α/r. mlx-lm’s library default (`rank: 8`, `scale: 20`) is a different convention again and should not be treated as “Unsloth-equivalent.”

A rough “update product” (scale-or-α/r × learning rate) for orientation only:

| Run | Multiplier | LR | Product |
|-----|------------|-----|---------|
| Spark v7 | 2.0 (α/r) | 2e-4 | 4e-4 |
| mlx-v1 (NaN) | 32 | 2e-4 | 6.4e-3 |
| mlx-v2 | 20 | 1e-5 | 2e-4 |
| mlx-v3 (collapse) | 2.0 | 2e-4 | 4e-4 |
| mlx-v4 | 2.0 | 5e-5 | 1e-4 |

mlx-v3 matched Spark’s product on paper and still collapsed (empty generations). Prompt-masked loss on short completions makes each step noisier than Unsloth’s full-sequence SFT, so the same nominal LR is not safe. mlx-v4 cut LR 4× and bought the difference back with ~8.6× more optimizer steps and ~4.4× more example-exposures.

## Other stack differences (not just step count)

These also prevent a 1:1 hyperparameter port:

1. **Quantization.** Spark loads `mistralai/Mistral-7B-Instruct-v0.3` with Unsloth 4-bit. Mac trains `mlx-community/Mistral-7B-Instruct-v0.3-4bit`. Same family, different 4-bit recipe.
2. **Which layers get LoRA.** Unsloth targets q/k/v/o/gate/up/down on **all** blocks. mlx-lm default `num_layers: 16` is the **last 16** of 32. mlx-v2 used 16; mlx-v4 uses `num_layers: -1` (all).
3. **Prompt format and loss.** Spark trains the Unsloth `<s>[INST] … [/INST] answer</s>` string, loss on the whole sequence. mlx-v4 exports chat `messages`, applies Mistral’s template, and sets `mask_prompt: true` (loss on the assistant span only).
4. **Optimizer / schedule.** Spark: `adamw_8bit`, linear warmup 3%. mlx-v4: AdamW, cosine 5e-5 → 5e-6, 20 warmup steps.
5. **Batch noise.** Spark effective batch 8 vs MLX 4. Smaller batches need more steps or a lower LR to stay stable.

Wall clock (weights already cached): Spark v6 ~109 s for 2 epochs; mlx-v4 ~17.5 min for 600 iters; peak MLX memory ~5.6 GB.

## What the golden scores do and do not imply

**mlx-v4 17/20 vs Spark 14/20** means: on this scorer, with more passes over the same 275 pairs, 4-bit MLX can *exceed* the Spark sprint target. The three mlx-v4 misses were phrasing (`Distinguishable`/`Complete`; Step 2 vs Step 3; the word `action` on the synchronization-matrix item), not collapse.

It does **not** mean:

- Mac training is strictly better. The 20-item golden set is small and overlaps the doctrine the pairs were written from. Extra epochs can look like quality when they are partly **overfit to the scorer’s required strings**.
- The adapters are substitutes. Unsloth `.safetensors` will not load in mlx-lm and vice versa.
- Spark should switch to 600 steps at 5e-5. Spark already hit 70% in two epochs at 2e-4; that remains the intended **publish** recipe (`README`: Spark Unsloth is the publish path).
- Paper 1’s 1/20 → 14/20 claim should be rewritten as 17/20. That result is Unsloth/GB10. Mac is a sidecar replication with a **different schedule**.

Val loss on mlx-v4 fell 6.79 → 1.08 at iter 500, then rose to 1.19 at 600. That is mild overfit on the MLX valid split and another reason not to treat “more iters” as unbounded.

## Implications for future runs

1. **Do not copy `train/config.yaml` into `train/mlx_config.yaml` field-for-field.** Translate α → `scale = alpha / rank`, then retune LR. If 4-bit MLX NaNs or emits empty strings, drop LR and raise iters; do not raise `scale` toward 32.
2. **Compare workloads in example-exposures or optimizer steps × effective batch**, not raw `iters` vs `num_train_epochs`.
3. **A Spark-matched MLX schedule** (~70 updates, effective batch 8, lr 2e-4) is a useful *ablation*, not a quality target. It failed here. The working Mac recipe is lower LR, all layers, masked chat SFT, ~9 epochs.
4. **Keep Spark as the GPU publish artifact** ([decisionlens/mistral7b-mdmp-lora](https://huggingface.co/decisionlens/mistral7b-mdmp-lora)). MLX v4 is the **Mac Hub sidecar** ([decisionlens/mistral7b-mdmp-lora-mlx](https://huggingface.co/decisionlens/mistral7b-mdmp-lora-mlx)), not a conversion of the Unsloth adapter. If AppHub or a paper needs one numbered GPU model, quote Spark v7 unless the Mac stack is named explicitly.
5. **If Mac quality is the goal**, next levers are data (the remaining FASDC / Step 3 / “action” misses), not another 2× iters. Valid loss already turned up at 600.
6. **If Spark quality is the goal**, extra Mac epochs are optional. Closing Spark’s remaining six golden failures is still a data/scorer problem (`eval/sprint1-summary.md` v7 cycle), not an MLX problem.

## Working recipes (do not mix)

Spark (publish):

```bash
python train/finetune.py
python eval/run_golden.py --adapter outputs/mistral7b-mdmp-lora --label v7
```

Mac (local train, or Hub download):

```bash
python scripts/export_mlx_data.py
python -m mlx_lm lora -c train/mlx_config.yaml
python eval/run_golden_mlx.py --adapter outputs/mlx-mistral7b-mdmp-lora-v4 --label mlx-v4

# or, after Hub publish:
hf download decisionlens/mistral7b-mdmp-lora-mlx --local-dir outputs/mlx-mistral7b-mdmp-lora-v4
```
