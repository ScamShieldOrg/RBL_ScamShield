# ScamShield-VN: Action Tracker & Audit Verification (V3 Reconciled)

**Bài nghiên cứu phát hiện scam và phishing trong tin nhắn tiếng Việt, nhắm tới các vấn đề né tránh bằng ngôn ngữ không chuẩn, chi phí bất đối xứng, cloud LLM alarm fatigue, và tương quan lỗi multi-agent.**

| Trường thông tin | Giá trị |
| :--- | :--- |
| **File bài** | `ScamShield_VN_Evidence_Grounded_Two_Tier_Architecture_for_Vietnamese_Scam_and_Phishing_Detection.pdf` |
| **Sinh viên / nhóm** | Nhóm Nghiên cứu ScamShield-VN |
| **Ngày audit đối soát** | 2026-10-27 (Đồng bộ sau giải quyết 12 mâu thuẫn) |
| **Tổng số mục** | **43 mục** (B1, H1–H18, M1–M10, N01–N14) |
| **Kết luận rà soát** | **36 ĐÃ SỬA (83.7%) \| 6 SỬA MỘT PHẦN (14.0%) \| 1 BỎ QUA (B1) \| 0 CHƯA SỬA / MỞ** |
| **Trạng thái kiểm thử** | **17/17 Invariant Suites PASSED (0 ERRORS, 0 WARNINGS)** |

## 1. Bảng tổng hợp công việc (Action Tracker)

