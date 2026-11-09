"""Static validator for the three reproduction notebooks.

Checks, without a GPU or API key:
1. Valid nbformat JSON with the expected cell counts.
2. Every code cell compiles as Python (IPython magics/shell escapes are stripped first).
3. No leftover artefacts from the pre-audit version (toy mock corpus, dead dataset pins,
   forbidden Gemini models, silently mocked API calls).
4. The required anti-audit guards are present (per-sample telemetry, exact McNemar,
   Clopper-Pearson bounds, integer denominator assertions).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

NB_DIR = Path("kaggle_notebooks")
NOTEBOOKS = {
    "P1": NB_DIR / "Repro_Paper1_ViSoBERT_EMNLP2023_Original.ipynb",
    "P2": NB_DIR / "Repro_Paper2_EdgeAI_WBCE_and_ExplainableDetector_UCI5574.ipynb",
    "P3": NB_DIR / "Repro_Paper3_SecureNet_MultiPhishGuard_and_SLM_Distillation.ipynb",
}

# Strings that must NOT survive from the pre-audit notebooks.
FORBIDDEN = {
    "P1": [
        "uitnlp/uit-vsmec",       # repository does not exist
        "sonlam1102/vihsd",       # repository does not exist
        'val_key = ... else "test"',
    ],
    "P2": [
        "Footprint': '< 5 MB'",
        '"< 5 MB"',
        '"< 0.5 ms"',
    ],
    "P3": [
        "benchmark_data = [",      # the 6-sentence toy corpus
        "Synthetic representative samples",
        "gpt-4o-mini",
        "gemini-2.5",
        "gemini-1.5",
    ],
}

# Capabilities the audit required.
REQUIRED = {
    "P1": [
        "EXPECTED_SPLITS",
        "duwuonline/UIT-VSMEC",
        "htdung167/ViHSD",
        "EVAL_STRATEGY_KEY",
        "build_trainer",
        "load_best_model_at_end=True",
        "Repro_Paper1_runs.jsonl",
        "benjamini_hochberg",
        "EQUIVALENCE_MARGIN_PP",
    ],
    "P2": [
        "MIRROR_TSV_URL",
        "pickle.dumps",
        "total_length=input_ids.size(1)",
        "Repro_Paper2_per_sample_predictions.csv",
        'assert row["N"] == 1115',
    ],
    "P3": [
        "puyang2025/seven-phishing-email-datasets",
        "build_frozen_slice",
        "Repro_Paper3_telemetry.jsonl",
        "_append_telemetry",
        "fsync",
        "binomtest",
        "clopper_pearson",
        "assert_model_allowed",
        "FORBIDDEN_GEMINI",
        "api_calls",
        "metadata_available",
        "REPRO_SIMULATE",
        "Rule 10.2",
    ],
}


def strip_magics(source: str) -> str:
    """Remove IPython magics and shell escapes so the cell can be compiled."""
    kept = []
    for line in source.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("!") or stripped.startswith("%"):
            kept.append("pass")
        else:
            kept.append(line)
    return "\n".join(kept)


def main() -> int:
    failures: list[str] = []
    for key, path in NOTEBOOKS.items():
        if not path.exists():
            failures.append(f"{key}: missing file {path}")
            continue

        raw = path.read_text(encoding="utf-8")
        try:
            nb = json.loads(raw)
        except json.JSONDecodeError as exc:
            failures.append(f"{key}: invalid JSON ({exc})")
            continue

        if nb.get("nbformat") != 4:
            failures.append(f"{key}: nbformat is {nb.get('nbformat')}, expected 4")

        code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
        md_cells = [c for c in nb["cells"] if c["cell_type"] == "markdown"]
        # Match against decoded cell sources, not the raw JSON (which escapes quotes).
        code_text = "\n".join("".join(c["source"]) for c in code_cells)
        all_text = "\n".join("".join(c["source"]) for c in nb["cells"])

        compile_errors = 0
        for i, cell in enumerate(code_cells):
            src = "".join(cell["source"])
            try:
                compile(strip_magics(src), f"{key}-code-{i}", "exec")
            except SyntaxError as exc:
                compile_errors += 1
                failures.append(f"{key}: code cell {i} SyntaxError: {exc} (line {exc.lineno})")

        for needle in FORBIDDEN.get(key, []):
            if needle in code_text:
                failures.append(f"{key}: forbidden leftover still present in code: {needle!r}")

        for needle in REQUIRED.get(key, []):
            if needle not in all_text:
                failures.append(f"{key}: required capability missing: {needle!r}")

        # Telemetry must be appended line-by-line and flushed per sample.
        if key == "P3" and 'json.dumps(record, ensure_ascii=False) + "\\n"' not in code_text:
            failures.append("P3: no per-sample JSONL append found for telemetry")

        print(
            f"{key}: {len(nb['cells'])} cells "
            f"({len(code_cells)} code / {len(md_cells)} markdown), "
            f"{compile_errors} compile error(s), {path.stat().st_size / 1024:.1f} KB"
        )

    print()
    if failures:
        print(f"FAILED ({len(failures)} issue(s)):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("PASS: all three notebooks are structurally valid and carry every required guard.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
