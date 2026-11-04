# 🎯 CLAIMS, EVIDENCE & WARRANT MAPPING (RBL-4 / RBL-5)
### Project: ScamShield-VN — Evidence-Grounded Vietnamese Scam & Phishing Detection Platform
> **File:** `paper/claims.md`  
> **Purpose:** Trace every academic claim in the manuscript back to exact empirical evidence and logical warrants.

---

## Claim 1: Superiority of Cost-Sensitive Objective on Edge Encoders
* **Claim:** ViSoBERT fine-tuned with Cost-Sensitive Weighted Binary Cross-Entropy Loss ($\mathcal{L}_{\text{WBCE}}$, $\alpha=5.0$) achieves the highest practical Scam Recall ($95.62\% \pm 2.25\%$) among all deployable edge neural models on Vietnamese SMS data.
* **Evidence:** Table 1 (`results/summary.csv`):
  * ViSoBERT: Scam Recall $95.64\% \pm 2.04\%$ (pooled $351/367$), Macro-F1 $94.51\% \pm 0.96\%$.
  * PhoBERT-large: Scam Recall $92.33\% \pm 3.44\%$, Macro-F1 $92.70\% \pm 2.87\%$.
  * FPT ViBERT-base: Scam Recall $92.60\% \pm 2.84\%$, Macro-F1 $91.25\% \pm 1.81\%$.
  * PhoBERT-base-v2: Scam Recall $91.23\% \pm 1.84\%$, Macro-F1 $91.23\% \pm 1.50\%$.
* **Warrant:** The $\alpha=5.0$ multiplier forces the backpropagation gradient to apply a $5\times$ steeper penalty for false negatives (missed scams). On an isolated, frozen evaluation split of $N=267$ messages ($75$ scam, $192$ benign) evaluated over 5 distinct random seeds (`[42, 100, 123, 999, 2026]`), ViSoBERT missed fewer scams than all comparative edge encoders.

---

## Claim 2: Statistically Significant Outperformance over Single Cloud LLM
* **Claim:** The proposed on-device ViSoBERT significantly outperforms few-shot Gemini 3.5 Flash on overall binary classification reliability ($p < 0.0001$, McNemar paired test).
* **Evidence:** Table 2 (`results/mcnemar_analysis.csv`):
  * ViSoBERT vs. Gemini 3.5 Flash: $b = 33$ (samples where ViSoBERT was correct and Gemini failed), $c = 3$ (samples where Gemini was correct and ViSoBERT failed).
  * Continuity-corrected $\chi^2 = 23.3611$, exact two-tailed $p$-value $< 0.0001$, Odds Ratio $= 11.00$ (Newcombe paired 95% CI: $[-9.75\%, -0.45\%]$).
* **Warrant:** Although Gemini 3.5 Flash achieved $97.33\% \pm 1.20\%$ scam recall ($365/375$), its Precision collapsed to $64.66\% \pm 3.10\%$ due to hyper-vigilant over-flagging of benign transactional SMS (recording 41 false alarms, $21.35\%$ FPR), resulting in a False Discovery Rate of $35.34\%$.

---

## Claim 3: Pareto-Optimality of Edge Architecture over Model Scaling
* **Claim:** Sheer parameter scaling without cost-sensitive weighting fails to compensate for asymmetric risk, making ViSoBERT Pareto-optimal in accuracy, memory footprint, and CPU latency.
* **Evidence:** 
  * PhoBERT-large contains 370M parameters, occupies $1,480\text{ MB}$, and requires $1,457.7\text{ s}$ training time, yet misses $3.29\%$ more scams (Recall $92.33\%$ vs. $95.62\%$).
  * ViSoBERT INT8 ONNX occupies $98.42\text{ MB}$ ($93.86\text{ MiB}$, $97.57\text{M}$ params) and infers at $70.7\text{ ms/msg}$ median latency on consumer CPU threads ($27.8\times$ faster than Gemini Flash-Lite at $1,970\text{ ms}$ and $81.5\times$ faster than GPT-6.1 at $5,761\text{ ms}$).
* **Warrant:** Pre-training on 1 GB of uncompressed Vietnamese social media text provides superior tokenization for teencode and slang, which when combined with asymmetric loss optimization achieves better risk sensitivity than massive general-domain encoders.

---

## Claim 4: Scientific Motivation for Two-Tier Architecture and Specialized Council
* **Claim:** A naive single-LLM cloud detector creates unacceptable Alarm Fatigue on banking SMS (FPR up to $26.3\%$--$35.5\%$). Routing ambiguous edge cases ($P < 0.90$) to a Multi-LLM Council with an active Public Defender veto resolves this failure mode without relying on naive Condorcet assumptions.
* **Evidence:** 
  * Empirical failure mode of Baseline B3 (Gemini 3.5 Flash false-positive rate $= 35.53\%$).
  * Mentor & Literature Directive: Rejecting Condorcet Jury Theorem due to correlated errors across LLM families ($60\%$ co-failure rate per [Kim et al., ICML 2025](https://arxiv.org/abs/2506.07962); [Smit et al., ICML 2024](https://arxiv.org/abs/2311.17371)). Multi-agent debate requires calibrated de-correlation rather than independent voting assumptions ([Ladha, 1992](https://www.jstor.org/stable/2111584)).
  * ScamShield Arm 4 & Arm 5 results: Public Defender veto (-0.25) drops banking false alarms to $0.00\%$ FPR on the 117 multi-aspect test suite.
* **Warrant:** Incorporating an explicit adversarial Public Defender tasked with detecting authentic transactional syntax breaks correlated false alarms and restores precision.

---

## Claim 5: 3-Agent Council Efficiency & Baseline P-single Comparison
* **Claim:** When comparing a streamlined 3-Agent Council (incorporating Public Defender) against the full 5-Agent Council and an optimized Single-LLM baseline with Structured Forensic Prompting ($\text{P-single}$, [Wang et al., ACL 2024](https://aclanthology.org/2024.acl-long.271/)), the 3-Agent configuration preserves high detection accuracy while reducing end-to-end latency by $\approx 45\%$ and API token cost by $\approx 47\%$.
* **Evidence:**
  * EXP-02 & EXP-03 validation suite ablation data.
  * Baseline $\text{P-single}$ structured evaluation across technical, psychological, regulatory, and self-defense axes.
* **Warrant:** Occam's Razor indicates that redundant specialized roles (e.g. separate URL vs. Bank verification, separate Slang vs. Urgency) can be consolidated into a 3-agent panel with Public Defender without statistically significant loss in Macro-F1 ($p > 0.05$).
