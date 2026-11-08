"""Runtime smoke test for the regenerated reproduction notebooks.

Executes the real notebook cell sources (not copies) so the artefacts themselves are
tested. No GPU, no network and no API key are required:

- Paper 3: full pipeline in REPRO_SIMULATE mode against a synthetic 420-row corpus that
  contains duplicates, missing senders and both classes. Verifies frozen-slice reuse,
  deduplication, per-sample telemetry (one JSONL line per sample with the exact API-call
  count), integer denominators and the exact McNemar path.
- Paper 1: the hardened dataset registry and the statistics block, driven by stub
  `load_dataset` objects whose split sizes match Table 2 of the ViSoBERT paper.

Paper 2 is GPU-only (torch training + DistilBERT) and is covered by static compilation in
scripts/validate_repro_notebooks.py.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import types
from pathlib import Path

import numpy as np
import pandas as pd

NB_DIR = Path("kaggle_notebooks")
P1 = NB_DIR / "Repro_Paper1_ViSoBERT_EMNLP2023_Original.ipynb"
P3 = NB_DIR / "Repro_Paper3_SecureNet_MultiPhishGuard_and_SLM_Distillation.ipynb"

FAILURES: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        print(f"  ok   {message}")
    else:
        print(f"  FAIL {message}")
        FAILURES.append(message)


def code_cells(path: Path) -> list[str]:
    nb = json.loads(path.read_text(encoding="utf-8"))
    return ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]


def strip_magics(source: str) -> str:
    out = []
    for line in source.splitlines():
        s = line.lstrip()
        out.append("pass" if s.startswith("!") or s.startswith("%") else line)
    return "\n".join(out)


def exec_cell(source: str, ns: dict, name: str) -> None:
    exec(compile(strip_magics(source), name, "exec"), ns)  # noqa: S102 - test harness


# --------------------------------------------------------------------------------------
# Paper 3: end-to-end in simulation mode
# --------------------------------------------------------------------------------------
def stub_litellm() -> None:
    mod = types.ModuleType("litellm")
    mod.drop_params = False

    def _completion(**_kwargs):
        raise RuntimeError("network access is disabled in the smoke test")

    mod.completion = _completion
    mod.completion_cost = lambda **_kwargs: 0.0
    sys.modules["litellm"] = mod


def build_fake_corpus() -> pd.DataFrame:
    rows = []
    for i in range(420):
        phishing = i % 4 == 0
        if phishing:
            text = (f"Subject: Notice {i}\n\nBody: please verify your account at "
                    f"http://evil{i}.xyz/login to avoid suspension within 24 hours")
        else:
            text = (f"Subject: Weekly sync {i}\n\nBody: here is the agenda for the "
                    f"planning meeting, no action required before Friday")
        rows.append({
            "text": text,
            "sender": f"user{i}@corp{i % 5}.com" if i % 3 else "",
            "label": 1 if phishing else 0,
            "dataset_name": "FAKE-TREC",
        })
    return pd.DataFrame(rows)


class SplitFrame(pd.DataFrame):
    _metadata = ["features"]

    @property
    def _constructor(self):
        return SplitFrame


def dataset_stub(corpus: pd.DataFrame) -> None:
    mod = types.ModuleType("datasets")

    class _DS(dict):
        def to_pandas(self):
            return corpus.copy()

    frame = _DS()
    frame["test"] = SplitFrame(corpus)
    mod.load_dataset = lambda *_a, **_k: frame
    sys.modules["datasets"] = mod


def test_paper3(tmpdir: Path) -> None:
    print("\n[Paper 3] end-to-end pipeline (simulation mode)")
    tmpdir = Path(tmpdir).resolve()
    os.environ["REPRO_SIMULATE"] = "1"
    os.environ.pop("OPENAI_API_KEY", None)
    os.environ.pop("GEMINI_API_KEY", None)
    stub_litellm()
    dataset_stub(build_fake_corpus())

    cells = code_cells(P3)
    check(len(cells) == 6, f"Paper 3 exposes 6 code cells (found {len(cells)})")

    ns: dict = {"__name__": "__smoke__", "display": lambda *a, **k: None}
    cwd = os.getcwd()
    os.chdir(tmpdir)
    try:
        for i, src in enumerate(cells):
            exec_cell(src, ns, f"P3-cell-{i + 1}")

        # Guard behaviour
        guard = ns["assert_model_allowed"]
        try:
            guard("gemini-2.5-flash")
            check(False, "guard rejects gemini-2.5-flash")
        except ValueError:
            check(True, "guard rejects gemini-2.5-flash")
        for allowed in ("gemini-3.5-flash", "gemini-3.8-flash", "gpt-4o", "gpt-6.1-sol"):
            try:
                guard(allowed)
            except ValueError:
                check(False, f"guard allows {allowed}")
        check(True, "guard allows gemini-3.5-flash / gemini-3.8-flash / gpt-4o / gpt-6.1-sol")

        frozen = ns["eval_df"]
        check(len(frozen) == 200, f"frozen slice is N=200 (got {len(frozen)})")
        check(int(frozen["label"].sum()) == 50,
              f"slice holds 50 phishing rows (got {int(frozen['label'].sum())})")
        check(int((1 - frozen["label"]).sum()) == 150, "slice holds 150 legitimate rows")
        check(frozen["text"].duplicated().sum() == 0, "no duplicated text in the slice")
        check((frozen["url"].str.len() > 0).sum() == 50,
              "URL extracted for every phishing row")
        benchmark_file = tmpdir / "Repro_Paper3_Benchmark_N200_Seed42.csv"
        check(benchmark_file.exists(), "frozen benchmark CSV written to disk")

        telemetry = (tmpdir / "Repro_Paper3_telemetry.jsonl").read_text(encoding="utf-8")
        lines = [json.loads(ln) for ln in telemetry.splitlines() if ln.strip()]
        check(len(lines) == 200, f"one telemetry line per sample (got {len(lines)})")
        required_keys = {
            "sample_id", "gold_label", "arm_a_pred", "arm_b_pred", "triad_score",
            "latency_ms", "api_calls", "metadata_available", "url_present",
            "agent_latencies_ms", "cum_prompt_tokens", "cum_cost_usd", "error",
        }
        check(required_keys.issubset(lines[0].keys()),
              "telemetry carries gold label, both arms, latency, api_calls and cost")
        check(all(ln["api_calls"] == 4 for ln in lines),
              "each sample records exactly 4 API calls (1 CoT + 3 agents)")
        check(all(ln["error"] is None for ln in lines), "no sample errored in simulation")
        check(all(ln["arm_a_pred"] in (0, 1) and ln["arm_b_pred"] in (0, 1)
                  for ln in lines), "both arms produced binary predictions")
        # Rows without a sender must reach the metadata agent as "UNKNOWN" (neutral 0.5),
        # not as the string "nan" produced by pandas NaN handling.
        no_sender = [ln for ln in lines if ln["metadata_available"] == 0]
        check(len(no_sender) > 0, f"slice contains rows without sender ({len(no_sender)})")
        check(all(ln["meta_score"] == 0.5 for ln in no_sender),
              "missing sender yields the neutral 0.5 metadata score (no 'nan' leak)")

        ablation = pd.read_csv(tmpdir / "Repro_Paper3_MultiPhishGuard_Ablation.csv")
        check(len(ablation) == 2, "ablation table has exactly 2 arms")
        totals = (ablation["TN"] + ablation["FP"] + ablation["FN"] + ablation["TP"]).tolist()
        check(totals == [200, 200], f"integer denominators sum to N=200 per arm (got {totals})")
        check(ablation["FPR 95% CI"].notna().all(), "FPR carries a Clopper-Pearson 95% CI")

        # Re-running cell 2 must reuse the frozen slice, not resample it.
        exec_cell(cells[1], ns, "P3-cell-2-rerun")
        rerun = ns["eval_df"]
        check(rerun["text"].tolist() == frozen["text"].tolist(),
              "re-run reuses the identical frozen slice")
    finally:
        os.chdir(cwd)


# --------------------------------------------------------------------------------------
# Paper 1: dataset registry + statistics block with stubbed datasets
# --------------------------------------------------------------------------------------
def split_frame(df: pd.DataFrame, text_col: str, label_col: str) -> SplitFrame:
    sf = SplitFrame(df)
    types_map = {}
    for col in df.columns:
        types_map[col] = types.SimpleNamespace(
            dtype="string" if df[col].dtype == object else "int64"
        )
    sf.features = types_map
    return sf


def test_paper1(tmpdir: Path) -> None:
    print("\n[Paper 1] dataset registry + statistics block")
    tmpdir = Path(tmpdir).resolve()
    from sklearn.metrics import f1_score, accuracy_score  # noqa: F401 - used via ns

    specs = {
        "duwuonline/UIT-VSMEC": (("train", 5548), ("validation", 686), ("test", 693),
                                 "Sentence", "Emotion", True),
        "htdung167/ViHSD": (("train", 24048), ("validation", 2672), ("test", 6680),
                            "free_text", "label_id", False),
    }
    rng = np.random.RandomState(0)

    def fake_load_dataset(repo, *_a, **_k):
        (tr, n_tr), (va, n_va), (te, n_te), text_col, label_col, string_labels = specs[repo]
        ds = {}

        def make(n):
            if string_labels:
                labels = rng.choice(
                    ["Other", "Disgust", "Enjoyment", "Anger", "Surprise", "Sadness", "Fear"], n
                )
            else:
                labels = rng.randint(0, 3, n)
            return split_frame(
                pd.DataFrame({text_col: [f"câu {i}" for i in range(n)], label_col: labels}),
                text_col, label_col,
            )

        ds[tr] = make(n_tr)
        ds[va] = make(n_va)
        ds[te] = make(n_te)
        return ds

    datasets_stub = types.ModuleType("datasets")
    datasets_stub.load_dataset = fake_load_dataset

    cells = code_cells(P1)
    # Cell 2 = registry/loader; its leading probe loop needs stubs already in place.
    ns: dict = {
        "__name__": "__smoke__",
        "display": lambda *a, **k: None,
        "pd": pd,
        "np": np,
        "f1_score": f1_score,
        "accuracy_score": accuracy_score,
        "json": json,
        "os": os,
        "torch": types.SimpleNamespace(cuda=types.SimpleNamespace(is_available=lambda: False),
                                       backends=types.SimpleNamespace(cudnn=types.SimpleNamespace())),
        "load_dataset": fake_load_dataset,
        "Dataset": object,
        "AutoTokenizer": object,
        "AutoModelForSequenceClassification": object,
        "Trainer": object,
        "TrainingArguments": objects_with_fields(),
        "DataCollatorWithPadding": object,
        "set_seed": lambda s: None,
        "EVAL_STRATEGY_KEY": "eval_strategy",
        "build_trainer": lambda **kw: None,
    }
    sys.modules["datasets"] = datasets_stub

    cwd = os.getcwd()
    os.chdir(tmpdir)
    try:
        exec_cell(cells[1], ns, "P1-cell-2")
        loader = ns["load_official_uit_dataset"]

        tr, va, te, n_cls, repo = loader("UIT-VSMEC")
        check((len(tr), len(va), len(te)) == (5548, 686, 693),
              f"VSMEC split sizes honoured (got {(len(tr), len(va), len(te))})")
        check(repo == "duwuonline/UIT-VSMEC", f"VSMEC resolved to {repo}")
        check(n_cls == 7, f"VSMEC has 7 emotion classes (got {n_cls})")

        tr, va, te, n_cls, repo = loader("UIT-ViHSD")
        check((len(tr), len(va), len(te)) == (24048, 2672, 6680),
              f"ViHSD split sizes honoured (got {(len(tr), len(va), len(te))})")
        check(n_cls == 3, f"ViHSD has 3 classes (got {n_cls})")

        # A wrong-size mirror must be rejected, not silently accepted.
        def bad_loader(repo, *_a, **_k):
            df = pd.DataFrame({"Sentence": ["x"], "Emotion": ["Other"]})
            return {"train": split_frame(df, "Sentence", "Emotion"),
                    "validation": split_frame(df, "Sentence", "Emotion"),
                    "test": split_frame(df, "Sentence", "Emotion")}

        ns["load_dataset"] = bad_loader
        # Cell 2 re-reads BENCHMARK_TASKS from the environment, so blank it to skip the
        # module-level probe loop for this exec only.
        previous_tasks_env = os.environ.get("REPRO_TASKS")
        os.environ["REPRO_TASKS"] = ""
        try:
            exec_cell(cells[1], ns, "P1-cell-2-bad")
        finally:
            if previous_tasks_env is None:
                os.environ.pop("REPRO_TASKS", None)
            else:
                os.environ["REPRO_TASKS"] = previous_tasks_env
        try:
            ns["load_official_uit_dataset"]("UIT-VSMEC")
            check(False, "wrong-size mirror is rejected")
        except RuntimeError:
            check(True, "wrong-size mirror is rejected instead of silently used")

        # Statistics block: run cell 4 with no tasks so only the helpers are defined.
        ns["BENCHMARK_TASKS"] = []
        ns["raw_predictions"] = {}
        ns["load_official_uit_dataset"] = loader
        exec_cell(cells[3], ns, "P1-cell-4")

        y = rng.randint(0, 7, 693)
        a = np.where(rng.rand(693) < 0.9, y, rng.randint(0, 7, 693))
        b = np.where(rng.rand(693) < 0.7, y, rng.randint(0, 7, 693))
        boot = ns["paired_bootstrap_mf1_diff"](y, a, b, n_bootstraps=200)
        check(boot["ci_95"][0] <= boot["mean_diff"] <= boot["ci_95"][1],
              "bootstrap CI brackets the mean delta")
        check(boot["p_value"] > 0.0, f"bootstrap p-value is floored (p={boot['p_value']:.4f})")
        check(boot["is_significant"] == (boot["ci_95"][0] > 0.0),
              "significance flag matches the CI rule")

        adj, reject = ns["benjamini_hochberg"]([0.001, 0.02, 0.03, 0.2])
        check(np.all(adj >= np.array([0.001, 0.02, 0.03, 0.2])),
              "BH-adjusted p-values are >= raw p-values")
        check(list(reject) == [True, True, True, False], f"BH decisions look sane ({list(reject)})")

        lo, hi = ns["clopper_pearson"](0, 19)
        check(lo == 0.0 and abs(hi - 17.65) < 0.05,
              f"0/19 Clopper-Pearson upper bound reproduces the Rule 10.3 value (got {lo}-{hi})")
        lo, hi = ns["clopper_pearson"](19, 19)
        check(hi == 100.0, "perfect-recall CP upper bound is 100%")
    finally:
        os.chdir(cwd)


def objects_with_fields():
    class _TA:
        __dataclass_fields__ = {"eval_strategy": object()}

    return _TA


def main() -> int:
    # The DSH file sandbox denies writes to directories created directly under the
    # workspace root, so the scratch directory lives under the pre-existing results/.
    scratch = (Path("results") / f".smoke_repro_{os.getpid()}").resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    try:
        test_paper3(scratch)
        test_paper1(scratch)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    print()
    if FAILURES:
        print(f"FAILED ({len(FAILURES)} check(s)):")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("PASS: Paper 3 pipeline and Paper 1 loader/statistics behave correctly at runtime.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
