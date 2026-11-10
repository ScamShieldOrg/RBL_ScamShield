"""Builder for the production-ready reproduction notebooks of the 3 foundational
precursor papers of ScamShield-VN:

1. ViSoBERT (Quoc-Nam Nguyen, Thang Chau Phan, Duc-Vu Nguyen, Kiet Van Nguyen,
   EMNLP 2023 Main Conference, pp. 5191-5207)
2. Edge-AI BiGRU + WBCE (H. C. Phap, J. Inf. Telecommun., 2026, M041)
3. MultiPhishGuard (Yinuo Xue, Eric Spero, Meng Wai Woo, Wei Gao, Giovanni Russello,
   arXiv:2505.23803v2, revised 23 May 2026)

Patch revision 2026-11-09 (audit fixes; see docs/BAO_CAO_CAP_NHAT_TAI_THUC_NGHIEM_3_PAPER.md):
- P1: dataset pins corrected after live verification against the HuggingFace
  datasets-server. `uitnlp/uit-vsmec` does not exist and `uitnlp/vihsd` is gated,
  so the loaders now use public mirrors whose split sizes match Table 2 of the
  paper exactly (5548/686/693 and 24048/2672/6680).
- P3: the toy 6-sentence mock corpus (replicated to N=100) is replaced by a real
  stratified slice of a public phishing/spam email corpus with sender and URL
  fields, frozen to disk so every re-run sees the identical benchmark.
- P3: per-sample telemetry (JSONL, flushed per sample) with gold label, both arm
  predictions, agent scores, latency, exact API-call count, token usage and cost.
- P3: provider-agnostic execution through litellm, with a guard that hard-fails on
  the Gemini versions forbidden by AGENTS.md.
- P3: one-sided McNemar now uses an exact binomial test (the chi-square
  approximation with the Edwards correction is reported only as a cross-check),
  plus Benjamini-Hochberg control and Clopper-Pearson bounds for FPR/recall.
- P2: UCI download fallback, measured (not asserted) footprint and latency for the
  supplementary ML baselines, and a single DistilBERT prediction pass.
- P1: transformers version shims (eval_strategy/evaluation_strategy,
  processing_class/tokenizer) and a resumable per-run JSONL log.

Everything below is generated code; the literature quotations are verbatim from
the primary PDFs and must not be paraphrased in any downstream report.
"""

import json
from pathlib import Path

OUT_DIR = Path("kaggle_notebooks")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def make_cell(cell_type: str, source: str) -> dict:
    lines = [line + "\n" for line in source.split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": lines,
    }
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell


def save_notebook(file_path: Path, cells: list):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.10.12",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Saved: {file_path} ({file_path.stat().st_size / 1024:.1f} KB)")


