# Paper 2: Edge-AI deployment profiling results

This reproduction evaluates the deployment claim in M041 by directly comparing the proposed **BiGRU + WBCE** model with **DistilBERT** on the same Kaggle environment. The four TF-IDF classifiers are supplementary reference models; they are not the primary comparison.

## Main result: BiGRU + WBCE vs. DistilBERT

| Model | Spam recall (%) | F1 (%) | Serialized footprint (MB) | CPU latency mean (ms/message) | CPU latency P95 (ms) |
|---|---:|---:|---:|---:|---:|
| **BiGRU + WBCE (proposed)** | 83.89 | 89.61 | **3.86** | **2.631** | **4.589** |
| **DistilBERT (reference)** | 95.97 | 96.30 | 255.45 | 48.972 | 77.632 |

In this run, BiGRU + WBCE is approximately **66× smaller** than DistilBERT (255.45 / 3.86) and has approximately **18.6× lower mean CPU latency** (48.972 / 2.631). Its P95 latency is also lower: 4.589 ms versus 77.632 ms. These measurements support the paper's deployment-oriented conclusion that the proposed architecture is substantially lighter and faster than the DistilBERT reference, making it a plausible edge deployment candidate under the measured conditions.

The experiment supports the **direction and practical meaning** of the paper's claim; it is not expected to reproduce the paper's exact 5.21 MB / 0.25 ms figures because the implementation and deployment environment differ. The paper reports 256.02 MB / 40.78 ms for DistilBERT. Here, the measured DistilBERT latency is 48.972 ms. These are environment-specific measurements, not discrepancies to conceal or numbers to substitute for the paper's.

This result demonstrates feasibility from model footprint and CPU inference latency. It is not a physical-device deployment test and does not measure memory pressure, energy use, or mobile runtime overhead. DistilBERT also has higher recall and F1 in this experiment; the comparison is about deployment cost as well as predictive performance.

## Supplementary models

The following TF-IDF models provide additional context. They are supplemental baselines, not the main BiGRU-versus-DistilBERT test.

| Supplementary model | Spam recall (%) | F1 (%) | Footprint (MB) | CPU latency mean (ms/message) | CPU latency P95 (ms) |
|---|---:|---:|---:|---:|---:|
| TF-IDF + Logistic Regression | 82.55 | 90.44 | 0.21 | 0.843 | 0.942 |
| TF-IDF + Linear SVM | 92.62 | 95.83 | 0.21 | 0.625 | 0.741 |
| TF-IDF + Random Forest | 83.22 | 90.84 | 6.21 | 7.765 | 9.176 |
| TF-IDF + XGBoost | 85.91 | 91.76 | 0.31 | 1.196 | 1.301 |

Rule 10.6 disclosure: LR and Linear SVM are faster than BiGRU in this run, and LR is also smaller. Therefore, these results do **not** claim that edge deep learning is the fastest or smallest option overall. The primary finding is specifically that BiGRU + WBCE has substantially lower footprint and CPU latency than DistilBERT, while TF-IDF remains a strong, efficient supplementary alternative.

## Measurement setup

- Dataset: UCI SMS Spam Collection, N=5,574; fixed 80/20 stratified split, test N=1,115 (966 ham, 149 spam in this run).
- Footprint: neural models saved with `torch.save(state_dict)` and measured using `os.path.getsize`; BiGRU filename is `bigru_wbce.pt`. TF-IDF baselines use the serialized pickle size of the fitted vectorizer and classifier.
- Neural CPU latency: batch size 1, 50 warm-up inferences, 500 measured samples, and `time.perf_counter_ns()`; report mean and P95. DistilBERT and BiGRU were measured on the same machine using this protocol. Tokenization is outside the timer; tensor construction and model inference are inside it.
- Supplementary ML latency is measured on CPU through TF-IDF transformation and prediction; it is reported to disclose the behavior of these additional baselines.
- Hardware/runtime: Intel Xeon CPU @ 2.00 GHz, 4 vCPU (2 cores, 2 threads/core), PyTorch CPU threads=2, RAM=31.35 GiB; Python 3.13.16, PyTorch 2.11.0+cu130. Two Tesla T4 GPUs were available for training; latency profiling was performed on CPU.

## WBCE ablation (supporting result)

The paired BCE/WBCE ablation is a separate supporting analysis on the same single test split; it is not the deployment-profile comparison above.

| Variant | TN | FP | FN | TP | N | Spam recall (%) | Precision (%) | F1 (%) | Accuracy (%) | FPR (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BiGRU + Standard BCE | 964 | 2 | 25 | 124 | 1,115 | 83.22 | 98.41 | 90.18 | 97.58 | 0.21 |
| BiGRU + WBCE | 961 | 5 | 24 | 125 | 1,115 | 83.89 | 96.15 | 89.61 | 97.40 | 0.52 |

WBCE raises spam recall by 0.67 percentage points on this split, with slightly lower F1 and accuracy and higher FPR. This is one fixed split, not the paper's five-seed evaluation.

## Relation to the paper

M041's Abstract states that deployment profiling found a smaller serialized footprint and lower CPU latency for the proposed BiGRU-based model than for DistilBERT. The corresponding detailed discussion is in Section 6.2, “Deployment-oriented footprint and CPU latency.” The current reproduction supports that comparative conclusion under its Kaggle environment; exact numeric equality is not the objective. The publisher's online-first article is unpaginated, so a page number is **N/A**. Citation details are recorded in [`docs/citation_provenance/M041_EdgeAI_WBCE.md`](../../../docs/citation_provenance/M041_EdgeAI_WBCE.md).

## Artifacts

- `Repro_Paper2_UCI_SMS_Comparison.csv` — primary two-model comparison plus supplementary baselines; includes numeric mean and P95 latency columns.
- `Repro_Paper2_WBCE_Ablation.csv` — BCE/WBCE confusion counts and metrics.
- `Repro_Paper2_per_sample_predictions.csv` — paired predictions/probabilities for all 1,115 test rows.
- `bigru_wbce.pt`, `distilbert_uci.pt` — serialized model state dictionaries.
- `sms_spam.zip` — downloaded UCI dataset archive.
- Notebook: [`kaggle_notebooks/Repro_Paper2_EdgeAI_WBCE_and_ExplainableDetector_UCI5574.ipynb`](../../../kaggle_notebooks/Repro_Paper2_EdgeAI_WBCE_and_ExplainableDetector_UCI5574.ipynb).

Paper: [Huynh Cong Phap, “Edge-AI enabled smishing and suspicious SMS detection: a cost-sensitive and lightweight deep learning architecture”](https://doi.org/10.1080/24751839.2026.2713250), *Journal of Information and Telecommunication* (2026).
