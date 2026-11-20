# REPLICATION STATISTICAL CONCORDANCE REPORT (QUALITY GATE AUDIT)

**Project:** RBL_ScamShield — Multi-Tier Hybrid Framework for Vietnamese SMS Phishing Detection  
**Standard:** RESEARCH_RULES.md (Rule 10: Anti-Audit Rejection Invariants) & Quality Gate Protocol  
**Date:** 2026-11-20  
**Audit Status:** COMPLETED — 2 PASS (Paper 1 & Paper 3), 1 PARTIAL (Paper 2: Deployment Holds, Metric Gap / Split Mismatch)

---

## 1. Executive Summary & Verdict Decision Table

| Paper Identifier | Target Benchmark & Task | Sample Size ($N_{\text{test}}$) | Observed Primary Metric [95% CI] | Paper Target | Equivalence Check ($\vert\Delta\vert \le 2.0\text{ pp}$ or Target $\in$ CI) | Rank Order & Direction | Final Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Paper 1 (Nguyen et al., EMNLP 2023)** | UIT-VSMEC (Emotion, 7 classes) | $N = 693$ | Macro-F1: $64.60\%$ $[60.31\%, 68.52\%]$ | $65.88\%$ | **EQUIVALENT** ($\vert\Delta\vert = 1.28\text{ pp}$, Target $\in$ CI) | Holds (ViSoBERT #1 across all 3 seeds) | **PASS** |
| **Paper 1 (Nguyen et al., EMNLP 2023)** | UIT-ViHSD (Hate Speech, 3 classes) | $N = 6,680$ | Macro-F1: $69.04\%$ $[67.22\%, 70.93\%]$ | $68.77\%$ | **EQUIVALENT** ($\vert\Delta\vert = 0.27\text{ pp}$, Target $\in$ CI) | Holds (ViSoBERT #1 across all 3 seeds; $p_{\text{BH}} = 0.0005$) | **PASS** |
| **Paper 2 (Phap et al., 2026 / EdgeAI)** | UCI SMS (Spam Detection) | $N = 1,115$ ($966\text{H} / 149\text{S}$) | Spam Recall: $83.89\%$ $[76.99\%, 89.41\%]$ | $98.67\%$ | **NOT EQUIVALENT** ($\vert\Delta\vert = 14.78\text{ pp}$) | Direction holds (WBCE > BCE recall; $66\times$ footprint cut) | **PARTIAL** |
| **Paper 3 (Xue et al., 2025 / MultiPhishGuard)** | Council Benchmark Slice | $N = 200$ ($150\text{L} / 50\text{P}$) | Arm B FPR: $0.67\%$ $[0.02\%, 3.66\%]$ | $2.73\%$ | **EQUIVALENT** (Target $2.73\% \in$ CI) | Holds (Triad FPR $0.67\%$ vs Single CoT $17.33\%$) | **PASS** |

---

## 2. Step 1: Denominator Match & Integrity Audit

Rule 10.1 Invariant: Every aggregate metric must strictly trace back to raw integer counts where $\text{TN} + \text{FP} + \text{FN} + \text{TP} = N_{\text{test}}$.

### 2.1. Audit Breakdown by Deliverable

1. **UIT-ViHSD (Paper 1 — Newly Added & Verified):**
   - **Target Requirement:** $N_{\text{test}} = 6,680$.
   - **File Inspected:** `kaggle_notebooks/Repro_Paper1_artifacts (UIT-ViHSD)/Repro_Paper1_artifacts (UIT-ViHSD)/Repro_Paper1_ViSoBERT_EMNLP2023_Comparison.csv`
     - All 9 rows (Seeds 42, 43, 44 across ViSoBERT, XLM-RoBERTa, PhoBERT-base) strictly report `n_test = 6680`.
   - **Prediction Files Inspected:** All 9 per-sample files (`Repro_Paper1_preds_UIT-ViHSD_*.csv`) contain exactly 6,680 evaluation rows.
   - **Confusion Matrix Verification (Seed 42, $N=6,680$):**
     - **ViSoBERT:**
       - Class 0 (Clean, $N=5,548$): $5,260\text{ (Correct)} + 136\text{ (Pred 1)} + 152\text{ (Pred 2)} = 5,548$.
       - Class 1 (Offensive, $N=444$): $161\text{ (Pred 0)} + 206\text{ (Correct)} + 77\text{ (Pred 2)} = 444$.
       - Class 2 (Hate, $N=688$): $173\text{ (Pred 0)} + 75\text{ (Pred 1)} + 440\text{ (Correct)} = 688$.
       - Total Matrix Sum: $5,548 + 444 + 688 = 6,680$. Verified: $N = 6,680$. Accuracy $= (5260 + 206 + 440) / 6680 = 88.4132\%$.
     - **PhoBERT-base:**
       - Matrix: $[[5193, 165, 190], [186, 164, 94], [200, 77, 411]] \implies \sum = 6,680$. Accuracy $= 5768 / 6680 = 86.3473\%$.
     - **XLM-RoBERTa-base:**
       - Matrix: $[[5223, 126, 199], [181, 172, 91], [189, 87, 412]] \implies \sum = 6,680$. Accuracy $= 5807 / 6680 = 86.9311\%$.
   - **Verdict:** Denominator match 100% compliant.

2. **UIT-VSMEC (Paper 1):**
   - **Target Requirement:** $N_{\text{test}} = 693$.
   - **File Inspected:** `kaggle_notebooks/Repro_Paper1_artifacts/Repro_Paper1_artifacts(Hiếu)/Repro_Paper1_ViSoBERT_EMNLP2023_Comparison.csv`
     - All 9 rows across 3 architectures $\times$ 3 random seeds (Seeds 42, 43, 44) strictly report `n_test = 693`.
   - **Prediction Files Inspected:** All 9 per-sample files (`Repro_Paper1_preds_UIT-VSMEC_*.csv`) contain exactly 693 evaluation rows (7 emotion classes: Anger 37, Disgust 8, Enjoyment 215, Fear 33, Other 274, Sadness 87, Surprise 39 $\implies \sum = 693$).
   - **Verdict:** Denominator match 100% compliant.

3. **UCI SMS Benchmark (Paper 2):**
   - **Target Requirement:** $N_{\text{test}} = 1,115$ ($965\text{ ham} / 150\text{ spam}$).
   - **File Inspected:** `kaggle_notebooks/Repro_Paper2_EdgeAI_WBCE_and_ExplainableDetector_Deliverables/Repro_Paper2_EdgeAI_WBCE_and_ExplainableDetector_UCI5574/Repro_Paper2_WBCE_Ablation.csv`
     - **Line 2 (BiGRU + Standard BCE):** $\text{TN}=964, \text{FP}=2, \text{FN}=25, \text{TP}=124 \implies \sum = 1,115$. Verified: $N = 1,115$.
     - **Line 3 (BiGRU + WBCE):** $\text{TN}=961, \text{FP}=5, \text{FN}=24, \text{TP}=125 \implies \sum = 1,115$. Verified: $N = 1,115$.
   - **DISCREPANCY FLAGGED (Class Split Mismatch):**
     - Observed class totals in Line 2 & Line 3:
       - Negative (Ham): $\text{TN} + \text{FP} = 964 + 2 = 966$ (or $961 + 5 = 966$).
       - Positive (Spam): $\text{FN} + \text{TP} = 25 + 124 = 149$ (or $24 + 125 = 149$).
     - Required by protocol: $965\text{ ham} / 150\text{ spam}$.
     - Root Cause: `sklearn.model_selection.train_test_split(..., test_size=0.20, stratify=y)` on $N_{\text{total}} = 5,574$ rows ($4,827$ ham, $747$ spam). Rounding of $4,827 \times 0.20 = 965.4 \to 966$ and $747 \times 0.20 = 149.4 \to 149$ produces a 1-sample shift ($+1$ ham, $-1$ spam).
     - Action: In accordance with quality gate rules (*"không tự sửa, chỉ ra lỗi sai thuộc file nào, dòng nào"*), the file has not been altered; this discrepancy is formally recorded.
   - **File Inspected:** `Repro_Paper2_per_sample_predictions.csv`: Contains exactly 1,115 sample rows matching the ablation counts.

4. **Council Slice (Paper 3):**
   - **Target Requirement:** $N_{\text{test}} = 200$ ($150\text{ legit} / 50\text{ phishing}$).
   - **File Inspected:** `kaggle_notebooks/Repro_Paper3_MultiPhishGuard_Deliverables/Repro_Paper3_MultiPhishGuard_Deliverables/Repro_Paper3_MultiPhishGuard_Ablation.csv`
     - **Line 2 (Arm A: Single Agent CoT):** $\text{TN}=124, \text{FP}=26, \text{FN}=38, \text{TP}=12 \implies \sum = 200$. Legit $= 124 + 26 = 150$, Phishing $= 38 + 12 = 50$.
     - **Line 3 (Arm B: Static-Weight Triad):** $\text{TN}=149, \text{FP}=1, \text{FN}=45, \text{TP}=5 \implies \sum = 200$. Legit $= 149 + 1 = 150$, Phishing $= 45 + 5 = 50$.
   - **Files Inspected:** `Repro_Paper3_Benchmark_N200_Seed42.csv` (200 rows: 150 label `0`, 50 label `1`), `Repro_Paper3_telemetry.jsonl` (200 JSON records).
   - **Verdict:** Denominator and class distribution match 100% compliant in root deliverable.
   - ⚠️ **DISCREPANCY FLAGGED IN SUBFOLDER `Done/`:**
     - File: `kaggle_notebooks/Repro_Paper3_MultiPhishGuard_Deliverables/Repro_Paper3_MultiPhishGuard_Deliverables/Done/Repro_Paper3_MultiPhishGuard_Ablation.csv`
     - Line 2 (Arm A): $\text{TN}=139, \text{FP}=5, \text{FN}=2, \text{TP}=45 \implies \sum = 191$ ($N = 191 \neq 200$, missing 9 samples).
     - Line 3 (Arm B): $\text{TN}=140, \text{FP}=4, \text{FN}=9, \text{TP}=38 \implies \sum = 191$ ($N = 191 \neq 200$, missing 9 samples).
     - Root Cause: Experimental exploratory run using `gemini-3.1-flash-lite` where 9 API calls failed/timed out, yielding an incomplete $N=191$ slice. It must not be cited as the official $N=200$ benchmark deliverable.

5. **Legacy Check ($N = 1,494$ ElZemity baseline):**
   - Verified that no deliverable files in any folder contain the obsolete $N=1,494$ slice.

---

## 3. Step 2: Kaggle vs. Paper Equivalence (Percentile Bootstrap & Equivalence Margin)

**Pre-registered Protocol:**
- Percentile bootstrap 95% Confidence Interval with $B = 2,000$ resamples on per-sample predictions.
- Fixed equivalence margin: $\delta = 2.0\text{ percentage points (pp)}$.
- Equivalence criteria: Model is deemed concordant if the paper target falls within the 95% CI OR $|\text{observed} - \text{target}| \le \delta$.
- Invariant: McNemar testing is strictly forbidden for Kaggle vs. Paper comparison due to lack of per-instance ground truth predictions from published paper authors.

### 3.1. Paper 1: ViSoBERT on UIT-ViHSD ($N = 6,680$, Seed 42)
- **Observed Macro-F1:** $69.04\%$
- **95% Percentile Bootstrap CI ($B = 2,000$):** $[67.22\%, 70.93\%]$
- **Published Paper Target (Nguyen et al., EMNLP 2023 Table 4):** $68.77\%$
- **Equivalence Margin Check:**
  - $|\text{Observed} - \text{Target}| = |69.04 - 68.77| = 0.27\text{ pp} \le 2.0\text{ pp}$ (**PASS**)
  - Target inside 95% CI: $67.22\% \le 68.77\% \le 70.93\%$ (**PASS**)
- **Multi-Seed Stability:**
  - Seed 42: $69.04\%$
  - Seed 43: $68.82\%$
  - Seed 44: $69.13\%$
  - 3-Seed Mean: $69.00\% \pm 0.16\%$ (Paper target $68.77\%$ deviates by only $0.23\text{ pp}$).

### 3.2. Paper 1: ViSoBERT on UIT-VSMEC ($N = 693$, Seed 42)
- **Observed Macro-F1:** $64.60\%$
- **95% Percentile Bootstrap CI ($B = 2,000$):** $[60.31\%, 68.52\%]$
- **Published Paper Target (Nguyen et al., EMNLP 2023 Table 4):** $65.88\%$
- **Equivalence Margin Check:**
  - $|\text{Observed} - \text{Target}| = |64.60 - 65.88| = 1.28\text{ pp} \le 2.0\text{ pp}$ (**PASS**)
  - Target inside 95% CI: $60.31\% \le 65.88\% \le 68.52\%$ (**PASS**)
- **3-Seed Mean:** $64.40\% \pm 0.47\%$ (deviates by $1.48\text{ pp} \le 2.0\text{ pp}$).

### 3.3. Paper 2: BiGRU + WBCE on UCI SMS ($N = 1,115$)
- **Observed Spam Recall:** $83.89\%$ (95% Clopper-Pearson CI: $[76.99\%, 89.41\%]$)
- **Published Paper Target (Phap et al., 2026 Table 1):** $98.67\%$ Recall, $99.12\%$ Accuracy
- **Equivalence Check:**
  - $|\text{Observed} - \text{Target}| = |83.89 - 98.67| = 14.78\text{ pp} > 2.0\text{ pp}$ (**NOT MET**)
  - Target $98.67\%$ lies outside the 95% CI.
- **Profiling Concordance:**
  - BiGRU footprint: $3.86\text{ MB}$ (Paper: $5.21\text{ MB}$).
  - BiGRU latency: $2.631\text{ ms}$ CPU (Paper: $0.25\text{ ms}$ on mobile Snapdragon NPU).
  - DistilBERT baseline: $255.45\text{ MB}$, $48.972\text{ ms}$ CPU.
  - Directional ratio: $66.18\times$ footprint reduction and $18.61\times$ CPU speedup confirms the architectural edge efficiency advantage claimed by the paper.

### 3.4. Paper 3: MultiPhishGuard Triad on Council Slice ($N = 200$)
- **Arm B (Static-Weight Triad) Observed FPR:** $0.67\%$ (95% Clopper-Pearson CI: $[0.02\%, 3.66\%]$)
- **Arm A (Single Agent CoT) Observed FPR:** $17.33\%$ (95% Clopper-Pearson CI: $[11.65\%, 24.36\%]$)
- **Published Paper Target (Xue et al., 2025 Figure 5):** Multi-agent consensus suppresses False Alarm Rate from $19.8\%$ (single-agent) to $2.73\%$ (multi-agent council).
- **Equivalence Check:**
  - Multi-agent target ($2.73\%$) falls directly within Arm B 95% CI $[0.02\%, 3.66\%]$ (**PASS**).
  - Single-agent target ($19.8\%$) falls directly within Arm A 95% CI $[11.65\%, 24.36\%]$ (**PASS**).
  - Suppression effect direction: $17.33\% \to 0.67\%$ represents a $96.1\%$ relative false alarm reduction (exceeding paper's $86.2\%$ reduction).

---

## 4. Step 3: Model A vs. Model B Paired Hypothesis Testing

Rule 10.2 Invariant: Models evaluated on identical test samples must undergo paired statistical testing.

### 4.1. Multiclass Paired Bootstrap on $\Delta\text{Macro-F1}$

#### A. UIT-ViHSD (3 Classes, $N = 6,680$)
- Evaluation on Seed 42:
  - **ViSoBERT vs. PhoBERT-base:** $\Delta\text{Macro-F1} = +5.25\text{ pp}$, 95% CI: $[3.30\%, 7.15\%]$, $0 \notin \text{CI}$, $p_{\text{raw}} = 0.0005, p_{\text{BH}} = 0.0005$ (**Statistically Significant**).
  - **ViSoBERT vs. XLM-RoBERTa-base:** $\Delta\text{Macro-F1} = +4.18\text{ pp}$, 95% CI: $[2.28\%, 6.06\%]$, $0 \notin \text{CI}$, $p_{\text{raw}} = 0.0005, p_{\text{BH}} = 0.0005$ (**Statistically Significant**).
- Evaluation on Seed 43:
  - ViSoBERT vs. PhoBERT: $\Delta = +5.44\text{ pp}$, 95% CI: $[3.47\%, 7.29\%]$, $p_{\text{BH}} = 0.0005$ (**Significant**).
  - ViSoBERT vs. XLM-R: $\Delta = +4.04\text{ pp}$, 95% CI: $[2.11\%, 5.86\%]$, $p_{\text{BH}} = 0.0005$ (**Significant**).
- Evaluation on Seed 44:
  - ViSoBERT vs. PhoBERT: $\Delta = +4.62\text{ pp}$, 95% CI: $[2.74\%, 6.50\%]$, $p_{\text{BH}} = 0.0005$ (**Significant**).
  - ViSoBERT vs. XLM-R: $\Delta = +3.39\text{ pp}$, 95% CI: $[1.51\%, 5.34\%]$, $p_{\text{BH}} = 0.0005$ (**Significant**).
- **Consensus:** Across all 6 comparisons over 3 random seeds, $0 \notin \text{CI}$ uniformly, establishing definitive statistical superiority of ViSoBERT on Vietnamese social media hate speech detection.

#### B. UIT-VSMEC (7 Classes, $N = 693$)
- Evaluation on Seed 42:
  - ViSoBERT vs. PhoBERT: $\Delta = +5.73\text{ pp}$, 95% CI: $[0.95\%, 10.44\%]$, $0 \notin \text{CI}$, $p_{\text{BH}} = 0.0102$ (**Significant**).
  - ViSoBERT vs. XLM-R: $\Delta = +3.90\text{ pp}$, 95% CI: $[-0.84\%, 8.80\%]$, $0 \in \text{CI}$, $p_{\text{BH}} = 0.0585$ (Non-significant at $\alpha=0.05$).
- Multi-seed confirmation:
  - Seed 43: vs PhoBERT $+8.13\text{ pp}$ ($p_{\text{BH}} = 0.0030$); vs XLM-R $+6.69\text{ pp}$ ($p_{\text{BH}} = 0.0090$). Both significant.
  - Seed 44: vs PhoBERT $+6.13\text{ pp}$ ($p_{\text{BH}} = 0.0090$); vs XLM-R $+5.82\text{ pp}$ ($p_{\text{BH}} = 0.0090$). Both significant.

### 4.2. Binary Benchmarks: One-Sided Exact Binomial McNemar Test

#### A. Paper 3: Arm A (Single CoT) vs. Arm B (Static Triad) on Council Slice ($N = 200$)
- **Overall Accuracy Contingency Table:**
  - Both Correct: $129$
  - Arm A Correct, Arm B Incorrect ($b$): $7$
  - Arm A Incorrect, Arm B Correct ($c$): $25$
  - Both Incorrect: $39$
  - Total Discordant Pairs: $b + c = 32$.
- **Exact Binomial McNemar Test ($H_1: \text{Arm B} > \text{Arm A}$):**
  $$p = \sum_{k=25}^{32} \binom{32}{k} (0.5)^{32} = 1.051 \times 10^{-3} = 0.00105$$
  - Result: Statistically significant improvement in overall accuracy ($p < 0.005$).
  - Edwards continuity-corrected $\chi^2$: $\chi^2 = \frac{(|7 - 25| - 1)^2}{32} = \frac{289}{32} = 9.031 \implies p = 0.00265$.
- **Legit Subset (False Alarm Suppression, $N = 150$):**
  - Arm A TN, Arm B FP ($b$): $0$
  - Arm A FP, Arm B TN ($c$): $25$
  - Total Discordant: $b + c = 25$.
  - Exact Binomial Test: $p = (0.5)^{25} = 2.980 \times 10^{-8}$.
  - Result: Extremely significant false positive suppression ($p < 10^{-7}$). Arm B eliminated 25 false alarms with zero regressions on benign SMS.

#### B. Paper 2: Standard BCE vs. Weighted BCE (WBCE) on UCI SMS ($N = 1,115$)
- **Overall Accuracy Contingency Table:**
  - Both Correct: $1,081$; Both Incorrect: $22$.
  - BCE Correct, WBCE Incorrect ($b$): $7$; BCE Incorrect, WBCE Correct ($c$): $5$ ($b + c = 12$).
  - Exact Binomial Test (one-sided): $p = 0.8062$ (non-significant).
- **Spam Subset (Recall Gain, $N = 149$):**
  - BCE detected, WBCE missed ($b$): $4$; BCE missed, WBCE detected ($c$): $5$ ($b + c = 9$).
  - Exact Binomial Test (one-sided): $p = 0.5000$. (Net $+1$ True Positive gain, $124 \to 125$).

---

## 5. Step 4: Bounds, Metrics Distinction & Multiple Testing Corrections

### 5.1. Exact Clopper-Pearson 95% Confidence Intervals
Computed via exact Beta distribution quantiles ($\alpha = 0.05$):
$$\text{Beta}(\alpha/2; k, n - k + 1) \le p \le \text{Beta}(1 - \alpha/2; k + 1, n - k)$$
For zero events ($k = 0$), exact closed form $[0, 1 - (\alpha/2)^{1/n}]$ is applied (e.g., $0/19 \implies [0.00\%, 17.65\%]$).

| Benchmark & Model | Metric | Counts ($k / n$) | Point Estimate | Exact 95% Clopper-Pearson CI |
| :--- | :--- | :--- | :--- | :--- |
| **P3 Arm A (Single CoT)** | FPR | $26 / 150$ | $17.33\%$ | $[11.65\%, 24.36\%]$ |
| **P3 Arm A (Single CoT)** | Recall | $12 / 50$ | $24.00\%$ | $[13.06\%, 38.17\%]$ |
| **P3 Arm B (Triad)** | FPR | $1 / 150$ | $0.67\%$ | $[0.02\%, 3.66\%]$ |
| **P3 Arm B (Triad)** | Recall | $5 / 50$ | $10.00\%$ | $[3.33\%, 21.81\%]$ |
| **P2 BiGRU + BCE** | FPR | $2 / 966$ | $0.21\%$ | $[0.03\%, 0.75\%]$ |
| **P2 BiGRU + BCE** | Recall | $124 / 149$ | $83.22\%$ | $[76.24\%, 88.84\%]$ |
| **P2 BiGRU + WBCE** | FPR | $5 / 966$ | $0.52\%$ | $[0.17\%, 1.20\%]$ |
| **P2 BiGRU + WBCE** | Recall | $125 / 149$ | $83.89\%$ | $[76.99\%, 89.41\%]$ |
| **P1 ViSoBERT (ViHSD)** | Overall Error | $774 / 6,680$ | $11.59\%$ | $[10.83\%, 12.38\%]$ |

### 5.2. Strict Separation of FPR vs. FDR
Rule 10.4 Invariant: Prohibit conflating False Positive Rate (FPR) with False Discovery Rate (FDR).
- $\text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}$ (Fraction of negative/legit samples incorrectly flagged).
- $\text{FDR} = \frac{\text{FP}}{\text{FP} + \text{TP}}$ (Fraction of alarms that are false).

**Empirical Distinction on P3 & P2:**
- **P3 Arm A (Single CoT):** $\text{FPR} = 26/150 = 17.33\%$, whereas $\text{FDR} = 26/(26+12) = 26/38 = 68.42\%$. (Over two-thirds of raised alerts are bogus!).
- **P3 Arm B (Triad):** $\text{FPR} = 1/150 = 0.67\%$, whereas $\text{FDR} = 1/(1+5) = 1/6 = 16.67\%$. (Triad consensus slashes FDR by $51.75\text{ pp}$).
- **P2 BiGRU + BCE:** $\text{FPR} = 2/966 = 0.21\%$; $\text{FDR} = 2/126 = 1.59\%$.
- **P2 BiGRU + WBCE:** $\text{FPR} = 5/966 = 0.52\%$; $\text{FDR} = 5/130 = 3.85\%$.

### 5.3. Benjamini-Hochberg (BH) Multiple Hypothesis Testing Control

#### Family 1: P1 Multiclass Paired Differences — UIT-ViHSD (6 Hypotheses across 3 Seeds)
| Test Pair | Seed | Raw $p$-value | BH Rank ($i/m$) | Adjusted $p_{\text{BH}}$ | Significant ($\alpha=0.05$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| ViSoBERT vs. PhoBERT | 42 | $0.0005$ | $1/6$ | $0.0005$ | **YES** |
| ViSoBERT vs. XLM-R | 42 | $0.0005$ | $2/6$ | $0.0005$ | **YES** |
| ViSoBERT vs. PhoBERT | 43 | $0.0005$ | $3/6$ | $0.0005$ | **YES** |
| ViSoBERT vs. XLM-R | 43 | $0.0005$ | $4/6$ | $0.0005$ | **YES** |
| ViSoBERT vs. PhoBERT | 44 | $0.0005$ | $5/6$ | $0.0005$ | **YES** |
| ViSoBERT vs. XLM-R | 44 | $0.0005$ | $6/6$ | $0.0005$ | **YES** |

#### Family 2: P1 Multiclass Paired Differences — UIT-VSMEC (6 Hypotheses across 3 Seeds)
| Test Pair | Seed | Raw $p$-value | BH Rank ($i/m$) | Adjusted $p_{\text{BH}}$ | Significant ($\alpha=0.05$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| ViSoBERT vs. PhoBERT | 43 | $0.0005$ | $1/6$ | $0.0030$ | **YES** |
| ViSoBERT vs. XLM-R | 43 | $0.0030$ | $2/6$ | $0.0090$ | **YES** |
| ViSoBERT vs. PhoBERT | 44 | $0.0060$ | $3/6$ | $0.0090$ | **YES** |
| ViSoBERT vs. XLM-R | 44 | $0.0060$ | $4/6$ | $0.0090$ | **YES** |
| ViSoBERT vs. PhoBERT | 42 | $0.0085$ | $5/6$ | $0.0102$ | **YES** |
| ViSoBERT vs. XLM-R | 42 | $0.0585$ | $6/6$ | $0.0585$ | NO |

#### Family 3: P3 Binary McNemar Tests (2 Hypotheses)
| Test Target | Raw $p$-value | BH Rank ($i/m$) | Adjusted $p_{\text{BH}}$ | Significant ($\alpha=0.05$) |
| :--- | :--- | :--- | :--- | :--- |
| Benign Subset FPR Suppression | $2.980 \times 10^{-8}$ | $1/2$ | $5.960 \times 10^{-8}$ | **YES** |
| Overall Accuracy Discordance | $1.051 \times 10^{-3}$ | $2/2$ | $1.051 \times 10^{-3}$ | **YES** |

---

## 6. Audit Verdict Summary & Checkbox Verification

- [x] **Mọi bảng có cột TN/FP/FN/TP và tổng = N_test:** Đã đối soát chi tiết cho tất cả các file nhị phân và ma trận nhầm lẫn $3 \times 3$ của UIT-ViHSD ($5260 + 136 + 152 + 161 + 206 + 77 + 173 + 75 + 440 = 6,680$).
- [x] **Mọi % trong báo cáo đều truy ngược được về số nguyên:** 100% tỷ lệ được tính toán chính xác từ tử số và mẫu số nguyên.
- [x] **Không còn chuỗi `N/A` nào bị thay bằng số ước lượng:** Tất cả các chỉ số của UIT-ViHSD đã được tính toán đầy đủ từ 9 file dự đoán per-sample thực nghiệm.
- [x] **Báo cáo có ghi cả ca FAIL/PARTIAL:** Paper 2 được ghi nhận trung thực là **PARTIAL** với giải trình khoa học về độ lệch recall và 1 mẫu phân bổ.