# ==============================================================================
# NOTEBOOK 1: ViSoBERT (EMNLP 2023 Main Conference)
# ==============================================================================
nb1_cells = [
    make_cell(
        "markdown",
        """# Repro Paper 1: *ViSoBERT: A Pre-trained Language Model for Vietnamese Social Media Text Processing*
**Venue:** EMNLP 2023 Main Conference (pp. 5191-5207)
**Authors:** Quoc-Nam Nguyen, Thang Chau Phan, Duc-Vu Nguyen, Kiet Van Nguyen
**Paper Link:** [ACL Anthology 2023.emnlp-main.315](https://aclanthology.org/2023.emnlp-main.315)
**Target:** Reproduce Table 4 benchmarks on the official UIT public datasets: `UIT-VSMEC` and `UIT-ViHSD`.

### Published Table 4 Targets (Macro F1 %):
| Model | UIT-VSMEC (Emotion, 7 classes) | UIT-ViHSD (Hate Speech, 3 classes) |
| :--- | :---: | :---: |
| `vinai/phobert-base` | 61.41 | 65.01 |
| `xlm-roberta-base` | 58.67 | 63.39 |
| **`uitnlp/visobert` (Ours)** | **65.88** | **68.77** |

### Dataset provenance (verified 2026-11-09 against the HF datasets-server)
| Task | Hub repository | Split sizes | Note |
| :--- | :--- | :--- | :--- |
| UIT-VSMEC | `duwuonline/UIT-VSMEC` | 5548 / 686 / 693 | Public mirror of the UIT release; columns `Sentence`, `Emotion` |
| UIT-ViHSD | `htdung167/ViHSD` | 24048 / 2672 / 6680 | Public mirror; columns `free_text`, `label_id` |

> The original `uitnlp/uit-vsmec` repository no longer resolves and `uitnlp/vihsd` is a gated
> repository (terms acceptance + token required). The mirrors above are used because their row
> counts match Table 2 of the paper exactly, which keeps the split-size assertions meaningful.
> This substitution is a documented deviation and must be disclosed in the report.

### Known Library & Implementation Deviations:
- **Original Paper:** Trained using `the simpletransformers` (ver 0.63.11 in footnote 15; default linear warmup, weight_decay = 0.0, AdamW eps = 1e-8). Procedures outlined in `(Devlin et al., 2019)`.
- **Dataset Names in Paper:** `UIT-VSMEC` (Emotion Recognition) and `UIT-ViHSD` (Hate Speech Detection).
- **This Replication:** Implemented via standard HuggingFace `Trainer` (`transformers` library).
- **Strict Anti-Data-Leakage:** Checkpoints are chosen strictly using validation (dev) Macro-F1 (`metric_for_best_model="macro_f1"`). The test set is evaluated exactly once after training, and the best-checkpoint selection never observes test labels.""",
    ),
    make_cell(
        "code",
        """# Cell 1: Environment Setup, Deterministic Seeding & Version Shims
# Kaggle's image ships transformers 5.x, whose build is incompatible with its own torch
# (torch._utils missing) -> AutoTokenizer cannot even be imported. Pin 4.x for this notebook.
!pip uninstall -y -q transformers
!pip install --no-cache-dir -q "transformers>=4.50,<5" "accelerate>=0.34" datasets evaluate scikit-learn sentencepiece

import inspect
import json
import os
import random
import numpy as np
import pandas as pd
import torch
from datasets import load_dataset, Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding,
    set_seed,
)
from sklearn.metrics import f1_score, accuracy_score

def set_deterministic_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    set_seed(seed)

set_deterministic_seed(42)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device} | CUDA Available: {torch.cuda.is_available()}")
print(f"transformers: {__import__('transformers').__version__}")
assert __import__("transformers").__version__.split(".")[0] == "4", (
    "Expected transformers 4.x. The two pip lines above must run, then "
    "Runtime -> Restart Session, then run this cell again."
)
print("AutoTokenizer import: OK")

# --- transformers version shims (4.x vs 5.x) ---
TA_FIELDS = getattr(TrainingArguments, "__dataclass_fields__", {})
EVAL_STRATEGY_KEY = "eval_strategy" if "eval_strategy" in TA_FIELDS else "evaluation_strategy"
print(f"Eval-strategy keyword: {EVAL_STRATEGY_KEY}")

def build_trainer(**kwargs):
    params = inspect.signature(Trainer.__init__).parameters
    if "processing_class" in params:
        kwargs["processing_class"] = kwargs.pop("tokenizer")
    return Trainer(**kwargs)""",
    ),
    make_cell(
        "code",
        """# Cell 2: Load Official UIT Datasets with Strict Split Assertions
# Execution order recommendation: run "UIT-VSMEC" first (fast, N_test=693), then append
# "UIT-ViHSD" (N_test=6680). Set the REPRO_TASKS env var to switch without editing code.
BENCHMARK_TASKS = [t for t in os.environ.get("REPRO_TASKS", "UIT-VSMEC").split(",") if t]

# Verified against the HF datasets-server on 2026-11-09.
DATASET_CANDIDATES = {
    "UIT-VSMEC": [
        ("duwuonline/UIT-VSMEC", "Sentence", "Emotion"),
        ("ura-hcmut/UIT-VSMEC", "Sentence", "Emotion"),
    ],
    "UIT-ViHSD": [
        ("htdung167/ViHSD", "free_text", "label_id"),
        ("SEACrowd/uit_vihsd", None, None),
    ],
}

EXPECTED_SPLITS = {
    "UIT-VSMEC": (5548, 686, 693),
    "UIT-ViHSD": (24048, 2672, 6680),
}

PUBLISHED_TABLE4 = {
    "UIT-VSMEC": {
        "vinai/phobert-base": {"MF1": 61.41, "WF1": 63.36, "Acc": 63.49},
        "xlm-roberta-base": {"MF1": 58.67, "WF1": 61.02, "Acc": 60.92},
        "uitnlp/visobert": {"MF1": 65.88, "WF1": 68.37, "Acc": 68.10},
    },
    "UIT-ViHSD": {
        "vinai/phobert-base": {"MF1": 65.01, "WF1": 86.81, "Acc": 87.12},
        "xlm-roberta-base": {"MF1": 63.39, "WF1": 86.08, "Acc": 86.36},
        "uitnlp/visobert": {"MF1": 68.77, "WF1": 88.31, "Acc": 88.51},
    },
}

def _resolve_columns(ds, text_col, label_col):
    feats = list(ds["train"].features.keys())
    if text_col is None or text_col not in feats:
        candidates = [c for c in feats if ds["train"].features[c].dtype == "string"]
        text_col = candidates[0] if candidates else None
    if label_col is None or label_col not in feats:
        for c in feats:
            if c.lower() in ("label", "label_id", "labels", "emotion", "target"):
                label_col = c
                break
    if text_col is None or label_col is None:
        raise ValueError(f"Could not resolve text/label columns from features: {feats}")
    return text_col, label_col

def load_official_uit_dataset(task_name: str):
    expected = EXPECTED_SPLITS[task_name]
    errors = []
    for repo, text_col, label_col in DATASET_CANDIDATES[task_name]:
        try:
            ds = load_dataset(repo)
        except Exception as exc:  # noqa: BLE001 - we want the reason logged, not raised yet
            errors.append(f"{repo}: {exc}")
            print(f"[skip] {repo} -> {type(exc).__name__}: {exc}")
            continue

        def pick(*names):
            for n in names:
                if n in ds:
                    return n
            return None

        tr_k, va_k, te_k = pick("train"), pick("validation", "dev"), pick("test")
        if tr_k is None or te_k is None:
            errors.append(f"{repo}: missing train/test split (found {list(ds.keys())})")
            continue

        text_col, label_col = _resolve_columns(ds, text_col, label_col)
        train_df = pd.DataFrame(ds[tr_k])
        test_df = pd.DataFrame(ds[te_k])

        deviation_note = ""
        if va_k is not None:
            val_df = pd.DataFrame(ds[va_k])
        else:
            # Honest fallback: carve a stratified dev split out of train and DISCLOSE it.
            from sklearn.model_selection import train_test_split
            train_df, val_df = train_test_split(
                train_df, test_size=0.1, random_state=42, stratify=train_df[label_col]
            )
            deviation_note = "NO-DEV-SPLIT FALLBACK: 10% stratified carve from train"

        got = (len(train_df), len(val_df), len(test_df))
        strict_ok = got == expected
        print(f"[{repo}] splits found: train={got[0]}, dev={got[1]}, test={got[2]} "
              f"(paper Table 2: {expected[0]}/{expected[1]}/{expected[2]})")
        if not strict_ok and not deviation_note:
            errors.append(f"{repo}: split mismatch {got} != {expected}")
            continue

        unique_labels = sorted(pd.concat([train_df, val_df, test_df])[label_col].unique().tolist())
        label2id = {lbl: idx for idx, lbl in enumerate(unique_labels)}
        for df in (train_df, val_df, test_df):
            df["text"] = df[text_col].astype(str)
            df["label"] = df[label_col].map(label2id).astype(int)

        print(f"[{task_name}] source={repo} text_col={text_col} label_col={label_col} "
              f"classes={len(unique_labels)} {deviation_note}")
        print(f"[{task_name}] class counts (train): "
              f"{train_df['label'].value_counts().sort_index().to_dict()}")
        assert len(test_df) == expected[2], "test split must match the paper exactly"
        return (
            train_df[["text", "label"]],
            val_df[["text", "label"]],
            test_df[["text", "label"]],
            len(unique_labels),
            repo,
        )
    raise RuntimeError(
        "No usable public source for " + task_name + ". Tried:\\n  " + "\\n  ".join(errors)
    )

# Probe the datasets without training so a broken pin fails fast.
for _task in BENCHMARK_TASKS:
    _tr, _va, _te, _n, _src = load_official_uit_dataset(_task)
    print(f"OK {_task}: {_src} | N_test={len(_te)} | classes={_n}")""",
    ),
    make_cell(
        "code",
        """# Cell 3: Multi-Seed Replication Pipeline with Dev Checkpoint Selection
import gc
import time

MODELS = ["xlm-roberta-base", "vinai/phobert-base", "uitnlp/visobert"]
SEEDS = [42, 43, 44]
RUN_LOG = "Repro_Paper1_runs.jsonl"
LATENCY_SAMPLES = 50

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {
        "macro_f1": f1_score(labels, preds, average="macro") * 100.0,
        "weighted_f1": f1_score(labels, preds, average="weighted") * 100.0,
        "accuracy": accuracy_score(labels, preds) * 100.0,
    }

def measure_cpu_latency(model, tokenizer, texts, max_length=128, warmup=20, reps=LATENCY_SAMPLES):
    # Measure a fp32 CPU copy so fp16 weights never hit CPU-only kernels; the GPU model
    # under evaluation stays untouched.
    import copy
    cpu_model = copy.deepcopy(model).float().to("cpu").eval()
    sample = [t[:512] for t in texts[:reps]]
    with torch.no_grad():
        for _ in range(warmup):
            _ = cpu_model(**tokenizer(sample[0], return_tensors="pt", truncation=True,
                                     max_length=max_length))
        lats = []
        for txt in sample:
            enc = tokenizer(txt, return_tensors="pt", truncation=True, max_length=max_length)
            t0 = time.perf_counter_ns()
            _ = cpu_model(**enc)
            lats.append(time.perf_counter_ns() - t0)
    del cpu_model
    return float(np.mean(lats)) / 1e6, float(np.percentile(lats, 95)) / 1e6

results_log = []
raw_predictions = {}

# --- Resume support: skip runs already written to RUN_LOG and reuse their preds CSV ---
_log_rows = []
if os.path.exists(RUN_LOG):
    with open(RUN_LOG, encoding="utf-8") as _f:
        for _line in _f:
            try:
                _log_rows.append(json.loads(_line))
            except Exception:
                pass
_done = {(r["task"], r["model"], r["seed"]) for r in _log_rows}
print(f"[resume] {len(_done)} run(s) already logged")

for task in BENCHMARK_TASKS:
    train_df, val_df, test_df, num_labels, source_repo = load_official_uit_dataset(task)
    raw_predictions[task] = {}

    for model_name in MODELS:
        seed_metrics = []
        raw_predictions[task][model_name] = {}

        for seed in SEEDS:
            if (task, model_name, seed) in _done:
                _p = f"Repro_Paper1_preds_{task}_{model_name.replace('/', '_')}_s{seed}.csv"
                if os.path.exists(_p):
                    raw_predictions[task][model_name][seed] = pd.read_csv(_p)["pred"].values
                    _rec = next((r for r in _log_rows
                                 if (r["task"], r["model"], r["seed"]) == (task, model_name, seed)),
                                None)
                    if _rec:
                        results_log.append(_rec)
                        seed_metrics.append((_rec["macro_f1"], _rec["weighted_f1"],
                                             _rec["accuracy"]))
                    print(f"[skip] {model_name} | seed {seed} (already done)")
                else:
                    print(f"[warn] logged but preds file missing: {model_name} s{seed} -> rerun")
                continue

            print(f"\\n>>> Fine-tuning {model_name} on {task} (Seed: {seed}) <<<")
            set_deterministic_seed(seed)
            tokenizer = AutoTokenizer.from_pretrained(model_name)

            def tokenize_fn(batch, _tok=tokenizer):
                return _tok(batch["text"], truncation=True, max_length=128)

            tr_ds = Dataset.from_pandas(train_df).map(tokenize_fn, batched=True)
            va_ds = Dataset.from_pandas(val_df).map(tokenize_fn, batched=True)
            te_ds = Dataset.from_pandas(test_df).map(tokenize_fn, batched=True)

            model = AutoModelForSequenceClassification.from_pretrained(
                model_name, num_labels=num_labels
            )

            # Exact hyperparameters from ViSoBERT Section 4.1:
            # batch_size=40, max_seq_length=128, lr=2e-5, epochs=10, weight_decay=0.0
            train_args_kwargs = dict(
                output_dir=f"./checkpoints_{task}_{model_name.replace('/', '_')}_s{seed}",
                save_strategy="epoch",
                learning_rate=2e-5,
                per_device_train_batch_size=40,
                per_device_eval_batch_size=40,
                num_train_epochs=10,
                weight_decay=0.0,
                adam_epsilon=1e-8,
                warmup_ratio=0.1,
                load_best_model_at_end=True,
                metric_for_best_model="macro_f1",
                greater_is_better=True,
                fp16=torch.cuda.is_available(),
                logging_steps=50,
                report_to="none",
                save_total_limit=1,
                seed=seed,
            )
            train_args_kwargs[EVAL_STRATEGY_KEY] = "epoch"
            # transformers 5.x dropped several 4.x TrainingArguments fields (e.g. adam_epsilon).
            # Drop anything this installed version does not accept instead of dying mid-run.
            _supported = set(getattr(TrainingArguments, "__dataclass_fields__", {}))
            if _supported:
                _dropped = {k: v for k, v in train_args_kwargs.items() if k not in _supported}
                if _dropped:
                    print(f"[compat] transformers {__import__('transformers').__version__} "
                          f"does not accept: {sorted(_dropped)} -> dropped")
                train_args_kwargs = {k: v for k, v in train_args_kwargs.items()
                                     if k in _supported}
            if "fp16" not in train_args_kwargs:
                print("[compat] fp16 not applied on this version -> training in fp32 "
                      "(slower; record this in the report)")
            training_args = TrainingArguments(**train_args_kwargs)

            trainer = build_trainer(
                model=model,
                args=training_args,
                train_dataset=tr_ds,
                eval_dataset=va_ds,
                tokenizer=tokenizer,
                data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
                compute_metrics=compute_metrics,
            )

            trainer.train()

            # Held-out test inference, exactly once, with the best dev checkpoint.
            test_preds_out = trainer.predict(te_ds)
            test_preds = np.argmax(test_preds_out.predictions, axis=-1)
            raw_predictions[task][model_name][seed] = test_preds

            mf1 = f1_score(test_df["label"], test_preds, average="macro") * 100.0
            wf1 = f1_score(test_df["label"], test_preds, average="weighted") * 100.0
            acc = accuracy_score(test_df["label"], test_preds) * 100.0
            seed_metrics.append((mf1, wf1, acc))

            n_params = sum(p.numel() for p in model.parameters())
            fp32_mb = n_params * 4 / (1024 ** 2)
            mean_ms, p95_ms = measure_cpu_latency(
                model, tokenizer, test_df["text"].tolist()
            )

            record = {
                "task": task,
                "source_repo": source_repo,
                "model": model_name,
                "seed": seed,
                "n_test": int(len(test_df)),
                "macro_f1": round(mf1, 4),
                "weighted_f1": round(wf1, 4),
                "accuracy": round(acc, 4),
                "params": int(n_params),
                "fp32_mib": round(fp32_mb, 2),
                "cpu_latency_mean_ms": round(mean_ms, 3),
                "cpu_latency_p95_ms": round(p95_ms, 3),
            }
            results_log.append(record)
            with open(RUN_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\\n")

            print(f"[{model_name} | Seed {seed}] Test: MF1={mf1:.2f}%, WF1={wf1:.2f}%, "
                  f"Acc={acc:.2f}%, params={n_params:,} (~{fp32_mb:.1f} MiB FP32), "
                  f"CPU {mean_ms:.2f} ms/sample")

            # Store per-sample predictions for the paired tests.
            pd.DataFrame({
                "idx": np.arange(len(test_df)),
                "gold": test_df["label"].values,
                "pred": test_preds,
            }).to_csv(
                f"Repro_Paper1_preds_{task}_{model_name.replace('/', '_')}_s{seed}.csv",
                index=False,
            )

            # Free VRAM before the next run: 9 sequential fine-tunes otherwise fragment
            # the caching allocator and OOM around run 5-9.
            del model, trainer
            gc.collect()
            torch.cuda.empty_cache()

        m_vals = [m[0] for m in seed_metrics]
        target_mf1 = PUBLISHED_TABLE4[task][model_name]["MF1"]
        mean_mf1 = float(np.mean(m_vals))
        std_mf1 = float(np.std(m_vals, ddof=1)) if len(m_vals) > 1 else 0.0
        print(f"== {model_name} on {task}: {mean_mf1:.2f} +/- {std_mf1:.2f} MF1 "
              f"(paper {target_mf1:.2f}) ==")

df_res = pd.DataFrame(results_log)
df_res.to_csv("Repro_Paper1_ViSoBERT_EMNLP2023_Comparison.csv", index=False)
display(df_res)""",
    ),
    make_cell(
        "code",
        """# Cell 4: Multi-Class Statistical Verification
# McNemar is for paired binary decisions. For the multi-class Macro-F1 difference on
# 7-class UIT-VSMEC we use a paired bootstrap over the test set, and for the
# "Kaggle vs paper target" comparison we use an equivalence bound (never McNemar).
from scipy import stats as sps

BOOT_B = 2000
EQUIVALENCE_MARGIN_PP = 2.0  # pre-registered, do not tune after seeing results

def paired_bootstrap_mf1_diff(y_true, preds_a, preds_b, n_bootstraps=BOOT_B, alpha=0.05, seed=42):
    rng = np.random.RandomState(seed)
    n = len(y_true)
    diffs = []
    for _ in range(n_bootstraps):
        idx = rng.choice(n, size=n, replace=True)
        if len(np.unique(y_true[idx])) < 2:
            continue
        f1_a = f1_score(y_true[idx], preds_a[idx], average="macro") * 100.0
        f1_b = f1_score(y_true[idx], preds_b[idx], average="macro") * 100.0
        diffs.append(f1_a - f1_b)
    diffs = np.asarray(diffs)
    low, high = np.percentile(diffs, [alpha / 2 * 100, (1 - alpha / 2) * 100])
    # Add-one bootstrap p-value: never report an impossible exact 0.0000.
    p_val = (np.sum(diffs <= 0.0) + 1) / (len(diffs) + 1)
    return {
        "mean_diff": float(diffs.mean()),
        "ci_95": (round(float(low), 2), round(float(high), 2)),
        "p_value": float(p_val),
        "p_value_floor": f"< {1 / (len(diffs) + 1):.4f}",
        "is_significant": bool(low > 0.0),
        "n_boot": int(len(diffs)),
    }

def bootstrap_ci_metric(y_true, y_pred, metric="macro_f1", n_bootstraps=BOOT_B, seed=42):
    rng = np.random.RandomState(seed)
    n = len(y_true)
    vals = []
    for _ in range(n_bootstraps):
        idx = rng.choice(n, size=n, replace=True)
        if len(np.unique(y_true[idx])) < 2:
            continue
        if metric == "macro_f1":
            vals.append(f1_score(y_true[idx], y_pred[idx], average="macro") * 100.0)
        elif metric == "accuracy":
            vals.append(accuracy_score(y_true[idx], y_pred[idx]) * 100.0)
    vals = np.asarray(vals)
    return (round(float(np.percentile(vals, 2.5)), 2),
            round(float(np.percentile(vals, 97.5)), 2))

def benjamini_hochberg(p_values, alpha=0.05):
    p = np.asarray(p_values, dtype=float)
    order = np.argsort(p)
    m = len(p)
    adjusted = np.empty(m)
    prev = 1.0
    for rank in range(m - 1, -1, -1):
        idx = order[rank]
        prev = min(prev, p[idx] * m / (rank + 1))
        adjusted[idx] = prev
    return adjusted, adjusted < alpha

def clopper_pearson(k, n, alpha=0.05):
    if n == 0:
        return (float("nan"), float("nan"))
    lo = 0.0 if k == 0 else sps.beta.ppf(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else sps.beta.ppf(1 - alpha / 2, k + 1, n - k)
    return round(float(lo) * 100, 2), round(float(hi) * 100, 2)

summary_rows = []
pvals_for_bh = []

for task in BENCHMARK_TASKS:
    y_test = load_official_uit_dataset(task)[2]["label"].values
    if "uitnlp/visobert" not in raw_predictions.get(task, {}):
        continue
    p_vis = raw_predictions[task]["uitnlp/visobert"][42]
    for baseline in ["vinai/phobert-base", "xlm-roberta-base"]:
        if baseline not in raw_predictions[task]:
            continue
        p_base = raw_predictions[task][baseline][42]
        boot = paired_bootstrap_mf1_diff(y_test, p_vis, p_base)
        ci = bootstrap_ci_metric(y_test, p_vis)
        target = PUBLISHED_TABLE4[task]["uitnlp/visobert"]["MF1"]
        lower_bound = target - EQUIVALENCE_MARGIN_PP
        observed = f1_score(y_test, p_vis, average="macro") * 100.0
        pvals_for_bh.append(boot["p_value"])
        summary_rows.append({
            "task": task,
            "comparison": f"ViSoBERT vs {baseline}",
            "delta_mf1_pp": round(boot["mean_diff"], 2),
            "delta_ci95": str(boot["ci_95"]),
            "p_value": round(boot["p_value"], 4),
            "significant": boot["is_significant"],
            "visobert_obs_mf1": round(observed, 2),
            "visobert_boot_ci95": str(ci),
            "paper_target_mf1": target,
            "within_equivalence_margin": bool(ci[0] >= lower_bound),
            "rank_order_holds": bool(observed > (f1_score(y_test, p_base, average="macro") * 100.0)),
        })
        print(f"\\n=== {task}: ViSoBERT vs {baseline} (Seed 42) ===")
        print(f"Delta Macro-F1 = {boot['mean_diff']:.2f} pp | 95% CI {boot['ci_95']} | "
              f"p = {boot['p_value']:.4f} | significant={boot['is_significant']}")
        print(f"ViSoBERT observed MF1 = {observed:.2f}% (bootstrap CI {ci}), "
              f"paper target = {target:.2f}%, equivalence floor = {lower_bound:.2f}")

if summary_rows:
    adj, reject = benjamini_hochberg(pvals_for_bh)
    for row, a, r in zip(summary_rows, adj, reject):
        row["p_bh_adjusted"] = round(float(a), 4)
        row["significant_bh"] = bool(r)
    df_stats = pd.DataFrame(summary_rows)
    df_stats.to_csv("Repro_Paper1_Statistical_Concordance.csv", index=False)
    display(df_stats)
    print("\\nBH-corrected decisions are in `significant_bh`. Report both raw and adjusted p-values.")""",
    ),
]
save_notebook(
    OUT_DIR / "Repro_Paper1_ViSoBERT_EMNLP2023_Original.ipynb", nb1_cells
)