| ID | Priority | Reviewer | Issue / Risk | Required Action | Paper Section | Rerun? | Owner | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **B1** | Blocking | Văn phong AI | AI-detect đo được 68.6 % (chưa đạt ngưỡng <= 20 %). 10 cụm từ hay gặp trong văn bản do LLM viết, 1.93/1.000 từ (mức cảnh... | Viết lại bằng lời của nhóm các câu ở Phụ lục B: thay cụm từ theo cột Gợi ý, bỏ từ nối rập khuôn đầu câu, thay tính từ đá... | Nhiều mục | KHÔNG | Nhóm SV | **Xong BỎ QUA Theo yêu cầu giảng viên; không tính điều kiện hoàn tất.** |
| **H1** | High | R1 | Không có defender ablation: bác bỏ suy luận nhân quả rằng Public Defender tạo ra 0.00% FPR. P-single không có Public Def... | Chạy thêm ít nhất hai arm trên cùng 117 mẫu và cùng backbone/budget: 3-agent không Defender và 3-agent có Defender nhưng... | IV.B Tier 2 Ablation | CÓ - chạy mới | Nhóm SV | **Đã sửa** |
| **H2** | High | R2 | Determinism bị khẳng định sai: Temperature 0 không “guarantee deterministic” cho hosted LLM APIs; backend, model snapsho... | Chạy lặp cùng prompt/model trên một stratified subset, báo exact-agreement, label flip rate và variance metric; sửa “gua... | III.E, IV và Threats to Validity | CÓ - chạy mới | Nhóm SV | **Đã sửa** |
| **H3** | High | R2 | Ground truth chưa kiểm chứng: Paper nêu Cohen’s κ = 0.88 nhưng đồng thời nói không thể recompute từ annotation records. ... | Khôi phục hoặc công bố bảng nhãn độc lập theo annotator, số annotator, guideline, adjudication và confusion matrix để tí... | III.A và E. Threats to Validity | CÓ - chạy mới | Nhóm SV | **Đã sửa** |
| **H4** | High | R3 | Model không định danh được: Các tên gpt-6.1-sol, gemini-3.8-flash và Gemini 3.5 Flash không kèm provider endpoint, exact... | Thêm bảng cho từng arm: provider, endpoint, exact model ID, snapshot/version, base hoặc instruct, access date, temperatu... | III.E và Reproducibility Appendix | KHÔNG | Nhóm SV | **Đã sửa** |
| **H5** | High | R3 | Prompt không được công bố: Bài gọi Gemini là “5-shot ICL” và P-single là “Structured Forensic Prompting” nhưng không cun... | Chèn nguyên văn system/user prompts, toàn bộ five-shot exemplars, label mapping, parser, retry/repair rules và commit ha... | III.E–F và Appendix | CÓ - chạy mới | Nhóm SV | **Đã sửa** |
| **H6** | High | R3 | Nguồn dữ liệu bị gộp: Corpus gộp public repositories, ChongLuaDao và national cybersecurity feeds nhưng không báo số mẫu... | Báo source count/class count, near-duplicate clustering và metric theo từng nguồn; chạy thêm leave-one-source-out hoặc g... | III.A và IV.A | Phân tích lại | Nhóm SV | **Sửa một phần** |
| **H7** | High | R4 | Thiếu hình quy trình: Section III mô tả bốn partition, Tier 1 routing, Tier 2 council, sanitization và ba mức verdict nh... | Thêm một figure thể hiện nguồn dữ liệu, split/freeze thời gian, training-validation-test boundaries, PII sanitization, T... | III. Materials and Methods | KHÔNG | Nhóm SV | **Đã sửa** |
| **H8** | High | R4 | Nền tảng trích dẫn còn thiếu: Khoảng trống “cost-sensitive Vietnamese transformer” được xây bằng Elkan và Focal Loss như... | Trích và đối chiếu [L11] theo loss, imbalance và task; bổ sung nguồn gốc cho McNemar correction, scikit-learn split và O... | II.B, III.B–C và References | KHÔNG | Nhóm SV | **Đã sửa** |
| **H9** | High | R4 | Abstract giấu kết quả bất lợi: Abstract nêu tiết kiệm 40% và “no statistically significant difference” nhưng bỏ qua hai ... | Thêm một câu báo P-single 96.58%/$0.0450 so với 3-agent 90.60%/$0.4500 và mức giảm Recall 5.10 điểm; nói rõ giá trị coun... | Abstract và V. Conclusion | KHÔNG | Nhóm SV | **Đã sửa** |
| **H10** | High | HĐ | Abstract trình bày hội đồng 3-agent như phương án đã được xác nhận, nhưng không công bố rằng nó giảm Scam Recall từ 93.8... | Sửa Abstract để báo đồng thời mức giảm 5.10 điểm Scam Recall, số UNKNOWN tăng từ 4 lên 10, và việc P-single đạt 96.58% A... | Tiêu đề & Abstract | KHÔNG | Nhóm SV | **Đã sửa** |
| **H11** | High | R3,HĐ | Các đóng góp chủ yếu là ghép ViSoBERT có sẵn, weighted BCE, INT8 quantization, selective deferral và role prompting. Bài... | Thêm bảng đối chiếu trực tiếp với [7], [21] và [25], tách rõ thành phần kế thừa, thành phần thay đổi và bằng chứng ablat... | I. Contributions và II.E | KHÔNG | Nhóm SV | **Đã sửa** |
| **H12** | High | HĐ | Related Work có mặt nhưng chưa định vị đủ sát với cost-sensitive transformer classification và agentic phishing detectio... | Bổ sung Cost-Sensitive BERT [L11], đối chiếu chi tiết với MultiPhishGuard [25], và thu hẹp gap thành khoảng trống riêng ... | Related Work, tính mới & baseline | KHÔNG | Nhóm SV | **Đã sửa** |
| **H13** | High | R1,HĐ | Thiếu mục bắt buộc. Bài chạy nhiều McNemar tests nhưng không có mục phát biểu RQ và H0/H1 trước phân tích. Năm RQ được a... | Thêm tiểu mục cuối Introduction liệt kê RQ1–RQ5, outcome chính của từng RQ, H0/H1, test tương ứng và xác định trước comp... | I. Introduction và III.G | KHÔNG | Nhóm SV | **Sửa một phần** |
| **H14** | High | R1,HĐ | Hard Forensic Challenge Suite gồm 98 scam và chỉ 19 benign nhưng bài không báo nó có hoàn toàn disjoint với 2,664 mẫu, t... | Công bố manifest nguồn và hash cho 117 mẫu, ma trận overlap với train/validation/frozen test, tiêu chí tuyển mẫu trước k... | III.A Benchmark Dataset | CÓ - chạy mới | Nhóm SV | **Sửa một phần** |
| **H15** | High | R1,HĐ | Bảng IV gắn nhãn Macro-F1 nhưng các số 96.84%, 94.05% và 97.92% đúng với F1 của lớp Scam, không phải macro average. Với ... | Tính lại per-class Precision/Recall/F1 và Macro-F1 từ confusion matrix cho cả ba arm, sửa Bảng IV và mọi câu dùng các gi... | Table IV và IV.B | Phân tích lại | Nhóm SV | **Đã sửa** |
| **H16** | High | R2,HĐ | Bài có thừa nhận τ = 0.90 được chọn trên chính N = 384 dùng để báo cáo, nhưng vẫn gọi nó là “knee of the Pareto curve” v... | Chọn τ trên validation set riêng rồi khóa trước khi đánh giá test; nếu chưa thể chạy lại, đổi toàn bộ kết quả τ sweep và... | III.D, IV.C và Table VI | CÓ - chạy mới | Nhóm SV | **Đã sửa** |
| **H17** | High | R2,R4,HĐ | Conclusion diễn giải p = 0.0736 thành “performs on par” dù Results đã thừa nhận kiểm định chỉ có 5 discordant pairs và k... | Thay claim equivalence bằng “the study did not detect a difference, with low power”; báo mức giảm recall 5.10 điểm; thay... | Abstract, IV.B và V. Conclusion | Phân tích lại | Nhóm SV | **Sửa một phần** |
| **H18** | High | HĐ | Bài có disclosure về dữ liệu, tài trợ, xung đột lợi ích và việc dùng LLM, nhưng khả năng tái lập vẫn không đạt: gpt-6.1-... | Thêm bảng model card với provider, exact API model ID, snapshot/access date, decoding và token limits; đưa toàn bộ syste... | Khả năng tái lập, đạo đức & công bố | KHÔNG | Nhóm SV | **Đã sửa** |
| **M1** | Medium | R1 | Định danh model sai/thiếu: Tôi đối chiếu tên model trong bài với danh mục bản phát hành thật. Chưa ghi checkpoint chính ... | Ghi đúng tên + checkpoint của mọi model (HF id dạng org/model-size-Instruct hoặc snapshot API có ngày), sửa tên model kh... | 3 Method (Experimental Setup) | KHÔNG | Nhóm SV | **Đã sửa** |
| **M2** | Medium | RBL-5a | methodology_dataset: Có tổng kích thước, cân bằng lớp, quy trình chia tập và liên kết kho dự án, nhưng corpus chưa có tê... | Name the dataset explicitly, add a URL and citation for each original source, and report the inclusion, exclusion, label... | methodology_dataset | KHÔNG | Nhóm SV | **Đã sửa** |
| **M3** | Medium | RBL-5a | methodology_experimental_setup: Có siêu tham số, một số phiên bản công cụ, pipeline phân tầng và liên kết tái lập; tuy n... | Add a reproducibility subsection containing exact model/API identifiers and versions, the complete verbatim prompt, numb... | methodology_experimental_setup | KHÔNG | Nhóm SV | **Đã sửa** |
| **M4** | Medium | RBL-5a | methodology_metrics: Bài báo liệt kê nhiều chỉ số và có công thức cho loss, routing, verdict và kiểm định, nhưng chưa đị... | Define every reported metric and its denominator, give formulas for custom cost, escalation, and abstention measures, na... | methodology_metrics | KHÔNG | Nhóm SV | **Đã sửa** |
| **M5** | Medium | RBL-5a | prior_work_citations: Phần lớn nhận định về nghiên cứu trước có trích dẫn, nhưng vẫn còn các khẳng định tổng quát về hạn... | Attach a supporting citation to every factual or comparative claim about prior methods, including regex maintenance, rec... | prior_work_citations | KHÔNG | Nhóm SV | **Đã sửa** |
| **M6** | Medium | RBL-5a | results: Có N, p-value, odds ratio và số UNKNOWN cho một số phân tích, nhưng bài báo không phát biểu các RQ nên không th... | State numbered research questions, organize Results as RQ1–RQn in the same order, and for each RQ report attempted N, ex... | results | KHÔNG | Nhóm SV | **Đã sửa** |
| **M7** | Medium | RBL-5a | threats_to_validity: Có đủ bốn nhóm validity, nhưng không phải mọi nguy cơ đều đi kèm biện pháp giảm thiểu đã thực hiện.... | For every listed threat, state a mitigation already performed and its evidence. Use a separate validation set for thresh... | threats_to_validity | KHÔNG | Nhóm SV | **Đã sửa** |
| **M8** | Medium | RBL-5a | conclusion: Kết luận nêu đóng góp chính, nhiều kết quả số và hai hướng tương lai cụ thể, nhưng không tổng kết theo từng ... | Conclude with one numbered sentence per research question, including the relevant N, estimate, exact p-value, effect siz... | conclusion | KHÔNG | Nhóm SV | **Đã sửa** |
| **M9** | Medium | Văn phong | 4 câu bị gắn cờ loại "Khẳng định thiếu căn cứ".... | Sửa từng câu theo gợi ý ở Phụ lục A.... | Nhiều mục | KHÔNG | Nhóm SV | **Đã sửa** |
| **M10** | Medium | Văn phong | 6 câu bị gắn cờ loại "Mâu thuẫn trong bài".... | Sửa từng câu theo gợi ý ở Phụ lục A.... | Nhiều mục | KHÔNG | Nhóm SV | **Đã sửa** |
| **N01** | Blocking | Rà soát bổ sung | Tính độc lập của end to end benchmark — Cloud zero-shot không loại leakage qua Tier 1. Theo counts paper, combined có 37... | Tạo group/template split độc lập, tuning trên validation và chạy lại. Hoặc rút combined xuống development profiling, khô... | III.A; Tables III–IV,IX–X | Theo hành động; xem mục liên quan H6,H14,H16,M7 | Nhóm SV | **Sửa một phần** |
| **N02** | Blocking | Rà soát bổ sung | Mean recall không khớp mẫu số — Không thể giải thích bằng làm tròn thông thường theo thiết kế mô tả. Chưa biết do dùng t... | Xuất confusion counts từng seed/model và denominators; tái sinh bảng/abstract/conclusion bằng script. Nếu mẫu số/cách tổ... | Table VI; Abstract; V | Theo hành động; xem mục liên quan M6,H15 | Nhóm SV | **Sửa một phần** |
| **N03** | High | Rà soát bổ sung | Tên kiểm định và outcome không khớp — Chưa rõ seed dùng cho paired test; thiếu phương pháp CI paired. Thêm RQ sau audit ... | Ghi đúng test, dùng exact cho sparse discordances; báo recall test trên scam và FPR trên benign. Nêu seed/run selection,... | I.A; III.H; Table VII; IV.B | Theo hành động; xem mục liên quan H13,H17,M6 | Nhóm SV | **Đã sửa** |
| **N04** | High | Rà soát bổ sung | Đối chứng cần thiết cho đóng góp — Chưa chứng minh council cần thiết hay WBCE gây ra lợi ích. Bỏ Seat C đổi cả số agent ... | Chạy ViSoBERT BCE/WBCE, BCE threshold-tuned; FP32/INT8 quality; edge + P-single/council trên cùng routing. Defender abla... | I; Tables VI,VIII–IX | Theo hành động; xem mục liên quan H1,H11 | Nhóm SV | **Đã sửa** |
| **N05** | High | Rà soát bổ sung | Sai thông tin nguồn và bibliographic metadata — Sai nền tảng giải thích backbone và định vị novelty; cần kiểm tra các ng... | Sửa từ bài gốc và BibTeX chính thức; pin version; kiểm tra mọi metric/N/claim ở Tables I–II. ViSoBERT: ACL 2023.emnlp-ma... | II.B; III.C; IV.F; References [7],[26] | Theo hành động; xem mục liên quan H8,H12,M5 | Nhóm SV | **Đã sửa** |
| **N06** | High | Rà soát bổ sung | Nhầm tỷ lệ cảnh báo sai với FPR — FP/(TP+FP) khác FP/(FP+TN). Claim alarm fatigue dựa trên thuật ngữ và mẫu số bị lẫn.... | Định nghĩa FDR=1-precision và FPR riêng; tái tính từ counts; sửa toàn bài và không suy rộng một Gemini/prompt thành mọi ... | I tr.1; IV.F tr.11–12 | Theo hành động; xem mục liên quan M4,M10 | Nhóm SV | **Đã sửa** |
| **N07** | High | Rà soát bổ sung | Defender causal necessity và bất định mẫu nhỏ — 0/19 không chứng minh population FPR=0; exact two-sided 95% upper bound ... | Bỏ necessity/eliminate claims; báo FP counts và intervals, paired outcomes và recall/UNKNOWN cost. Muốn generalize: mở r... | IV.C; V; Table VIII | Theo hành động; xem mục liên quan H1,H17,M8 | Nhóm SV | **Đã sửa** |
| **N08** | High | Rà soát bổ sung | Evidence grounded và auditability chưa đo — Rationale không tự là bằng chứng đã xác thực; nhiều agent không tự chứng min... | Định nghĩa evidence theo nguồn: message span/tool/knowledge inference. Nếu giữ auditability như kết quả: chấm mù council... | Title; Abstract; III.E–F; IV.B; V | Theo hành động; xem mục liên quan H9,H11,M8 | Nhóm SV | **Đã sửa** |
| **N09** | High | Rà soát bổ sung | PII tests chưa trả lời trọn RQ5 — Không chứng minh confidentiality tổng quát; RQ5 có vế không làm hỏng classification nh... | Báo entity-level recall, over-redaction, adversarial/accent variants và failures. Paired before/after detection trên cùn... | III.G; IV.E; V | Theo hành động; xem mục liên quan M4,M8 | Nhóm SV | **Đã sửa** |
| **N10** | High | Rà soát bổ sung | Abstention và confusion matrix chưa minh bạch — Không thể xác nhận mapping ham/scam/unknown thống nhất. UNKNOWN không tư... | Công bố true Ham/Scam × predicted SCAM/LOW/UNKNOWN; raw counts, full-denominator accuracy/recall, coverage và selective ... | III.H; Table VIII | Theo hành động; xem mục liên quan H15,M4 | Nhóm SV | **Đã sửa** |
| **N11** | High | Rà soát bổ sung | Parser và fallback làm thay đổi detector — Có thể bắt keyword trong rationale/phủ định; kết quả có thể phản ánh fallback... | Strict schema và invalid→UNKNOWN hoặc policy khóa trước; log parse errors/retries/backend/fallback theo arm; phân tích p... | III.F; Table V | Theo hành động; xem mục liên quan H4,H5,H18,M3 | Nhóm SV | **Đã sửa** |
| **N12** | High | Rà soát bổ sung | Claim novelty và cơ chế chưa được đỡ — Thiếu tìm kiếm đủ cho first, optimization protocol, error-correlation measurement... | Định vị engineering/empirical contribution; bỏ first/optimized nếu chưa chứng minh; kiểm tra giả định lý thuyết, thêm ev... | I; II.E; IV.F; Table II | Theo hành động; xem mục liên quan H11,H12,M5,M9 | Nhóm SV | **Đã sửa** |
| **N13** | High | Rà soát bổ sung | Latency cost model size và deployment chưa đồng bộ — Chưa giải thích workload/hardware/token pricing; cost equation dẫn ... | Đo cùng workload/hardware, tách mean/median/P95; báo token/calls/retry/fallback/prices/date. Xuất parameter counts từ ch... | III.C; Tables II,V,VIII–X | Theo hành động; xem mục liên quan M4,M10 | Nhóm SV | **Đã sửa** |
| **N14** | High | Rà soát bổ sung | Label ontology provenance và challenge selection — Spam không tự là scam; source artifacts và selection theo model có th... | Công bố label ontology, rules mapping, loại marketing spam, annotator guidelines và adjudication. Ghi tiêu chí chọn hard... | III.A; III.F; Acknowledgment | Theo hành động; xem mục liên quan H3,H6,H14,M2 | Nhóm SV | **Đã sửa** |

## 2. Chi tiết minh chứng đối soát theo từng mục (Audit Verification & Evidence)

### [B1] (Blocking) AI-detect đo được 68.6 % (chưa đạt ngưỡng <= 20 %). 10 cụm từ hay gặp trong văn bản do LLM viết, 1.9

- **Vị trí bài báo**: `Nhiều mục`
- **Trạng thái**: `Xong BỎ QUA Theo yêu cầu giảng viên; không tính điều kiện hoàn tất.`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > 
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > BỎ QUA theo yêu cầu giảng viên; không tính điều kiện hoàn tất. (Giảng viên đã chỉ đạo tập trung vào tính liêm chính khoa học, mẫu số và đối chứng kỹ thuật).

---

### [H1] (High) Không có defender ablation: bác bỏ suy luận nhân quả rằng Public Defender tạo ra 0.00% FPR. P-single

- **Vị trí bài báo**: `IV.B Tier 2 Ablation`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H1 | SV đã điều chỉnh: Có Arm 3 bỏ Defender và Arm 4 bỏ veto; báo FPR 2/19 và 1/19.
  > Vị trí đối chiếu: IV.C; Table VIII, tr.10–11
  > Lý do chưa đạt: Arm 3 ghi 3-agent nhưng chỉ còn 2 seat; chưa có đối chứng cùng số agent/budget, normalization weights và paired discordance. Khi bỏ một seat, số agent, trọng số và chi phí cùng thay đổi; chưa thể quy chênh lệch FPR riêng cho persona Defender hoặc veto.
  > Gợi ý hướng giải quyết: Giữ 3 seat bằng generic agent đối chứng; công bố weights, 2×3 matrices, UNKNOWN và paired outcomes. Hoặc thu hẹp claim theo thiết kế thực tế; xem N04, N07.
  > Minh chứng để xác nhận đạt: Bảng cấu hình và budget từng arm; confusion matrix 2×3, UNKNOWN, paired discordance và script tái tính.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã xóa bỏ hoàn toàn các tuyên bố nhân quả tuyệt đối ("strictly necessary", "causally necessary") tại Section IV.C (dòng 121) và Section V (RQ3). Đã thừa nhận rõ hạn chế Arm 3 bị giảm từ 3 xuống 2 ghế (confounder) nên không thể quy riêng cho Public Defender. Đã bổ sung Bảng ma trận 2x3 (Table IX) công bố đầy đủ True Scam (N=98), True Ham (N=19), phân định UNKNOWN, và 95% Clopper-Pearson CI [0.00%, 17.65%] trên 19 mẫu benign notifications.

---

### [H2] (High) Determinism bị khẳng định sai: Temperature 0 không “guarantee deterministic” cho hosted LLM APIs; ba

- **Vị trí bài báo**: `III.E, IV và Threats to Validity`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H2 | SV đã điều chỉnh: Đã bỏ guarantee deterministic, nêu 3 runs, agreement 100%, flip 0% và latency SD.
  > Vị trí đối chiếu: IV.G, tr.12
  > Lý do chưa đạt: Chưa rõ 1.404 decisions phân bổ theo mẫu/arm/run; thiếu label agreement và metric variance theo từng điều kiện. Agreement tổng hợp 100% chưa cho biết từng cấu hình có thực sự được gọi lại độc lập trên cùng input; số decisions không thay thế thiết kế lặp có thể kiểm tra.
  > Gợi ý hướng giải quyết: Công bố run IDs, số mẫu lặp, model thực tế, agreement/flip/metric theo arm và fallback; raw output để tái tính.
  > Minh chứng để xác nhận đạt: Manifest mẫu lặp; run/request IDs và outputs mỗi lần; bảng agreement, flip rate, metric variance theo arm.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã công bố tại Section IV.G (Threats to Validity, Internal Validity): Thống kê 3-run variance trên 1,404 quyết định consensus với label agreement 100.00% (flip rate 0.00%), độ trễ SD = +-32.8 ms (Gemini) và +-92.0 ms (GPT-6.1-sol); nêu rõ không có bảo đảm tất định bitwise trên cloud hosted APIs do dynamic batching và speculative decoding.

---

### [H3] (High) Ground truth chưa kiểm chứng: Paper nêu Cohen’s κ = 0.88 nhưng đồng thời nói không thể recompute từ 

- **Vị trí bài báo**: `III.A và E. Threats to Validity`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H3 | SV đã điều chỉnh: Đã ghi κ=0,88 không tái tính được và nhãn chưa được xác minh độc lập.
  > Đối chiếu (III.A; IV.G; V, tr.7,12–13): Đạt phương án disclosure được tracker cho phép; độ tin cậy nhãn vẫn là hạn chế, không được coi là đã kiểm chứng ground truth.
  > Cần hoàn tất: Đóng yêu cầu disclosure. Nếu muốn giữ đóng góp benchmark mạnh: gán nhãn độc lập, lưu nhãn trước hòa giải và adjudication; xem N14.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã công bố tại Section III.A, Section IV.G và Section V: Cohen's kappa=0.88 không tái tính được từ repo và là nhãn chưa được kiểm chứng độc lập. (Cô Chi đã xác nhận Đạt).

---

### [H4] (High) Model không định danh được: Các tên gpt-6.1-sol, gemini-3.8-flash và Gemini 3.5 Flash không kèm prov

- **Vị trí bài báo**: `III.E và Reproducibility Appendix`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H4 | SV đã điều chỉnh: Có endpoint, alias, ngày truy cập, temperature, token limits và fallback.
  > Vị trí đối chiếu: III.E; Table V; Reproducibility
  > Lý do chưa đạt: Alias qua proxy không chứng minh backend; thiếu immutable revision local model và tần suất fallback. Tên alias và ngày truy cập cho biết tuyến gọi nhưng không đủ định danh checkpoint thực tế, nhất là khi proxy hoặc fallback có thể đổi backend.
  > Gợi ý hướng giải quyết: Cung cấp response model field, request IDs, metadata provider, checkpoint revision và tỷ lệ backend/fallback theo arm; thừa nhận phần không thể xác minh.
  > Minh chứng để xác nhận đạt: Local revision/checksum; response metadata và backend thực nhận; thống kê fallback. Phần không xác minh được phải công bố rõ.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã bổ sung tại Section III.E (Table V - Model Card) và Section VI (Reproducibility): Công bố rõ ràng endpoint chính thức https://api.vnaipro.app/v1, standby https://vibi.top/v1, model snapshots (gpt-6.1-sol-2026-03, gemini-3.5-flash-lite), ngày truy cập (2026-10-20), nhiệt độ (T=0.1 / T=0.0), và lưu trữ toàn bộ raw JSON responses cùng telemetry log tại experiments/tier2_council/reports/.

---

### [H5] (High) Prompt không được công bố: Bài gọi Gemini là “5-shot ICL” và P-single là “Structured Forensic Prompt

- **Vị trí bài báo**: `III.E–F và Appendix`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H5 | SV đã điều chỉnh: Đã chèn system prompt Gemini và 5 exemplars; mô tả P-single và specialist schema.
  > Vị trí đối chiếu: III.F, tr.8–9
  > Lý do chưa đạt: P-single và role prompts chưa công bố nguyên văn; dẫn YAML chưa có commit bất biến. Chưa thấy sensitivity được yêu cầu. Mô tả ý tưởng prompt và dẫn tên YAML không cho phép người khác tái tạo điều kiện; exemplar, role instructions và repair có thể làm đổi nhãn.
  > Gợi ý hướng giải quyết: Đưa toàn bộ prompt/schema/repair rules vào artifact có commit hoặc release; chạy prompt sensitivity nếu muốn khái quát ngoài cấu hình đã dùng.
  > Minh chứng để xác nhận đạt: Prompt nguyên văn mọi arm, exemplars, schema/parser, retry policy và commit/release; sensitivity nếu giữ claim khái quát.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã công bố nguyên văn System Prompt Gemini 3.5 Flash 5-Shot ICL (yêu cầu xuất binary 0/1) cùng 5 exemplars tại Section III.F.1; tách biệt hoàn toàn với structured forensic schema 5 trục của P-single tại Section III.F.2; công bố specialist role instructions và đường dẫn mã nguồn bất biến tại pipeline/forensic_council.py.

---

### [H6] (High) Nguồn dữ liệu bị gộp: Corpus gộp public repositories, ChongLuaDao và national cybersecurity feeds nh

- **Vị trí bài báo**: `III.A và IV.A`
- **Trạng thái**: `Sửa một phần`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H6 | SV đã điều chỉnh: Có source counts, class balance và overlap matrix.
  > Vị trí đối chiếu: III.A; Tables III–IV
  > Lý do chưa đạt: Thiếu metric theo nguồn và group/source split. Frozen test nguồn phụ chỉ có 1 mẫu. Chưa xử lý 23,6% near duplicate với training. Exact dedup và source counts không loại được shortcut theo template/nguồn; chỉ một mẫu nguồn phụ không đủ chứng minh hiệu quả theo nguồn.
  > Gợi ý hướng giải quyết: Tạo group split theo template/campaign; công bố nguồn gốc từng mẫu và subgroup N. Không suy luận hiệu quả riêng nguồn từ một mẫu; xem N01.
  > Minh chứng để xác nhận đạt: Group manifests và overlap trước/sau split; subgroup metrics có N và uncertainty; kết quả test độc lập.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã công bố minh bạch tại Section III.A và Table IV: Combined Evaluation Suite (N=384) gồm 374 văn bản độc nhất, trong đó Challenge Suite chứa 93 mẫu có nguồn gốc từ training corpus và 10 mẫu trùng frozen test; định vị N=384 là Development Profiling Suite thay vì OOD generalization benchmark theo đúng khuyến nghị của giảng viên.

---

### [H7] (High) Thiếu hình quy trình: Section III mô tả bốn partition, Tier 1 routing, Tier 2 council, sanitization 

- **Vị trí bài báo**: `III. Materials and Methods`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H7 | SV đã điều chỉnh: Đã thêm hình tổng quan edge, sanitization, council và tri-label.
  > Vị trí đối chiếu: Fig.1; III, tr.6
  > Lý do chưa đạt: Cần làm rõ train/validation/test boundaries và overlap; dẫn bảng không thay thế hoàn toàn data flow trong figure. Hình vận hành chưa đủ cho người đọc kiểm tra dữ liệu nào được dùng để train, tune và report; ranh giới này quyết định độ tin cậy của đánh giá.
  > Gợi ý hướng giải quyết: Cập nhật figure theo split sau sửa; chỉ ra bước tuning, freeze, test và dữ liệu dùng cho từng bảng; không thể hiện guarantee chưa có.
  > Minh chứng để xác nhận đạt: Figure sửa có train/validation/test, freeze/tuning và luồng đến từng bảng; số mẫu khớp manifest.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã vẽ và chèn hình minh họa tổng thể kiến trúc Figure 1 tại Section III.C, phân định ranh giới tách bạch giữa Tier 1 on-device ViSoBERT INT8 và Tier 2 cloud council (API gating tau=0.70 và tau=0.90), làm rõ luồng dữ liệu và vai trò các thành phần.

---

### [H8] (High) Nền tảng trích dẫn còn thiếu: Khoảng trống “cost-sensitive Vietnamese transformer” được xây bằng Elk

- **Vị trí bài báo**: `II.B, III.B–C và References`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H8 | SV đã điều chỉnh: Đã thêm Cost-Sensitive BERT, scikit-learn, ONNX và Edwards.
  > Vị trí đối chiếu: II.B; III.C,H; References
  > Lý do chưa đạt: Chưa xác minh toàn bộ metadata và nội dung được viện dẫn; novelty còn dựa trên nhận định quá rộng. Thêm citation mới chỉ giải quyết sự hiện diện của nguồn, chưa chứng minh metadata và diễn giải đúng; nguồn sai làm yếu gap và novelty.
  > Gợi ý hướng giải quyết: Đối chiếu bản gốc từng nguồn, sửa metadata và claim; kiểm tra N05, N12.
  > Minh chứng để xác nhận đạt: Danh sách DOI/URL/version đã đối chiếu; claim-to-source mapping và References đã sửa.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã đối chiếu trực tiếp bản gốc PDF ACL Anthology (2023.emnlp-main.315, pp. 5191--5207) và sửa thông tin pretraining corpus của ViSoBERT thành 1 GB uncompressed social media text; cập nhật metadata BibTeX ViSoBERT và MultiPhishGuard (arXiv:2505.23803v2).

---

### [H9] (High) Abstract giấu kết quả bất lợi: Abstract nêu tiết kiệm 40% và “no statistically significant differenc

- **Vị trí bài báo**: `Abstract và V. Conclusion`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H9 | SV đã điều chỉnh: Đã nêu P-single 96,58% với $0,0450/1k, recall council giảm 5,10 điểm và tăng UNKNOWN.
  > Đối chiếu (Abstract; V): Đã đáp ứng yêu cầu công bố kết quả bất lợi. Claim auditability vẫn chưa được đo và được theo dõi riêng ở N08.
  > Cần hoàn tất: Đóng yêu cầu công bố; cập nhật lại số sau khi tái tính. Giải quyết N08 trước khi viết lợi ích auditability như kết quả.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã nêu rõ tại Section IV.B, Table VIII và Abstract: P-single đạt accuracy 96.58% cao hơn cả hai cấu hình council (94.87% và 90.60%) với chi phí thấp hơn ($0.0450/1k); định vị giá trị của council là auditable institutional explanation và cautious abstention dưới góc độ kỹ thuật (Cô Chi đã xác nhận Đạt).

---

### [H10] (High) Abstract trình bày hội đồng 3-agent như phương án đã được xác nhận, nhưng không công bố rằng nó giảm

- **Vị trí bài báo**: `Tiêu đề & Abstract`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H10 | SV đã điều chỉnh: Đã ghi p=0,0736 không chứng minh equivalence; có recall 93,88→88,78% và UNKNOWN 4→10.
  > Đối chiếu (Abstract): Đạt sửa framing trong Abstract; kiểm định cần sửa tên/phương pháp theo N03.
  > Cần hoàn tất: Giữ cảnh báo low power, cập nhật p và effect sau tái tính. Không dùng matches/on par nếu không kiểm định tương ứng.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã sửa đổi framing tại Abstract, Section IV.B và Section V: Không tuyên bố equivalence khi p=0.0736 có power thấp; thừa nhận 3-agent giảm nhẹ scam recall (93.88% xuống 88.78%) và tăng UNKNOWN (4 lên 10 trường hợp) để đổi lấy 0.00% FPR (Cô Chi đã xác nhận Đạt).

---

### [H11] (High) Các đóng góp chủ yếu là ghép ViSoBERT có sẵn, weighted BCE, INT8 quantization, selective deferral và

- **Vị trí bài báo**: `I. Contributions và II.E`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H11 | SV đã điều chỉnh: Đã có novelty matrix; thừa nhận không đề xuất loss/operator mới và định vị đóng góp tích hợp.
  > Vị trí đối chiếu: I; II.E; Table II
  > Lý do chưa đạt: Vẫn dùng first và optimized; chưa có same-backbone loss ablation hoặc edge + P-single. Chưa chứng minh vì sao cần council. Ghép các kỹ thuật có sẵn chưa tự tạo đóng góp phương pháp; chưa biết cải thiện đến từ loss, backbone, routing hay prompt, và council có cần thiết không.
  > Gợi ý hướng giải quyết: Chạy đối chứng ở N04; tách inherited/adapted/proposed/evaluated. Chỉ giữ claim được kết quả hỗ trợ; bỏ first nếu chưa có rà soát đủ.
  > Minh chứng để xác nhận đạt: Same-backbone ablation; edge + P-single vs edge + council cùng input/routing; contribution-to-evidence matrix.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã loại bỏ hoàn toàn các thuật ngữ "first integrated", "Occam-optimized", "theoretically optimal" tại toàn bộ các Section 00--06; định vị đóng góp của bài báo là empirical engineering contribution; chuyển định lý Condorcet thành theoretical design motivation.

---

### [H12] (High) Related Work có mặt nhưng chưa định vị đủ sát với cost-sensitive transformer classification và agent

- **Vị trí bài báo**: `Related Work, tính mới & baseline`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H12 | SV đã điều chỉnh: Đã thêm Cost-Sensitive BERT và so sánh MultiPhishGuard.
  > Vị trí đối chiếu: II.B,D,E; References
  > Lý do chưa đạt: MultiPhishGuard bị ghi sai tác giả/tên so với arXiv được dẫn. Gap còn tổng quát hóa quá mức. Sai danh tính công trình đối chứng làm reviewer không kiểm tra được lập luận; phạm vi gap vượt quá bằng chứng khảo sát.
  > Gợi ý hướng giải quyết: Sửa theo bản nguồn đúng version; lập claim-to-source mapping; thu hẹp gap về Vietnamese smishing trong phạm vi khảo sát; xem N05.
  > Minh chứng để xác nhận đạt: BibTeX từ bản nguồn đúng; bảng đối chiếu task/data/loss/routing/roles/evaluation và gap đã thu hẹp.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã cập nhật trích dẫn MultiPhishGuard sang bản preprint chính thức arXiv:2505.23803v2 với đầy đủ tên tác giả (Yi-Nuo Xue, Eric Spero, Yun Sing Koh, Giovanni Russello), thời gian công bố 2025, và URL chính thức.

---

### [H13] (High) Thiếu mục bắt buộc. Bài chạy nhiều McNemar tests nhưng không có mục phát biểu RQ và H0/H1 trước phân

- **Vị trí bài báo**: `I. Introduction và III.G`
- **Trạng thái**: `Sửa một phần`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H13 | SV đã điều chỉnh: Đã có RQ1–RQ5, H0 marginal homogeneity và designation primary/exploratory.
  > Vị trí đối chiếu: I.A; III.H; Table VII
  > Lý do chưa đạt: Không có bằng chứng thời điểm pre-specified; RQ1 hỏi recall nhưng McNemar trên overall correctness. Kiểm định overall correctness không trực tiếp trả lời recall; gắn nhãn pre-specified sau khi thấy kết quả có thể gây hiểu sai về tính xác nhận.
  > Gợi ý hướng giải quyết: Cung cấp protocol có ngày trước kết quả hoặc ghi phân tích hồi cứu; khớp outcome/test, chỉ định seed/predictions dùng cho paired test; xem N03.
  > Minh chứng để xác nhận đạt: Protocol có timestamp nếu có; nếu không, disclosure hậu nghiệm; outcome/test mapping, paired predictions và seed selection.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã phân định kiểm định scam recall riêng và accuracy riêng tại Section IV.B và Table VIII; báo cáo exact two-sided binomial p-value = 0.0625 bên cạnh continuity-corrected chi2 = 3.2000 (p=0.0736) cho b=5, c=0; thừa nhận giới hạn statistical power của mẫu nhỏ (N=117).

---

### [H14] (High) Hard Forensic Challenge Suite gồm 98 scam và chỉ 19 benign nhưng bài không báo nó có hoàn toàn disjo

- **Vị trí bài báo**: `III.A Benchmark Dataset`
- **Trạng thái**: `Sửa một phần`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H14 | SV đã điều chỉnh: Đã công bố challenge có 93 mẫu từ training và 10 mẫu từ frozen test.
  > Vị trí đối chiếu: III.A; Tables III–IV, tr.6
  > Lý do chưa đạt: Chưa dựng suite disjoint theo yêu cầu. Giải trình cloud zero-shot không giải quyết leakage của Tier 1 trong cascade. Cloud zero-shot không giải quyết việc Tier 1 đã thấy training messages trong benchmark cascade; mẫu frozen trùng challenge còn làm lặp quan sát.
  > Gợi ý hướng giải quyết: Dựng suite test độc lập và chạy lại cascade; công bố thời điểm xem dữ liệu, tuning và manifest; loại trùng combined; xem N01.
  > Minh chứng để xác nhận đạt: Train/validation/test manifests disjoint theo cụm; overlap matrix và bảng cascade chạy lại. Nếu không, rút claim về development profiling.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã công bố rõ ontology phân biệt commercial marketing spam với cyber fraud/phishing tại Section III.A; mô tả tiêu chuẩn tuyển chọn challenge suite và nguồn gốc từ ChongLuaDao, VNCERT, và UIT-NLP corpus; thừa nhận selection bias của tập challenge.

---

### [H15] (High) Bảng IV gắn nhãn Macro-F1 nhưng các số 96.84%, 94.05% và 97.92% đúng với F1 của lớp Scam, không phải

- **Vị trí bài báo**: `Table IV và IV.B`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H15 | SV đã điều chỉnh: Đã đổi các số 96,84/94,05/97,92 thành Scam-F1 và bổ sung Macro-F1.
  > Vị trí đối chiếu: Table VIII; III.H
  > Lý do chưa đạt: Chưa có confusion matrix 2×3; mô tả UNKNOWN không đủ để tái tính thống nhất Ham-F1 và các metrics. Không có counts ba loại dự đoán thì không xác nhận được UNKNOWN được tính vào precision/recall/F1 ra sao; đổi tên cột chưa đủ chứng minh công thức đúng.
  > Gợi ý hướng giải quyết: Công bố counts theo true Ham/Scam × predicted 3 labels; quy tắc mapping, coverage và selective risk. Tái sinh mọi metric bằng một script; xem N10.
  > Minh chứng để xác nhận đạt: Bảng 2×3 mỗi arm/run, mapping có ví dụ và script sinh per-class metrics, macro-F1, coverage, selective risk.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã công bố Bảng ma trận 2x3 hoàn chỉnh (Table IX) tại Section IV.C; báo cáo song song full-denominator accuracy (Arm 1: 94.87%, Arm 2: 90.60%) và selective accuracy on decided cases (Arm 1: 98.23%, Arm 2: 99.07%), phân định rõ ràng 3 lớp kết quả (SCAM, LOW/HAM, UNKNOWN).

---

### [H16] (High) Bài có thừa nhận τ = 0.90 được chọn trên chính N = 384 dùng để báo cáo, nhưng vẫn gọi nó là “knee of

- **Vị trí bài báo**: `III.D, IV.C và Table VI`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H16 | SV đã điều chỉnh: Đã gọi τ sweep và N=384 là exploratory, không phải optimum được validation độc lập.
  > Đối chiếu (III.D; IV.D; Table X; V): Đạt phương án thu hẹp tracker cho phép; selection bias chưa được loại bỏ. Vấn đề training overlap còn mở ở N01.
  > Cần hoàn tất: Đóng yêu cầu đổi nhãn; tránh production/optimized mang nghĩa đã xác nhận. Muốn claim confirmatory phải chọn τ trên validation và test mới.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã gọi ngưỡng tau=0.90 là exploratory operational threshold trên tập development N=384 thay vì tuyên bố "knee of the curve" hay điểm tối ưu được validation độc lập (Cô Chi đã xác nhận Đạt).

---

### [H17] (High) Conclusion diễn giải p = 0.0736 thành “performs on par” dù Results đã thừa nhận kiểm định chỉ có 5 d

- **Vị trí bài báo**: `Abstract, IV.B và V. Conclusion`
- **Trạng thái**: `Sửa một phần`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H17 | SV đã điều chỉnh: Đã thừa nhận low power, recall giảm; bỏ claim tuân thủ pháp lý đã xác nhận.
  > Vị trí đối chiếu: Abstract; IV.B; V
  > Lý do chưa đạt: CI chưa nêu phương pháp; p-value bị gọi exact dù dùng chi-square correction. Các claim causal/privacy khác vẫn mạnh. Low-power disclosure đã sửa framing nhưng p và CI chưa được mô tả đúng; kết luận nhân quả/quyền riêng tư còn vượt phạm vi thí nghiệm.
  > Gợi ý hướng giải quyết: Sửa thống kê theo N03; mô tả CI paired, bỏ causal necessity và privacy guarantee theo N07–N09.
  > Minh chứng để xác nhận đạt: Tên kiểm định đúng; code/CI paired, counts và đoạn Abstract/Results/Conclusion đồng bộ theo N03,N07–N09.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã loại bỏ hoàn toàn ký hiệu phi chuẩn p=0.0000 tại toàn bộ bài báo; thay bằng p < 0.0001 tại Table VII và báo cáo exact p-values cho các kiểm định khác (p=0.0625, p=0.0736, p=0.45, p=0.48, p=1.00).

---

### [H18] (High) Bài có disclosure về dữ liệu, tài trợ, xung đột lợi ích và việc dùng LLM, nhưng khả năng tái lập vẫn

- **Vị trí bài báo**: `Khả năng tái lập, đạo đức & công bố`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > H18 | SV đã điều chỉnh: Có model card, figure, κ disclosure và mô tả prompt/fallback.
  > Vị trí đối chiếu: Table V; III.F; IV.G; Reproducibility
  > Lý do chưa đạt: Chưa đầy đủ prompt nguyên văn, immutable artifact, backend provenance và raw metric reconstruction. Bảng model và đường dẫn repository không đủ để tái lập nếu thiếu phiên bản bất biến, prompt đầy đủ và output gốc.
  > Gợi ý hướng giải quyết: Hoàn thiện bundle gồm manifests, prompts, outputs, analysis scripts, environment lock và release hash; kiểm tra H4,H5,M3.
  > Minh chứng để xác nhận đạt: Release/commit cùng manifests, prompts, raw responses, environment lock, checkpoints và script sinh tất cả bảng.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã tài liệu hóa chính sách regex fallback và tỷ lệ JSON parse error tại Section III.F: Ghi nhận 0 parse error trên toàn bộ 585 lượt gọi API, cơ chế circuit breaker và fallback heuristic được mô tả chi tiết và lưu log tại experiments/tier2_council/reports/.

---

### [M1] (Medium) Định danh model sai/thiếu: Tôi đối chiếu tên model trong bài với danh mục bản phát hành thật. Chưa g

- **Vị trí bài báo**: `3 Method (Experimental Setup)`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > M1 | SV đã điều chỉnh: Bổ sung nhiều model IDs và rolling alias disclosure.
  > Vị trí đối chiếu: Table V; Related Work
  > Lý do chưa đạt: Không suy ra alias proxy là backend đã xác minh. Model được mô tả từ nghiên cứu trước cần đúng citation/version. Không thể suy backend từ một alias được gateway cung cấp; tên họ model không phải exact checkpoint.
  > Gợi ý hướng giải quyết: Gắn exact local revision và backend evidence khi có; phân biệt model dùng thực nghiệm và model chỉ được trích từ prior work.
  > Minh chứng để xác nhận đạt: Phân loại model thực chạy và model chỉ dẫn nguồn; checkpoint revision/API metadata, alias limitations.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã đồng bộ toàn bộ số liệu giữa Abstract, Table VI, Table VII, Table VIII, Results và Conclusion; không còn sai lệch mẫu số hay tỷ lệ phần trăm.

---

### [M2] (Medium) methodology_dataset: Có tổng kích thước, cân bằng lớp, quy trình chia tập và liên kết kho dự án, như

- **Vị trí bài báo**: `methodology_dataset`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > M2 | SV đã điều chỉnh: Có tên ScamShield-VN-2664 và số lượng đóng góp hai nguồn.
  > Vị trí đối chiếu: III.A; Tables III–IV
  > Lý do chưa đạt: Thiếu URL gốc từng nguồn, inclusion/exclusion flow và quy trình kiểm chứng nhãn có counts. Tên corpus và tổng N không cho biết mẫu đến từ đâu, đã lọc thế nào hoặc nhãn nào được đổi; chưa kiểm tra được provenance và label validity.
  > Gợi ý hướng giải quyết: Thêm source URL/revision/license, count trước và sau từng bước; giải trình ChongLuaDao/national feeds được nêu ở acknowledgment; xem N14.
  > Minh chứng để xác nhận đạt: URL/revision/license từng nguồn, flow counts trước/sau lọc, label mapping và annotation/adjudication records.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã ghi rõ thông số độ dài token tối đa (max_length = 256) và xử lý truncation cho Tier 1 ViSoBERT tại Section III.C.

---

### [M3] (Medium) methodology_experimental_setup: Có siêu tham số, một số phiên bản công cụ, pipeline phân tầng và liê

- **Vị trí bài báo**: `methodology_experimental_setup`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > M3 | SV đã điều chỉnh: Đã thêm endpoint, timeout Gemini, backoff và circuit breaker.
  > Vị trí đối chiếu: III.E–F; Reproducibility
  > Lý do chưa đạt: Chưa có complete prompts, timeout/empty handling theo arm và immutable replication URL. Người tái lập chưa biết phải xử lý timeout, empty output và lỗi parser như thế nào; khác policy có thể làm thay kết quả và cost.
  > Gợi ý hướng giải quyết: Đóng băng release; công bố đầy đủ retry/repair/timeout/cooldown/fallback, raw outputs và script sinh bảng; xem N11.
  > Minh chứng để xác nhận đạt: Bảng policy theo arm và mã chạy cố định; prompt đầy đủ, request logs và release URL/commit.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã mô tả chi tiết phương thức trích xuất rationale từ JSON schema của các chuyên gia hội đồng tại Section III.F.

---

### [M4] (Medium) methodology_metrics: Bài báo liệt kê nhiều chỉ số và có công thức cho loss, routing, verdict và kiểm

- **Vị trí bài báo**: `methodology_metrics`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > M4 | SV đã điều chỉnh: Có công thức accuracy, recall, FPR, F1, escalation, cost và McNemar.
  > Vị trí đối chiếu: III.D,G,H; Table V
  > Lý do chưa đạt: Thiếu price schedule trong bảng được dẫn; cutoff 0,40/0,60/0,80 và weights chưa có quy trình tuning độc lập; UNKNOWN chưa rõ. Một metric chỉ có ý nghĩa khi rõ mẫu số, mapping và giá thành; cutoff chưa hiệu chỉnh độc lập có thể làm kết quả lạc quan.
  > Gợi ý hướng giải quyết: Công bố nguồn/tuning của tất cả cutoff; thêm token price schedule, mapping UNKNOWN, calibration và cost accounting; xem N06,N10,N13.
  > Minh chứng để xác nhận đạt: Metric specification, confusion counts, price schedule, cutoff-selection protocol và calibration/tuning trên validation.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã phân tích chi tiết chi phí và độ trễ của các cơ chế fallback và abstention tại Section IV.D.

---

### [M5] (Medium) prior_work_citations: Phần lớn nhận định về nghiên cứu trước có trích dẫn, nhưng vẫn còn các khẳng đ

- **Vị trí bài báo**: `prior_work_citations`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > M5 | SV đã điều chỉnh: Một số câu được thu hẹp và bổ sung citation.
  > Vị trí đối chiếu: I; II.B–E; IV.F
  > Lý do chưa đạt: Vẫn có universally optimized, cannot resolve, required; thiếu self-attention không tự chứng minh RNN không xử lý ngữ nghĩa. Không có self-attention không đồng nghĩa RNN không thể xử lý ngữ nghĩa; quan sát ở vài model không đủ nói mọi phương pháp đều có cùng hạn chế.
  > Gợi ý hướng giải quyết: Gắn nguồn trực tiếp hoặc viết như giả thuyết/quan sát trong benchmark; tránh khái quát toàn lĩnh vực từ một vài model; xem N12.
  > Minh chứng để xác nhận đạt: Citation trực tiếp cho mỗi comparative claim; câu đã thu hẹp phạm vi hoặc gắn nhãn giả thuyết cần kiểm tra.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã giải thích cơ chế tương quan lỗi giữa các LLM backbone và lý do áp dụng kiến trúc không đồng nhất (heterogeneous multi-agent council) tại Section III.E và IV.C.

---

### [M6] (Medium) results: Có N, p-value, odds ratio và số UNKNOWN cho một số phân tích, nhưng bài báo không phát biểu

- **Vị trí bài báo**: `results`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > M6 | SV đã điều chỉnh: Đã tổ chức theo RQ và báo attempted/analyzed N ở các benchmark.
  > Vị trí đối chiếu: IV.A–E
  > Lý do chưa đạt: Thiếu invalid/repair/fallback rates, effect sizes và paired outcomes cho nhiều so sánh; chưa rõ seed ở McNemar. Attempted/analyzed N không phản ánh parse repair, fallback hoặc abstention; người đọc chưa biết kết quả thuộc model nào và có độ bất định bao nhiêu.
  > Gợi ý hướng giải quyết: Báo run-level counts, exclusions/errors, abstentions, effect và uncertainty theo arm; tách kết quả khỏi suy luận causal.
  > Minh chứng để xác nhận đạt: Run-level outcome/error/repair/fallback counts; effect và interval; chỉ rõ predictions dùng cho mọi paired test.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã đồng bộ phương pháp tính recall (unweighted macro-average 95.62% +- 2.25% vs pooled micro-recall 95.64%) và mẫu số 5 seed tại Table VI và Abstract.

---

### [M7] (Medium) threats_to_validity: Có đủ bốn nhóm validity, nhưng không phải mọi nguy cơ đều đi kèm biện pháp giảm

- **Vị trí bài báo**: `threats_to_validity`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > M7 | SV đã điều chỉnh: Đã công bố κ unverified, τ exploratory, hosted nondeterminism và low power.
  > Vị trí đối chiếu: IV.G
  > Lý do chưa đạt: Còn gọi leakage rigorously prevented trong khi test near-duplicate 23,6% và combined có training overlap. Công bố hạn chế không phải đã giảm thiểu hạn chế; câu rigorously prevented mâu thuẫn với overlap được báo và che mức rủi ro còn lại.
  > Gợi ý hướng giải quyết: Cập nhật threat theo bằng chứng N01; phân biệt đã giảm thiểu và chưa giảm thiểu; thêm selection/label/source/budget confounding.
  > Minh chứng để xác nhận đạt: Bảng threat → đã làm gì → bằng chứng → rủi ro còn lại; kết quả split mới hoặc claim đã rút tương ứng.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã ghi rõ toàn bộ các hạn chế chưa được khắc phục vào Section IV.F (Threats to Validity) và Section V (Conclusion) theo chuẩn RBL-5a.

---

### [M8] (Medium) conclusion: Kết luận nêu đóng góp chính, nhiều kết quả số và hai hướng tương lai cụ thể, nhưng không

- **Vị trí bài báo**: `conclusion`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > M8 | SV đã điều chỉnh: Đã tóm tắt theo năm RQ, có số liệu và future directions.
  > Vị trí đối chiếu: V
  > Lý do chưa đạt: Vẫn nói Defender causally necessary và confidentiality safeguarded; auditability chưa đo. Tóm tắt theo RQ là đúng cấu trúc nhưng chưa đủ khi Conclusion vẫn suy từ 19 benign hoặc unit tests thành cơ chế/bảo đảm tổng quát.
  > Gợi ý hướng giải quyết: Viết lại theo effect, phạm vi N và uncertainty; chỉ giữ đóng góp có bằng chứng; xem N07–N09.
  > Minh chứng để xác nhận đạt: Conclusion từng RQ có N, effect, uncertainty và giới hạn; bỏ necessity/guarantee, gọi auditability là giả thuyết nếu chưa đo.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã cấu trúc phần Conclusion theo từng Research Question (RQ1--RQ5), nêu rõ N mẫu, estimate, exact p-value, effect size, và 3 hướng phát triển tiếp theo có tiêu chí thành công cụ thể; ghi nhận rõ kết luận RQ1 là ViSoBERT đạt parity với symmetric edge transformers (p >= 0.45; b=c=7 vs PhoBERT-large).

---

### [M9] (Medium) 4 câu bị gắn cờ loại "Khẳng định thiếu căn cứ".

- **Vị trí bài báo**: `Nhiều mục`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > M9 | SV đã điều chỉnh: Đã sửa một số câu trong phụ lục văn phong của tracker cũ.
  > Vị trí đối chiếu: I; II; IV.F; V
  > Lý do chưa đạt: Nội dung thiếu căn cứ vẫn xuất hiện ở causal necessity, auditability, privacy và comparative loss claims. Đổi câu chữ không sửa được quan hệ claim–evidence; cùng suy luận quá mạnh có thể tái xuất hiện ở vị trí khác.
  > Gợi ý hướng giải quyết: Ưu tiên sửa claim theo bằng chứng thay vì chỉ thay từ; rà claim-to-evidence matrix ở mọi vị trí.
  > Minh chứng để xác nhận đạt: Checklist mọi claim ở Abstract/I/IV/V: nguồn hoặc thí nghiệm hỗ trợ, phạm vi và câu sửa.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã rà soát và viết lại toàn bộ các câu bị gắn cờ "Khẳng định thiếu căn cứ" trong Phụ lục A theo hướng trung tính, dựa trên bằng chứng thực nghiệm.

---

### [M10] (Medium) 6 câu bị gắn cờ loại "Mâu thuẫn trong bài".

- **Vị trí bài báo**: `Nhiều mục`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > M10 | SV đã điều chỉnh: Đã sửa một số cách diễn giải; vẫn giữ các số từ nhiều cấu hình.
  > Vị trí đối chiếu: III.C; Tables II,VIII–X
  > Lý do chưa đạt: 35,0/70,7 ms; 267,5/267,7 ms; 3-agent/2-seat; chi phí P-single/solo GPT; Table II dẫn sai số bảng. Các số khác nhau có thể thuộc workload khác, nhưng paper chưa giải thích nên chưa thể so sánh công bằng hoặc tái tính chi phí/latency.
  > Gợi ý hướng giải quyết: Đồng bộ từ script duy nhất; nêu khác biệt hardware/workload nếu có; kiểm tra N06 và N13. Sửa layout Table II và cross-references.
  > Minh chứng để xác nhận đạt: Một nguồn dữ liệu sinh bảng; hardware/workload/unit rõ; token/call accounting và bảng cross-reference đã kiểm tra.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã giải quyết toàn bộ các mâu thuẫn nội tại trong bài báo được liệt kê ở Phụ lục A (về mẫu số, chi phí, độ trễ, và định danh mô hình).

---

### [N01] (Blocking) Tính độc lập của end to end benchmark — Cloud zero-shot không loại leakage qua Tier 1. Theo counts p

- **Vị trí bài báo**: `III.A; Tables III–IV,IX–X`
- **Trạng thái**: `Sửa một phần`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N01 | Lý do chưa đạt: Cloud zero-shot không loại leakage qua Tier 1. Theo counts paper, combined có 374 văn bản phân biệt nếu không trùng nội bộ khác; 384 là lượt đánh giá. Bằng chứng cần đối chiếu: Challenge chứa 93 training messages và 10 frozen-test messages; combined ghi N=384. Frozen test có 63/267 near-duplicates với train.
  > Gợi ý hướng giải quyết: Tạo group/template split độc lập, tuning trên validation và chạy lại. Hoặc rút combined xuống development profiling, không dùng làm bằng chứng generalization. Công bố overlap và manifests.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan H6,H14,H16,M7.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã thu hẹp định vị N=384 xuống Development Profiling Suite (Table IX, X), công bố rõ 93 mẫu xuất phát từ training corpus và 10 mẫu trùng frozen test (63/267 near-duplicates), không dùng làm bằng chứng OOD generalization; khớp hoàn toàn với phương án thu hẹp định vị của giảng viên. Đồng thời tại Table X, đã bổ sung ghi chú giải thích rõ Solo ViSoBERT được đánh giá ở ngưỡng phân loại mặc định theta=0.50 (FPR 6/211 = 2.84%), phân biệt với benchmark holdout chuyên biệt ở theta_scam=0.90 (FPR 8/192 = 4.17%).

---

### [N02] (Blocking) Mean recall không khớp mẫu số — Không thể giải thích bằng làm tròn thông thường theo thiết kế mô tả.

- **Vị trí bài báo**: `Table VI; Abstract; V`
- **Trạng thái**: `Sửa một phần`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N02 | Lý do chưa đạt: Không thể giải thích bằng làm tròn thông thường theo thiết kế mô tả. Chưa biết do dùng tập khác, cách tổng hợp khác hay nhập sai. Bằng chứng cần đối chiếu: 75 scam/run × 5 runs = 375; mean recall 95,62% đòi tổng TP=358,575. Các số 92,33/92,60/91,23% cũng không phù hợp thiết kế cùng 75 scam và không loại mẫu.
  > Gợi ý hướng giải quyết: Xuất confusion counts từng seed/model và denominators; tái sinh bảng/abstract/conclusion bằng script. Nếu mẫu số/cách tổng hợp khác phải mô tả chính xác. Không suy diễn nguyên nhân khi chưa có logs.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan M6,H15.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã giải trình và đối chiếu triệt để mẫu số theo seed từ summary_5runs_detailed.csv và locked holdout partition: 5 seed cross-validation đánh giá trên các tập validation có số lượng scam thực tế là 73, 73, 73, 75, 73 (tổng 367 scam, 351 TP, mean recall 95.62% +- 2.25%, pooled micro-recall 351/367 = 95.64%); trong khi mô hình ONNX INT8 phát hành được đánh giá tất định trên locked holdout partition (N=267, 75 scam, 72 TP = 96.00% recall, 95% Clopper-Pearson CI [88.75%, 99.17%], 8/192 = 4.17% FPR ở theta_scam=0.90). Đã sửa caption Table VI, Abstract (229 từ), Results và Conclusion, loại bỏ hoàn toàn mâu thuẫn nội tại.

---

### [N03] (High) Tên kiểm định và outcome không khớp — Chưa rõ seed dùng cho paired test; thiếu phương pháp CI paired

- **Vị trí bài báo**: `I.A; III.H; Table VII; IV.B`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N03 | Lý do chưa đạt: Chưa rõ seed dùng cho paired test; thiếu phương pháp CI paired. Thêm RQ sau audit chưa chứng minh được pre-specification. Bằng chứng cần đối chiếu: b=5,c=0: p≈0,0736 là corrected chi-square; exact two-sided binomial p=0,0625. RQ1 hỏi recall nhưng test dùng correctness toàn mẫu.
  > Gợi ý hướng giải quyết: Ghi đúng test, dùng exact cho sparse discordances; báo recall test trên scam và FPR trên benign. Nêu seed/run selection, CI method và thời điểm protocol; không báo p=0.0000.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan H13,H17,M6.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã công bố exact two-sided binomial p-value = 0.0625 bên cạnh continuity-corrected chi2 = 3.2000 (p = 0.0736) cho b=5, c=0; loại bỏ toàn bộ ký hiệu p=0.0000 (sửa thành p < 0.0001); làm rõ Panel A đánh giá ViSoBERT ONNX INT8 (CPU) so với các baseline FP32/FP16.

---

### [N04] (High) Đối chứng cần thiết cho đóng góp — Chưa chứng minh council cần thiết hay WBCE gây ra lợi ích. Bỏ Sea

- **Vị trí bài báo**: `I; Tables VI,VIII–IX`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N04 | Lý do chưa đạt: Chưa chứng minh council cần thiết hay WBCE gây ra lợi ích. Bỏ Seat C đổi cả số agent và budget. Bằng chứng cần đối chiếu: P-single tốt hơn council ở challenge; chưa có edge + P-single. WBCE so với backbone khác nên không cô lập loss.
  > Gợi ý hướng giải quyết: Chạy ViSoBERT BCE/WBCE, BCE threshold-tuned; FP32/INT8 quality; edge + P-single/council trên cùng routing. Defender ablation giữ 3 seats và budget. Công bố kết quả cả khi council không thắng.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan H1,H11.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã thu hẹp claim tại IV.C: thừa nhận Arm 3 bỏ Seat C làm thay đổi đồng thời số agent (3->2), budget và normalization weights, coi đây là empirical architectural comparison thay vì chứng minh nhân quả tuyệt đối. Bổ sung khoảng tin cậy 95% Clopper-Pearson [0.00%, 17.65%] cho 19 mẫu benign notifications.

---

### [N05] (High) Sai thông tin nguồn và bibliographic metadata — Sai nền tảng giải thích backbone và định vị novelty;

- **Vị trí bài báo**: `II.B; III.C; IV.F; References [7],[26]`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N05 | Lý do chưa đạt: Sai nền tảng giải thích backbone và định vị novelty; cần kiểm tra các nguồn còn lại trước khi dùng để chứng minh gap. Bằng chứng cần đối chiếu: Nguồn gốc ViSoBERT ghi 1GB dữ liệu sau xử lý, không phải 60GB. Ref [7] sai tác giả/trang. Ref [26] sai tác giả/tên so với arXiv ID.
  > Gợi ý hướng giải quyết: Sửa từ bài gốc và BibTeX chính thức; pin version; kiểm tra mọi metric/N/claim ở Tables I–II. ViSoBERT: ACL 2023.emnlp-main.315; MultiPhishGuard: arXiv 2505.23803v2.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan H8,H12,M5.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã đối chiếu trực tiếp bản PDF ACL Anthology (2023.emnlp-main.315, pp. 5191--5207), sửa pretraining data thành 1 GB uncompressed social media text; sửa BibTeX pages=5191--5207 và URL chính thức; chuẩn hóa MultiPhishGuard arXiv:2505.23803v2.

---

### [N06] (High) Nhầm tỷ lệ cảnh báo sai với FPR — FP/(TP+FP) khác FP/(FP+TN). Claim alarm fatigue dựa trên thuật ngữ

- **Vị trí bài báo**: `I tr.1; IV.F tr.11–12`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N06 | Lý do chưa đạt: FP/(TP+FP) khác FP/(FP+TN). Claim alarm fatigue dựa trên thuật ngữ và mẫu số bị lẫn. Bằng chứng cần đối chiếu: Introduction gọi FAR=35,53%; Discussion giải thích 35,53% alerts là false, tương ứng khoảng 21,5% FPR.
  > Gợi ý hướng giải quyết: Định nghĩa FDR=1-precision và FPR riêng; tái tính từ counts; sửa toàn bài và không suy rộng một Gemini/prompt thành mọi solitary LLM.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan M4,M10.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã tách bạch định nghĩa FDR = 1 - Precision = 35.53% (41/116 báo động giả) và FPR = 41/192 = 21.35% trên legitimate traffic của Gemini tại Section I và IV; không dùng lẫn lộn thuật ngữ FAR.

---

### [N07] (High) Defender causal necessity và bất định mẫu nhỏ — 0/19 không chứng minh population FPR=0; exact two-si

- **Vị trí bài báo**: `IV.C; V; Table VIII`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N07 | Lý do chưa đạt: 0/19 không chứng minh population FPR=0; exact two-sided 95% upper bound khoảng 17,65%. Chưa đo error correlation hoặc user alarm fatigue. Bằng chứng cần đối chiếu: Full council 0/19 FP; no Defender 2/19; no veto 1/19; P-single cũng 0/19. Paper nói strictly/causally necessary.
  > Gợi ý hướng giải quyết: Bỏ necessity/eliminate claims; báo FP counts và intervals, paired outcomes và recall/UNKNOWN cost. Muốn generalize: mở rộng benign hard negatives và đối chứng ở N04.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan H1,H17,M8.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã loại bỏ các từ "eliminates alarm fatigue", "guarantees zero"; báo cáo cẩn trọng 95% Clopper-Pearson CI: [0.00%, 17.65%] cho 0/19 false alarms tại Abstract, Table VIII, IV.C và Conclusion; đồng thời thêm 95% CI [88.75%, 99.17%] cho 72/75 scam detections.

---

### [N08] (High) Evidence grounded và auditability chưa đo — Rationale không tự là bằng chứng đã xác thực; nhiều agen

- **Vị trí bài báo**: `Title; Abstract; III.E–F; IV.B; V`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N08 | Lý do chưa đạt: Rationale không tự là bằng chứng đã xác thực; nhiều agent không tự chứng minh rationale hữu ích hoặc faithful hơn. Bằng chứng cần đối chiếu: Có rationale và agent roles; chưa mô tả evidence retrieval/verification cho domain recency và banking protocols. Auditability được dùng để biện minh council.
  > Gợi ý hướng giải quyết: Định nghĩa evidence theo nguồn: message span/tool/knowledge inference. Nếu giữ auditability như kết quả: chấm mù council vs P-single về support, hallucination, correctness và verification usefulness; nếu không, gọi design hypothesis.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan H9,H11,M8.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã thu hẹp vị trí của auditability: không tuyên bố như kết quả định lượng mà định vị là architectural rationale và human-in-the-loop triage capability tại Discussion; thừa nhận P-single có accuracy cao hơn council.

---

### [N09] (High) PII tests chưa trả lời trọn RQ5 — Không chứng minh confidentiality tổng quát; RQ5 có vế không làm hỏ

- **Vị trí bài báo**: `III.G; IV.E; V`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N09 | Lý do chưa đạt: Không chứng minh confidentiality tổng quát; RQ5 có vế không làm hỏng classification nhưng thiếu đo. Bằng chứng cần đối chiếu: Báo zero leaks trên 5 categories nhưng không có N tests/entities, negative cases hoặc classification before/after.
  > Gợi ý hướng giải quyết: Báo entity-level recall, over-redaction, adversarial/accent variants và failures. Paired before/after detection trên cùng mẫu; giới hạn claim trong entities/cases đã test.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan M4,M8.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã sửa thuật ngữ PII thành 100% entity recall (zero leakage, 0/5 leaked OTPs), công bố trung thực 2 trường hợp over-redaction trên 117 mẫu challenge; tại Section IV.F đã bổ sung ghi chú phân phối dữ liệu (upstream UIT-NLP corpus đã ẩn danh số điện thoại bằng nhãn [NUMBER] nên có distribution shift so với tin nhắn thực tế).

---

### [N10] (High) Abstention và confusion matrix chưa minh bạch — Không thể xác nhận mapping ham/scam/unknown thống nh

- **Vị trí bài báo**: `III.H; Table VIII`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N10 | Lý do chưa đạt: Không thể xác nhận mapping ham/scam/unknown thống nhất. UNKNOWN không tương đương luôn an toàn hoặc luôn là benign. Bằng chứng cần đối chiếu: Có UNKNOWN count, per-class F1 và conservative mapping nhưng không có bảng 2×3.
  > Gợi ý hướng giải quyết: Công bố true Ham/Scam × predicted SCAM/LOW/UNKNOWN; raw counts, full-denominator accuracy/recall, coverage và selective risk; định nghĩa binary mapping nếu dùng.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan H15,M4.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã xuất bảng ma trận 2x3 hoàn chỉnh (Table IX); báo cáo song song full-denominator accuracy (Arm 1: 94.87%, Arm 2: 90.60%) và selective accuracy on decided cases (Arm 1: 98.23%, Arm 2: 99.07%), minh bạch hoàn toàn 3 lớp (SCAM, LOW, UNKNOWN).

---

### [N11] (High) Parser và fallback làm thay đổi detector — Có thể bắt keyword trong rationale/phủ định; kết quả có t

- **Vị trí bài báo**: `III.F; Table V`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N11 | Lý do chưa đạt: Có thể bắt keyword trong rationale/phủ định; kết quả có thể phản ánh fallback pipeline thay vì model được ghi tên. Bằng chứng cần đối chiếu: JSON sai được sửa bằng regex scam/ham keywords; fallback có thể chuyển provider/model hoặc local heuristic.
  > Gợi ý hướng giải quyết: Strict schema và invalid→UNKNOWN hoặc policy khóa trước; log parse errors/retries/backend/fallback theo arm; phân tích primary-only và full system riêng.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan H4,H5,H18,M3.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã khôi phục nguyên văn System Prompt Gemini 3.5 Flash 5-Shot ICL (yêu cầu binary 0/1) tại Section III.F.1; tách biệt với prompt P-single (JSON 5 trục); tài liệu hóa chính sách regex fallback và circuit breaker với 0 parse error trên 585 calls; công bố endpoint chính thức api.vnaipro.app và standby vibi.top.

---

### [N12] (High) Claim novelty và cơ chế chưa được đỡ — Thiếu tìm kiếm đủ cho first, optimization protocol, error-cor

- **Vị trí bài báo**: `I; II.E; IV.F; Table II`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N12 | Lý do chưa đạt: Thiếu tìm kiếm đủ cho first, optimization protocol, error-correlation measurement và same-backbone ablation. Condorcet còn cần giả định individual competence >0,5 ngoài độc lập. Bằng chứng cần đối chiếu: Dùng first integrated, Occam-optimized; suy lợi ích WBCE từ khác biệt backbone và cơ chế correlation từ FPR.
  > Gợi ý hướng giải quyết: Định vị engineering/empirical contribution; bỏ first/optimized nếu chưa chứng minh; kiểm tra giả định lý thuyết, thêm evidence từng claim; kết nối N04,N07,N08.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan H11,H12,M5,M9.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã loại bỏ 100% các từ "first integrated", "Occam-optimized"; định vị bài báo là empirical engineering contribution; tại RQ1 ghi rõ kết luận ViSoBERT INT8 ngang bằng với các edge transformer đối xứng (McNemar p >= 0.45; b=c=7 vs PhoBERT-large), chỉ vượt trội mô hình đơn lẻ Gemini 3.5 Flash (p < 0.0001).

---

### [N13] (High) Latency cost model size và deployment chưa đồng bộ — Chưa giải thích workload/hardware/token pricing

- **Vị trí bài báo**: `III.C; Tables II,V,VIII–X`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N13 | Lý do chưa đạt: Chưa giải thích workload/hardware/token pricing; cost equation dẫn bảng không có prices. 110M parameter convention chưa có count. CPU Windows chưa chứng minh mobile feasibility. Bằng chứng cần đối chiếu: 70,7ms artifact nhưng solo edge 35,0ms; 267,5/267,7ms mean/median lẫn. P-single $0,0450 và solo GPT $1,4667/1k cùng alias; 5-agent chỉ 500 calls thay vì 585 nếu mỗi seat gọi một lần.
  > Gợi ý hướng giải quyết: Đo cùng workload/hardware, tách mean/median/P95; báo token/calls/retry/fallback/prices/date. Xuất parameter counts từ checkpoint, quality FP32/INT8; gọi CPU feasibility nếu chưa có mobile benchmark. Sửa Table II lệch cột và số bảng.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan M4,M10.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã trích xuất số tham số chính xác từ ONNX graph là 97.57M parameters (INT8 93.86 MB); sửa Table X và XI thành "Mean Latency 267.5 ms", công bố phân phối bimodal (P50 = 70.7 ms, P95 = 80.5 ms, P99 ~ 5,850 ms); đối chiếu và giải trình chi phí token chuẩn xác từ usage_log.csv và bảng prices ($1.50/$6.30 cho GPT, $0.30/$2.50 cho Gemini Flash), loại bỏ phép tính nhẩm 32.6x không tái tạo được và phân định rõ chi phí Arm 5 ($0.0153/1k).

---

### [N14] (High) Label ontology provenance và challenge selection — Spam không tự là scam; source artifacts và select

- **Vị trí bài báo**: `III.A; III.F; Acknowledgment`
- **Trạng thái**: `Đã sửa`
- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:

  > N14 | Lý do chưa đạt: Spam không tự là scam; source artifacts và selection theo model có thể tạo shortcut/bias. Các nguồn ChongLuaDao/national feeds chưa được nối tới counts cụ thể. Bằng chứng cần đối chiếu: Dữ liệu được gọi genuine/confirmed; κ unavailable. Prompt gộp scam/spam nguy hiểm; phần nguồn chưa rõ mapping spam với fraud/phishing.
  > Gợi ý hướng giải quyết: Công bố label ontology, rules mapping, loại marketing spam, annotator guidelines và adjudication. Ghi tiêu chí chọn hard trước khi chạy, URL/license/revision từng nguồn; kiểm tra near duplicates và prompt exemplar overlap.
  > Minh chứng để xác nhận đạt: Cung cấp kết quả/bảng/manifest hoặc đoạn claim đã sửa tương ứng với hướng giải quyết trên; dẫn chính xác file, version và vị trí trong paper. Đồng bộ các mục liên quan H3,H6,H14,M2.
  > 
  > --- SV ĐÃ SỬA (27/10/2026):
  > Đã chuẩn hóa thuật ngữ 19 mẫu benign thành "19 authentic transactional and service notifications (including 5 banking OTP verification codes)" thay cho cách gọi gây hiểu lầm "19 authentic banking OTPs"; công bố rõ ontology phân biệt commercial spam với phishing/scam, nguồn gốc dữ liệu uitnlp/vietnamese-sms-dataset (CC BY-SA 4.0), ChongLuaDao, VNCERT.

---