# ==============================================================================
# NOTEBOOK 2: Edge-AI BiGRU + WBCE (H. C. Phap, 2026)
# ==============================================================================
nb2_cells = [
    make_cell(
        "markdown",
        r"""# Repro Paper 2: *Edge-AI Smishing Detection with Weighted BCE*
**Venue:** Journal of Information and Telecommunication, 2026 (M041)
**Author:** Huynh Cong Phap (DOI: 10.1080/24751839.2026.2713250)
**Dataset:** UCI SMS Spam Collection ($N=5,574$), 80/20 train/test split ($N_{\text{test}}=1,115$: 965 ham, 150 spam).

### Primary Literature Quotes & Implementation Details:
1. **Model & Pooling:** *"combining a Bidirectional Gated Recurrent Unit (BiGRU) encoder with Masked Global Pooling to strictly exclude padding noise from pooled representations"* (H. C. Phap, JIT 2026).
2. **Hardware Profiling:** *"requires only a 5.21 MB serialized footprint and 0.25 ms CPU latency, compared to 256.02 MB and 40.78 ms for DistilBERT"* (H. C. Phap, JIT 2026).
3. **Loss Function (WBCE):**
   - The original paper formulates inverse class weighting as $w_1 = N / (2N_1)$ and $w_0 = N / (2N_0)$.
   - In PyTorch `nn.BCEWithLogitsLoss(pos_weight=...)`, the relative positive weight equals $w_1 / w_0 = N_0 / N_1 = 4,827 / 747 \approx 6.46$ (derived for the PyTorch implementation; this is an implementation derivation, not a quotation).
4. **Evaluation Setup:** The original paper evaluates across 5 stratified folds/seeds. Here we use a single pre-registered 80/20 stratified split ($N_{\text{test}}=1,115$: 965 ham, 150 spam) and profile CPU latency.

> **Known deviation:** a single split gives one realization of the test set, so the WBCE-vs-BCE comparison is a paired comparison on the same $N=1,115$ rows, not a cross-fold mean. Do not report it as a 5-fold replication.""",
    ),
    make_cell(
        "code",
        """# Cell 1: Environment Setup & Dataset Ingestion (with mirror fallback)
!pip install -q torch scikit-learn pandas numpy xgboost transformers

import io
import json
import os
import pickle
import time
import urllib.request
import zipfile
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)

torch.manual_seed(42)
np.random.seed(42)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")

UCI_ZIP_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
MIRROR_TSV_URL = (
    "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
)

def load_uci_sms() -> pd.DataFrame:
    # Primary source: the UCI archive itself.
    try:
        zip_path = "sms_spam.zip"
        if not os.path.exists(zip_path):
            urllib.request.urlretrieve(UCI_ZIP_URL, zip_path)
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall("uci_sms")
        frame = pd.read_csv("uci_sms/SMSSpamCollection", sep="\\t", names=["label_str", "text"])
        print("Source: UCI archive (SMSSpamCollection)")
        return frame
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] UCI archive unavailable ({type(exc).__name__}: {exc}); trying mirror")

    # Fallback: public TSV mirror with a header row.
    try:
        with urllib.request.urlopen(MIRROR_TSV_URL, timeout=60) as resp:
            mirror = pd.read_csv(io.StringIO(resp.read().decode("utf-8")), sep="\\t")
        mirror = mirror.rename(columns={"message": "text", "label": "label_str"})
        print("Source: GitHub TSV mirror (justmarkham/pycon-2016-tutorial)")
        return mirror[["label_str", "text"]]
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            "Could not download the UCI SMS Spam Collection from either source. "
            "Attach the Kaggle 'sms-spam-collection-dataset' as an input and set "
            "UCI_SMS_PATH to the local CSV."
        ) from exc

local_path = os.environ.get("UCI_SMS_PATH")
if local_path and os.path.exists(local_path):
    df = pd.read_csv(local_path, sep="\\t", names=["label_str", "text"])
    print(f"Source: local file {local_path}")
else:
    df = load_uci_sms()

df = df.dropna(subset=["text"]).reset_index(drop=True)
df["label"] = (df["label_str"].str.strip().str.lower() == "spam").astype(int)
assert len(df) == 5574, f"Dataset size mismatch: {len(df)} != 5574"
print(f"UCI SMS verified: N={len(df)} | ham={(df['label'] == 0).sum()} | "
      f"spam={(df['label'] == 1).sum()}")

train_df, test_df = train_test_split(
    df, test_size=0.2, random_state=42, stratify=df["label"]
)
assert len(test_df) == 1115, f"Expected 1,115 test rows, got {len(test_df)}"
observed_counts = test_df["label"].value_counts().sort_index().to_dict()
if observed_counts != {0: 965, 1: 150}:
    print(f"[warn] test class counts {observed_counts} differ from the protocol's "
          f"{{0: 965, 1: 150}}; the integer counts below remain authoritative.")
print(f"Split verified: Train={len(train_df)} | Test={len(test_df)} {observed_counts}")""",
    ),
    make_cell(
        "code",
        """# Cell 2: Tokenization & CostSensitiveBiGRU Architecture
# Vocabulary construction is fitted on the TRAIN split only (leakage prevention).
word_counts = {}
for text in train_df["text"]:
    for token in str(text).lower().split():
        word_counts[token] = word_counts.get(token, 0) + 1

VOCAB_SIZE = 15000
sorted_vocab = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:VOCAB_SIZE - 2]
vocab = {"<PAD>": 0, "<UNK>": 1}
for word, _ in sorted_vocab:
    vocab[word] = len(vocab)

def text_pipeline(text, max_len=100):
    tokens = [vocab.get(w, 1) for w in str(text).lower().split()][:max_len]
    length = max(len(tokens), 1)
    padded = tokens + [0] * (max_len - len(tokens))
    return padded, length

class SMSDataset(Dataset):
    def __init__(self, frame):
        self.samples = [text_pipeline(t) for t in frame["text"]]
        self.labels = frame["label"].values.astype(np.float32)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        padded, length = self.samples[idx]
        return (torch.tensor(padded, dtype=torch.long),
                torch.tensor(length, dtype=torch.long),
                torch.tensor(self.labels[idx], dtype=torch.float))

train_loader = DataLoader(SMSDataset(train_df), batch_size=64, shuffle=True)
test_loader = DataLoader(SMSDataset(test_df), batch_size=64, shuffle=False)

class CostSensitiveBiGRU(nn.Module):
    # BiGRU + Masked Global Max & Average Pooling (H. C. Phap, 2026).
    # Dual-branch pooling is concatenated: in_features = hidden_dim * 4.
    def __init__(self, vocab_sz=15000, embed_dim=64, hidden_dim=64):
        super().__init__()
        self.embedding = nn.Embedding(vocab_sz, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 4, 1)

    def forward(self, input_ids, lengths):
        emb = self.embedding(input_ids)
        packed = pack_padded_sequence(
            emb, lengths.cpu(), batch_first=True, enforce_sorted=False
        )
        packed_out, _ = self.gru(packed)
        # total_length keeps the time dimension consistent when batch_size == 1.
        out, _ = pad_packed_sequence(
            packed_out, batch_first=True, total_length=input_ids.size(1)
        )

        mask = (input_ids != 0).unsqueeze(-1)
        out_masked_for_max = out.masked_fill(~mask, -1e9)
        max_pool = torch.max(out_masked_for_max, dim=1)[0]

        out_masked_for_avg = out.masked_fill(~mask, 0.0)
        lens = lengths.unsqueeze(1).float().clamp(min=1.0)
        avg_pool = torch.sum(out_masked_for_avg, dim=1) / lens

        pooled = torch.cat([max_pool, avg_pool], dim=1)
        return self.fc(pooled).squeeze(-1)

temp_model = CostSensitiveBiGRU()
total_params = sum(p.numel() for p in temp_model.parameters())
raw_weight_mb = total_params * 4 / (1024 * 1024)
print(f"CostSensitiveBiGRU Parameter Count: {total_params:,} parameters")
print(f"Calculated Raw FP32 Weight Size: {raw_weight_mb:.2f} MiB")
print("Note: the paper reports 5.21 MB; the exact hidden/embedding dimensions are not "
      "fully disclosed, so the measured footprint here is reported as-is.")""",
    ),
    make_cell(
        "code",
        """# Cell 3: Training & Loss Function Ablation (Standard BCE vs. WBCE)
def train_model(wbce_weight=1.0, epochs=8, seed=42):
    torch.manual_seed(seed)
    np.random.seed(seed)
    model = CostSensitiveBiGRU().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    pos_weight = torch.tensor([wbce_weight], device=device)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

    for _ in range(epochs):
        model.train()
        for ids, lens, labels in train_loader:
            ids, lens, labels = ids.to(device), lens.to(device), labels.to(device)
            optimizer.zero_grad()
            loss = criterion(model(ids, lens), labels)
            loss.backward()
            optimizer.step()
    return model

POS_WEIGHT = len(df[df["label"] == 0]) / len(df[df["label"] == 1])
print(f"Derived pos_weight = N_ham / N_spam = {POS_WEIGHT:.4f}")

print("Training Variant 1: BiGRU + Standard BCE (w=1.0)...")
model_bce = train_model(wbce_weight=1.0)

print(f"Training Variant 2: BiGRU + WBCE (w={POS_WEIGHT:.2f}, derived from the paper's weighting)...")
model_wbce = train_model(wbce_weight=POS_WEIGHT)

def evaluate_model(model):
    model.eval()
    all_preds, all_probs, all_labels = [], [], []
    with torch.no_grad():
        for ids, lens, labels in test_loader:
            ids, lens = ids.to(device), lens.to(device)
            probs = torch.sigmoid(model(ids, lens))
            all_probs.extend(probs.cpu().numpy())
            all_preds.extend((probs >= 0.5).int().cpu().numpy())
            all_labels.extend(labels.numpy())
    return np.array(all_labels).astype(int), np.array(all_preds), np.array(all_probs)

y_true, preds_bce, probs_bce = evaluate_model(model_bce)
_, preds_wbce, probs_wbce = evaluate_model(model_wbce)

def full_metrics(y_t, y_p, name):
    tn, fp, fn, tp = confusion_matrix(y_t, y_p, labels=[0, 1]).ravel()
    return {
        "Variant": name,
        "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp),
        "N": int(tn + fp + fn + tp),
        "Spam Recall (%)": round(recall_score(y_t, y_p) * 100, 2),
        "Precision (%)": round(precision_score(y_t, y_p, zero_division=0) * 100, 2),
        "F1 (%)": round(f1_score(y_t, y_p) * 100, 2),
        "Accuracy (%)": round(accuracy_score(y_t, y_p) * 100, 2),
        "FPR (%)": round(fp / max(fp + tn, 1) * 100, 2),
    }

rows = [
    full_metrics(y_true, preds_bce, "BiGRU + Standard BCE"),
    full_metrics(y_true, preds_wbce, "BiGRU + WBCE"),
]
df_ablation = pd.DataFrame(rows)
for row in rows:
    assert row["N"] == 1115, f"Denominator integrity violated: {row}"
display(df_ablation)
df_ablation.to_csv("Repro_Paper2_WBCE_Ablation.csv", index=False)

# Per-sample telemetry for the statistical audit.
pd.DataFrame({
    "idx": np.arange(len(y_true)),
    "gold": y_true,
    "pred_bce": preds_bce,
    "prob_bce": np.round(probs_bce, 6),
    "pred_wbce": preds_wbce,
    "prob_wbce": np.round(probs_wbce, 6),
}).to_csv("Repro_Paper2_per_sample_predictions.csv", index=False)

recall_gain = rows[1]["Spam Recall (%)"] - rows[0]["Spam Recall (%)"]
print(f"\\nSpam recall change under WBCE: {recall_gain:+.2f} pp")
print("Paired decisions on identical rows -> McNemar is admissible here.")""",
    ),
    make_cell(
        "code",
        """# Cell 4: Hardware Benchmarking (CPU Latency & Serialized Footprint)
torch.save(model_wbce.state_dict(), "bigru_wbce.pt")
measured_mb = os.path.getsize("bigru_wbce.pt") / (1024 * 1024)

cpu_model = model_wbce.to("cpu").eval()
test_samples = [text_pipeline(t) for t in test_df["text"].iloc[:500]]

with torch.no_grad():
    for _ in range(50):
        p0, l0 = test_samples[0]
        _ = cpu_model(torch.tensor([p0], dtype=torch.long), torch.tensor([l0], dtype=torch.long))

latencies_ns = []
with torch.no_grad():
    for p, l in test_samples:
        t0 = time.perf_counter_ns()
        _ = cpu_model(torch.tensor([p], dtype=torch.long), torch.tensor([l], dtype=torch.long))
        latencies_ns.append(time.perf_counter_ns() - t0)

mean_cpu_latency_ms = float(np.mean(latencies_ns)) / 1e6
p95_cpu_latency_ms = float(np.percentile(latencies_ns, 95)) / 1e6
latencies_cold_ns = []
with torch.no_grad():
    for p, l in test_samples[:100]:
        t0 = time.perf_counter_ns()
        _ = cpu_model(torch.tensor([p], dtype=torch.long), torch.tensor([l], dtype=torch.long))
        latencies_cold_ns.append(time.perf_counter_ns() - t0)

print("=== HARDWARE AUDIT: CostSensitiveBiGRU ===")
print(f"Serialized footprint (state_dict on disk): {measured_mb:.2f} MB")
print(f"CPU single-sample latency (warm, n=500): {mean_cpu_latency_ms:.3f} ms "
      f"(P95 {p95_cpu_latency_ms:.3f} ms)")
print(f"CPU single-sample latency (no warm-up, n=100): "
      f"{float(np.mean(latencies_cold_ns)) / 1e6:.3f} ms")
print("Paper reference: 5.21 MB and 0.25 ms (hardware unspecified in the paper).")
print("Report the measured numbers, not the paper's, and state the hardware used.")""",
    ),
    make_cell(
        "code",
        """# Cell 5: Supplementary Baselines (DistilBERT & Classical ML) with MEASURED cost
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from datasets import Dataset

comparison_rows = [{
    "Model": "BiGRU + WBCE (H. C. Phap 2026)",
    "Spam Recall (%)": rows[1]["Spam Recall (%)"],
    "F1 (%)": rows[1]["F1 (%)"],
    "Footprint (MB)": round(measured_mb, 2),
    "CPU Latency (ms)": round(mean_cpu_latency_ms, 3),
    "Type": "Proposed Edge Architecture",
}]

# --- 1. DistilBERT: single training pass, single prediction pass ---
distil_tok = AutoTokenizer.from_pretrained("distilbert-base-uncased")
def dist_tok_fn(b):
    return distil_tok(b["text"], truncation=True, max_length=128)

tr_ds = Dataset.from_pandas(train_df[["text"]]).map(dist_tok_fn, batched=True)
te_ds = Dataset.from_pandas(test_df[["text"]]).map(dist_tok_fn, batched=True)

distil_mod = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2
)
d_trainer = Trainer(
    model=distil_mod,
    args=TrainingArguments(
        output_dir="./distil_out",
        per_device_train_batch_size=32,
        num_train_epochs=3,
        weight_decay=0.01,
        fp16=torch.cuda.is_available(),
        report_to="none",
        save_strategy="no",
    ),
    train_dataset=tr_ds,
)
d_trainer.train()

distil_logits = d_trainer.predict(te_ds).predictions
distil_preds = np.argmax(distil_logits, axis=-1)
distil_f1 = f1_score(test_df["label"].values, distil_preds) * 100
distil_recall = recall_score(test_df["label"].values, distil_preds) * 100

torch.save(distil_mod.state_dict(), "distilbert_uci.pt")
distil_mb = os.path.getsize("distilbert_uci.pt") / (1024 * 1024)

distil_cpu = distil_mod.to("cpu").eval()
sample_texts = test_df["text"].iloc[:100].tolist()
with torch.no_grad():
    for _ in range(10):
        _ = distil_cpu(**distil_tok(sample_texts[0], return_tensors="pt", truncation=True,
                                    max_length=128))
    d_lats = []
    for txt in sample_texts:
        inp = distil_tok(txt, return_tensors="pt", truncation=True, max_length=128)
        t0 = time.perf_counter_ns()
        _ = distil_cpu(**inp)
        d_lats.append(time.perf_counter_ns() - t0)
distil_cpu_ms = float(np.mean(d_lats)) / 1e6

comparison_rows.append({
    "Model": "DistilBERT (H. C. Phap 2026 baseline)",
    "Spam Recall (%)": round(float(distil_recall), 2),
    "F1 (%)": round(float(distil_f1), 2),
    "Footprint (MB)": round(distil_mb, 2),
    "CPU Latency (ms)": round(distil_cpu_ms, 3),
    "Type": "Official Transformer Baseline",
})

# --- 2. Classical ML: footprint and latency are MEASURED, not asserted ---
tfidf = TfidfVectorizer(max_features=5000)
X_tr = tfidf.fit_transform(train_df["text"])
X_te = tfidf.transform(test_df["text"])
y_tr = train_df["label"].values
y_te = test_df["label"].values

ml_models = {
    "TF-IDF + LR (Supplementary)": LogisticRegression(max_iter=1000),
    "TF-IDF + Linear SVM (Supplementary)": LinearSVC(),
    "TF-IDF + Random Forest (Supplementary)": RandomForestClassifier(
        n_estimators=100, random_state=42),
    "TF-IDF + XGBoost (Supplementary)": XGBClassifier(
        n_estimators=100, random_state=42, eval_metric="logloss"),
}

lat_probe = test_df["text"].iloc[:100].tolist()
for name, clf in ml_models.items():
    clf.fit(X_tr, y_tr)
    pred = clf.predict(X_te)
    blob = pickle.dumps({"vectorizer": tfidf, "clf": clf})
    for _ in range(5):
        _ = clf.predict(tfidf.transform([lat_probe[0]]))
    lats = []
    for txt in lat_probe:
        t0 = time.perf_counter_ns()
        _ = clf.predict(tfidf.transform([txt]))
        lats.append(time.perf_counter_ns() - t0)
    comparison_rows.append({
        "Model": name,
        "Spam Recall (%)": round(float(recall_score(y_te, pred)) * 100, 2),
        "F1 (%)": round(float(f1_score(y_te, pred)) * 100, 2),
        "Footprint (MB)": round(len(blob) / (1024 * 1024), 2),
        "CPU Latency (ms)": round(float(np.mean(lats)) / 1e6, 3),
        "Type": "Supplementary Baseline",
    })

res_df = pd.DataFrame(comparison_rows)
res_df.to_csv("Repro_Paper2_UCI_SMS_Comparison.csv", index=False)
display(res_df)
print("Footprint = pickled vectorizer+model (ML) or state_dict (neural); "
      "latency = single-message end-to-end predict on CPU, this machine.")""",
    ),
]
save_notebook(
    OUT_DIR
    / "Repro_Paper2_EdgeAI_WBCE_and_ExplainableDetector_UCI5574.ipynb",
    nb2_cells,
)


# ==============================================================================
# NOTEBOOK 3: MultiPhishGuard (Yinuo Xue et al., arXiv:2505.23803v2, 2026)
# ==============================================================================
nb3_cells = [
    make_cell(
        "markdown",
        """# Repro Paper 3: *MultiPhishGuard: An Explainable and Adaptive Multi-Agent LLM System for Phishing Email Detection*
**Venue:** arXiv:2505.23803v2 [cs.CR] (revised 23 May 2026; v1 submitted 26 May 2025)
**Authors:** Yinuo Xue, Eric Spero, Meng Wai Woo, Wei Gao, Giovanni Russello (The University of Auckland)
**Objective:** Independent experimental verification of the **multi-agent role-decomposition effect on false alarms** via a static-weight triad ablation.

> **Citation note (re-verified 2026-11-09 against the arXiv abs page):** the v2 title is
> *"An Explainable and Adaptive Multi-Agent LLM System..."* and the author list has **five**
> names, including Meng Wai Woo and Wei Gao. Earlier internal documents recorded a different
> title and four authors; that was wrong. Provenance log:
> `docs/citation_provenance/M043_MultiPhishGuard.md`.

### Primary Literature Numbers (arXiv v2, Table 1):
| Model / System | Accuracy | Precision | Recall | F1 | FPR | FNR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Single Agent (Zero-shot) | 84.42 | 61.31 | 99.39 | 75.84 | 20.47 | 0.61 |
| Chain-of-Thought (CoT) | 86.60 | 64.93 | 99.08 | 78.45 | 17.47 | 0.92 |
| RoBERTa-base (Supervised) | 95.73 | 86.20 | 98.67 | 91.89 | 5.13 | 1.63 |
| MultiPhishGuard (Full) | 97.89 | 92.26 | 99.80 | 95.88 | 2.73 | 0.20 |

> All values are percentages. Section 4.4 confirms the static-weight variant uses
> 0.3 (text) + 0.4 (URL) + 0.3 (metadata). The paper's Table 5 FPR for that variant is **not**
> quoted here because the value has not been re-verified against the PDF page; the goal of this
> notebook is to test whether role decomposition lowers FPR relative to single-agent CoT.

### Scope, corpus and honest limitations
- **Agents:** the full system has **five** agents (text, URL, metadata, explanation simplifier,
  adversarial) with **PPO-learned dynamic weighting** (abstract + Section 3.1). This notebook
  replicates the **three *analysis* agents only**, combined with the paper's **static** weights
  (Section 4.4) instead of PPO. Do not describe the paper as "a 3-agent system".
- **Corpus:** a public phishing/spam email corpus with real sender fields
  (`puyang2025/seven-phishing-email-datasets`, sources include Enron, CEAS-08, Assassin,
  TREC-05/06/07). This is a **construct-validity deviation**: the original benchmark uses
  Nazario phishing emails, whereas the public corpus labels spam and phishing jointly. Report it.
- **Sample:** a frozen stratified slice of 200 emails (50 phishing / 150 legitimate) drawn from
  the corpus `test` split with a fixed seed, written to disk so every re-run scores identical rows.
- **Replication nature:** `gpt-4o` => Direct replication. Any other model => Conceptual /
  Cross-model replication, and must be labelled as such.
- **Ablation confound (Rule 10.2 of RESEARCH_RULES.md):** Arm A issues **1** LLM call per email,
  Arm B issues **3**. Any FPR gain is therefore confounded with token budget and call count. Both
  are logged per sample, and the claim must be restricted to an architectural observation unless a
  matched-budget control (3 calls of the same CoT agent) is also run.""",
    ),
    make_cell(
        "code",
        """# Cell 1: Environment, Provider Configuration & Model Guard
!pip install -q litellm datasets scikit-learn pandas numpy scipy

import hashlib
import json
import os
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sps
from sklearn.metrics import (
    accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
)

# --- AGENTS.md guard: Gemini models below 3.5 are forbidden. ---
FORBIDDEN_GEMINI = re.compile(r"gemini[-_](1\\.5|2\\.0|2\\.5)", re.IGNORECASE)

def assert_model_allowed(model_name: str) -> None:
    if FORBIDDEN_GEMINI.search(model_name):
        raise ValueError(
            f"Model '{model_name}' violates the AGENTS.md Gemini floor "
            "(< gemini-3.5-flash is forbidden). Pick gemini-3.5-flash or higher."
        )

LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o")
assert_model_allowed(LLM_MODEL)

# gpt-4o => direct replication; anything else => cross-model replication.
IS_DIRECT_REPLICATION = LLM_MODEL.strip().lower() == "gpt-4o"

# REPRO_SIMULATE=1 runs a deterministic rule-based stand-in used ONLY to smoke-test the
# pipeline offline. Its outputs are explicitly labelled non-scientific and must never be
# reported as a result.
SIMULATE = os.environ.get("REPRO_SIMULATE", "0") == "1"

API_KEY_PRESENT = any(
    os.environ.get(k)
    for k in ("OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "OPENROUTER_API_KEY")
)

TELEMETRY_PATH = Path("Repro_Paper3_telemetry.jsonl")
BENCHMARK_PATH = Path("Repro_Paper3_Benchmark_N200_Seed42.csv")

print(f"Active LLM: {LLM_MODEL}")
print(f"Replication mode: {'DIRECT 1:1 REPLICATION' if IS_DIRECT_REPLICATION else 'CONCEPTUAL / CROSS-MODEL'}")
print(f"API key present: {API_KEY_PRESENT} | Simulation mode: {SIMULATE}")
if not API_KEY_PRESENT and not SIMULATE:
    print("\\nNo API key found. Set one of OPENAI_API_KEY / GEMINI_API_KEY / "
          "OPENROUTER_API_KEY, or export REPRO_SIMULATE=1 for a pipeline smoke test only.")""",
    ),
    make_cell(
        "code",
        """# Cell 2: Real Benchmark Corpus -> Frozen Stratified Slice (N=200)
from datasets import load_dataset

CORPUS_REPO = "puyang2025/seven-phishing-email-datasets"
CORPUS_SPLIT = "test"
N_PHISHING, N_LEGIT = 50, 150          # 1:3 ratio, as in the paper's corpus description
SLICE_SEED = 42

URL_RE = re.compile(r"(?:https?://|www\\.)[^\\s<>\\"')]+", re.IGNORECASE)

def _clean(text, limit=6000):
    text = re.sub(r"[ \\t]+", " ", str(text))
    text = re.sub(r"\\n{3,}", "\\n\\n", text).strip()
    return text[:limit]

def _first_url(text):
    m = URL_RE.search(str(text))
    return m.group(0).rstrip(".,;)") if m else ""

def build_frozen_slice(force_rebuild=False) -> pd.DataFrame:
    if BENCHMARK_PATH.exists() and not force_rebuild:
        frozen = pd.read_csv(BENCHMARK_PATH)
        digest = hashlib.sha256(
            BENCHMARK_PATH.read_bytes()
        ).hexdigest()[:16]
        print(f"Reusing frozen benchmark {BENCHMARK_PATH} "
              f"(N={len(frozen)}, sha256:{digest}) - every re-run scores identical rows.")
        return frozen

    ds = load_dataset(CORPUS_REPO, split=CORPUS_SPLIT)
    frame = ds.to_pandas()
    frame["text"] = frame["text"].map(_clean)
    frame["sender"] = frame.get("sender", pd.Series([""] * len(frame))).fillna("")
    frame["url"] = frame["text"].map(_first_url)

    # Deduplicate on normalised text: leakage between the two arms would be fatal.
    frame["_norm"] = frame["text"].str.lower().str.replace(r"\\W+", " ", regex=True).str.strip()
    frame = frame[frame["_norm"].str.len() > 40]
    frame = frame.drop_duplicates(subset=["_norm"]).reset_index(drop=True)

    phish = frame[frame["label"] == 1]
    legit = frame[frame["label"] == 0]
    if len(phish) < N_PHISHING or len(legit) < N_LEGIT:
        raise RuntimeError(f"Insufficient pool: phish={len(phish)}, legit={len(legit)}")

    sampled = pd.concat([
        phish.sample(n=N_PHISHING, random_state=SLICE_SEED),
        legit.sample(n=N_LEGIT, random_state=SLICE_SEED),
    ]).sample(frac=1.0, random_state=SLICE_SEED).reset_index(drop=True)

    sampled = sampled.reset_index().rename(columns={"index": "sample_id"})
    sampled["metadata_available"] = (sampled["sender"].astype(str).str.len() > 0).astype(int)
    keep = ["sample_id", "text", "url", "sender", "label", "metadata_available", "dataset_name"]
    out = sampled[[c for c in keep if c in sampled.columns]]
    out.to_csv(BENCHMARK_PATH, index=False)
    print(f"Frozen slice written: {BENCHMARK_PATH} (N={len(out)})")
    return out

eval_df = build_frozen_slice()

print(f"\\nN={len(eval_df)} | phishing={int(eval_df['label'].sum())} | "
      f"legitimate={int((1 - eval_df['label']).sum())}")
print(f"URL extracted: {int((eval_df['url'].str.len() > 0).sum())}/{len(eval_df)}")
print(f"Sender present: {int(eval_df['metadata_available'].sum())}/{len(eval_df)}")
if "dataset_name" in eval_df.columns:
    print("Source corpora:", eval_df["dataset_name"].value_counts().to_dict())
dup = eval_df["text"].duplicated().sum()
assert dup == 0, f"{dup} duplicated texts in the frozen slice"
print("No duplicated texts in the slice.")""",
    ),
    make_cell(
        "code",
        """# Cell 3: Prompt Engineering - Arm A (Single CoT) vs Arm B (3 Voting Agents)
# Missing metadata is handled explicitly: the metadata agent is told to return a neutral
# 0.5 when no sender/header is supplied, so the 0.3 weight stays a documented prior
# rather than a silently fabricated signal.

COT_SYSTEM_PROMPT = \"\"\"You are an expert Cyber Security Analyst evaluating incoming emails for phishing.
Analyze the email content, URL, and sender metadata step-by-step.
Return ONLY valid JSON in this exact structure:
{
  "chain_of_thought": "detailed reasoning over text, URL and sender",
  "suspicion_score": <float 0.0-1.0>,
  "is_phishing": <true|false>
}\"\"\"

TEXT_AGENT_PROMPT = \"\"\"You are the Text Specialist Agent of MultiPhishGuard.
Analyze linguistic features: psychological pressure, urgency, authority pretexting, coercion,
financial lures, requests for credentials.
Return ONLY valid JSON:
{"text_risk_score": <float 0.0-1.0>, "rationale": "concise text analysis"}\"\"\"

URL_AGENT_PROMPT = \"\"\"You are the URL Specialist Agent of MultiPhishGuard.
Analyze embedded hyperlinks: domain legitimacy, typosquatting, suspicious subdomains,
IP-literal hosts, risky TLDs, URL shorteners.
If no URL is present, return 0.2 (absence of a link is weak evidence of legitimacy).
Return ONLY valid JSON:
{"url_risk_score": <float 0.0-1.0>, "rationale": "concise URL analysis"}\"\"\"

METADATA_AGENT_PROMPT = \"\"\"You are the Metadata Specialist Agent of MultiPhishGuard.
Analyze the sender display name vs. the actual address, domain consistency, free-mail use for
corporate claims, and spoofing indicators.
If the sender field is UNKNOWN, return exactly 0.5 with rationale "no metadata supplied".
Return ONLY valid JSON:
{"metadata_risk_score": <float 0.0-1.0>, "rationale": "concise metadata analysis"}\"\"\"

WEIGHTS = {"text": 0.3, "url": 0.4, "metadata": 0.3}
DECISION_THRESHOLD = 0.5

def _field(value, default):
    # pandas turns empty CSV cells into NaN, and NaN is truthy - so `value or default`
    # would leak the string "nan" to the agents. Normalise explicitly.
    if value is None or pd.isna(value):
        return default
    text = str(value).strip()
    return text if text and text.lower() != "nan" else default

def build_email_block(row) -> str:
    sender = _field(row.get("sender"), "UNKNOWN")
    url = _field(row.get("url"), "NONE")
    return (f"Sender: {sender}\\n"
            f"Embedded URL: {url}\\n"
            f"Subject/Body:\\n{row['text']}")

print("Prompt contracts established for Arm A (CoT) and Arm B (static-weight triad).")
print(f"Triage weights: {WEIGHTS} | decision threshold: {DECISION_THRESHOLD}")""",
    ),
    make_cell(
        "code",
        """# Cell 4: Execution Harness - litellm, retries, JSON repair, exact call accounting
import litellm
from litellm import completion

litellm.drop_params = True
MAX_RETRIES = 4
RETRY_BASE_SECONDS = 2.0
TEMPERATURE = 0.0
MAX_TOKENS = 700

def _extract_json(raw: str) -> dict:
    if not raw:
        raise ValueError("empty LLM response")
    text = raw.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    depth, start = 0, None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                return json.loads(text[start:i + 1])
    raise ValueError(f"no JSON object found in response: {raw[:200]!r}")

USAGE = {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0, "cost_usd": 0.0,
         "cost_unavailable": 0}

def _accumulate_usage(resp) -> None:
    usage = getattr(resp, "usage", None)
    if usage is not None:
        USAGE["prompt_tokens"] += int(getattr(usage, "prompt_tokens", 0) or 0)
        USAGE["completion_tokens"] += int(getattr(usage, "completion_tokens", 0) or 0)
    try:
        from litellm import completion_cost
        USAGE["cost_usd"] += float(completion_cost(completion_response=resp) or 0.0)
    except Exception:  # noqa: BLE001 - price table may not know the model
        USAGE["cost_unavailable"] += 1

def _simulated_response(system_prompt: str, content: str) -> dict:
    # Offline stand-in for pipeline smoke tests. NOT a scientific result.
    low = content.lower()
    phish_cues = any(w in low for w in (
        "verify", "urgent", "suspended", "refund", "unauthorized", "winner",
        "click here", "act now", "confidential", "investment", "million",
    ))
    bad_domain = bool(re.search(r"(\\b\\d{1,3}(\\.\\d{1,3}){3}\\b|\\.(ru|top|xyz|biz|info)/|"
                                r"-secure|account-verify|login-)", low))
    if "Text Specialist" in system_prompt:
        return {"text_risk_score": 0.85 if phish_cues else 0.15, "rationale": "simulated"}
    if "URL Specialist" in system_prompt:
        return {"url_risk_score": 0.95 if bad_domain else 0.15, "rationale": "simulated"}
    if "Metadata Specialist" in system_prompt:
        if "Sender: UNKNOWN" in content:
            return {"metadata_risk_score": 0.5, "rationale": "no metadata supplied"}
        spoofy = bool(re.search(r"@(?!.*\\.(edu|gov)$)[a-z0-9.-]+\\.(com|net|org)$", low))
        return {"metadata_risk_score": 0.75 if spoofy else 0.25, "rationale": "simulated"}
    score = 0.75 if (phish_cues or bad_domain) else 0.2
    return {"chain_of_thought": "simulated", "suspicion_score": score,
            "is_phishing": score >= 0.5}

def call_llm(system_prompt: str, user_content: str) -> tuple[dict, float, int]:
    \"\"\"Returns (parsed_json, latency_ms, n_api_calls). Raises on unrecoverable failure.\"\"\"
    if SIMULATE:
        t0 = time.perf_counter()
        payload = _simulated_response(system_prompt, user_content)
        USAGE["calls"] += 1
        return payload, (time.perf_counter() - t0) * 1000.0, 1

    if not API_KEY_PRESENT:
        raise RuntimeError(
            "No LLM API key configured. Set OPENAI_API_KEY / GEMINI_API_KEY / "
            "OPENROUTER_API_KEY, or set REPRO_SIMULATE=1 for a smoke test only."
        )

    last_error = None
    for attempt in range(MAX_RETRIES):
        calls_this_attempt = attempt + 1
        t0 = time.perf_counter()
        try:
            resp = completion(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                response_format={"type": "json_object"},
            )
            USAGE["calls"] += 1
            _accumulate_usage(resp)
            latency_ms = (time.perf_counter() - t0) * 1000.0
            payload = _extract_json(resp.choices[0].message.content)
            return payload, latency_ms, calls_this_attempt
        except Exception as exc:  # noqa: BLE001 - rate limits, timeouts, JSON errors
            last_error = exc
            USAGE["calls"] += 1
            if attempt == MAX_RETRIES - 1:
                break
            time.sleep(RETRY_BASE_SECONDS * (2 ** attempt) + np.random.uniform(0, 0.5))
    raise RuntimeError(f"LLM call failed after {MAX_RETRIES} attempts: {last_error}")

print("Harness ready: litellm routing, exponential backoff, JSON repair, per-call accounting.")""",
    ),
    make_cell(
        "code",
        """# Cell 5: Run the Comparative Ablation with Per-Sample Telemetry
# Telemetry is appended and fsynced after every sample so a crash or a rate-limit wall
# never loses completed work.
import os as _os

def _append_telemetry(record: dict) -> None:
    with open(TELEMETRY_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\\n")
        fh.flush()
        _os.fsync(fh.fileno())

if TELEMETRY_PATH.exists():
    TELEMETRY_PATH.unlink()
print(f"Telemetry -> {TELEMETRY_PATH}")

y_true = eval_df["label"].values.astype(int)
arm_a_preds, arm_b_preds = [], []
failures = 0
run_start = time.perf_counter()

for idx, row in eval_df.iterrows():
    sample_id = int(row.get("sample_id", idx))
    mail_block = build_email_block(row)
    record = {"sample_id": sample_id, "gold_label": int(row["label"]),
              "model": LLM_MODEL, "simulate": SIMULATE}
    sample_start = time.perf_counter()
    calls_before = USAGE["calls"]

    try:
        cot = call_llm(COT_SYSTEM_PROMPT, mail_block)
        cot_payload, cot_latency, _ = cot
        score_a = float(cot_payload.get("suspicion_score", 0.5))
        pred_a = int(bool(cot_payload.get("is_phishing", score_a >= DECISION_THRESHOLD)))

        text_payload, text_latency, _ = call_llm(TEXT_AGENT_PROMPT, mail_block)
        url_payload, url_latency, _ = call_llm(URL_AGENT_PROMPT, mail_block)
        meta_payload, meta_latency, _ = call_llm(METADATA_AGENT_PROMPT, mail_block)

        s_text = float(text_payload.get("text_risk_score", 0.5))
        s_url = float(url_payload.get("url_risk_score", 0.5))
        s_meta = float(meta_payload.get("metadata_risk_score", 0.5))
        triad = (WEIGHTS["text"] * s_text + WEIGHTS["url"] * s_url
                 + WEIGHTS["metadata"] * s_meta)
        pred_b = int(triad >= DECISION_THRESHOLD)

        record.update({
            "arm_a_pred": pred_a, "arm_a_score": round(score_a, 4),
            "text_score": round(s_text, 4), "url_score": round(s_url, 4),
            "meta_score": round(s_meta, 4), "triad_score": round(triad, 4),
            "arm_b_pred": pred_b,
            "metadata_available": int(row.get("metadata_available", 0)),
            "url_present": int(bool(str(row.get("url", "")).strip())),
            "latency_ms": round((time.perf_counter() - sample_start) * 1000.0, 1),
            "agent_latencies_ms": [round(cot_latency, 1), round(text_latency, 1),
                                   round(url_latency, 1), round(meta_latency, 1)],
            "error": None,
        })
        arm_a_preds.append(pred_a)
        arm_b_preds.append(pred_b)
    except Exception as exc:  # noqa: BLE001
        failures += 1
        record.update({"arm_a_pred": None, "arm_b_pred": None, "error": str(exc)[:300]})
        arm_a_preds.append(None)
        arm_b_preds.append(None)

    record["api_calls"] = int(USAGE["calls"] - calls_before)
    record["cum_prompt_tokens"] = USAGE["prompt_tokens"]
    record["cum_completion_tokens"] = USAGE["completion_tokens"]
    record["cum_cost_usd"] = round(USAGE["cost_usd"], 6)
    _append_telemetry(record)

    if (idx + 1) % 10 == 0 or idx == 0:
        print(f"[{idx + 1}/{len(eval_df)}] id={sample_id} gold={record['gold_label']} "
              f"A={record.get('arm_a_pred')} B={record.get('arm_b_pred')} "
              f"triad={record.get('triad_score')} calls={record['api_calls']} "
              f"lat={record['latency_ms']}ms failures={failures}")

wall_seconds = time.perf_counter() - run_start
print(f"\\nDone in {wall_seconds / 60:.1f} min | total API calls={USAGE['calls']} | "
      f"failures={failures}")
print(f"Tokens: prompt={USAGE['prompt_tokens']:,} completion={USAGE['completion_tokens']:,}")
if USAGE["cost_unavailable"]:
    print(f"[warn] {USAGE['cost_unavailable']} calls had no price entry; cost reported as a "
          f"lower bound / N/A.")
else:
    print(f"Estimated cost: ${USAGE['cost_usd']:.4f}")""",
    ),
    make_cell(
        "code",
        """# Cell 6: Metrics, Exact McNemar, BH Correction and Clopper-Pearson Bounds
from scipy.stats import binomtest

def clopper_pearson(k, n, alpha=0.05):
    if n == 0:
        return (float("nan"), float("nan"))
    lo = 0.0 if k == 0 else sps.beta.ppf(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else sps.beta.ppf(1 - alpha / 2, k + 1, n - k)
    return round(float(lo) * 100, 2), round(float(hi) * 100, 2)

def performance(y_t, y_p, name):
    tn, fp, fn, tp = confusion_matrix(y_t, y_p, labels=[0, 1]).ravel()
    fpr_ci = clopper_pearson(fp, fp + tn)
    rec_ci = clopper_pearson(tp, tp + fn)
    return {
        "Approach": name,
        "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp),
        "N": int(tn + fp + fn + tp),
        "Accuracy (%)": round(accuracy_score(y_t, y_p) * 100, 2),
        "Precision (%)": round(precision_score(y_t, y_p, zero_division=0) * 100, 2),
        "Recall (%)": round(recall_score(y_t, y_p) * 100, 2),
        "F1 (%)": round(f1_score(y_t, y_p) * 100, 2),
        # Rule 10.4: FPR (per legitimate email) and FDR (per raised alarm) are distinct.
        "FPR (%)": round(fp / max(fp + tn, 1) * 100, 2),
        "FPR 95% CI": f"{fpr_ci[0]}-{fpr_ci[1]}",
        "FDR (%)": round(fp / max(fp + tp, 1) * 100, 2),
        "Recall 95% CI": f"{rec_ci[0]}-{rec_ci[1]}",
    }

valid = [i for i, (a, b) in enumerate(zip(arm_a_preds, arm_b_preds))
         if a is not None and b is not None]
if len(valid) < len(eval_df):
    print(f"[warn] {len(eval_df) - len(valid)} samples failed and are excluded; "
          f"the denominators below reflect the surviving N={len(valid)} only.")

if not valid:
    raise RuntimeError("No valid predictions - inspect the telemetry JSONL for errors.")

y_v = y_true[valid]
a_v = np.array([arm_a_preds[i] for i in valid])
b_v = np.array([arm_b_preds[i] for i in valid])

rows = [
    performance(y_v, a_v, f"Arm A: Single Agent CoT ({LLM_MODEL})"),
    performance(y_v, b_v, f"Arm B: Static-Weight Triad 0.3/0.4/0.3 ({LLM_MODEL})"),
]
results_df = pd.DataFrame(rows)
display(results_df)
results_df.to_csv("Repro_Paper3_MultiPhishGuard_Ablation.csv", index=False)
if SIMULATE:
    print("\\n*** SIMULATION MODE - these numbers are a pipeline smoke test and must NOT ***")
    print("*** be reported as experimental results. Re-run with a real API key.       ***")

# --- Exact one-sided McNemar: H1 = Arm B makes fewer errors than Arm A ---
disagree_a_right = int(np.sum((a_v == y_v) & (b_v != y_v)))
disagree_b_right = int(np.sum((a_v != y_v) & (b_v == y_v)))
n_discordant = disagree_a_right + disagree_b_right
if n_discordant == 0:
    p_exact = 1.0
    print("\\nNo discordant pairs: the two arms agreed on every surviving sample "
          "(p = 1.0, McNemar is uninformative).")
else:
    p_exact = float(binomtest(disagree_b_right, n_discordant, 0.5, alternative="greater").pvalue)
    chi2 = (abs(disagree_a_right - disagree_b_right) - 1.0) ** 2 / n_discordant
    p_chi2 = float(1.0 - sps.chi2.cdf(max(chi2, 0.0), df=1))
    print(f"\\nDiscordant pairs: A right/B wrong={disagree_a_right}, "
          f"A wrong/B right={disagree_b_right}")
    print(f"Exact one-sided McNemar p = {p_exact:.4f}")
    print(f"Edwards-corrected chi-square cross-check: chi2={chi2:.3f}, "
          f"two-sided p={p_chi2:.4f}")

print(f"FPR delta (B - A) = {rows[1]['FPR (%)'] - rows[0]['FPR (%)']:+.2f} pp "
      f"| Recall delta = {rows[1]['Recall (%)'] - rows[0]['Recall (%)']:+.2f} pp")
print("Report the call-count asymmetry (Arm A = 1 call, Arm B = 3 calls per email) "
      "alongside these numbers; see Rule 10.2.")""",
    ),
]
save_notebook(
    OUT_DIR
    / "Repro_Paper3_SecureNet_MultiPhishGuard_and_SLM_Distillation.ipynb",
    nb3_cells,
)

print("\n>>> All 3 Reproduction Notebooks Successfully Rebuilt <<<")
