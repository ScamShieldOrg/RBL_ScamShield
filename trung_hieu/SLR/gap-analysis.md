# GAP Analysis — Nghịch Lý Đánh Đổi Độ Chính Xác – Độ Trễ – Chi Phí (Accuracy-Latency-Cost Trilemma) & Tối Ưu Hóa AI 2 Tầng Cascaded

**Thành viên:** Nguyễn Trung Hiếu (`trung_hieu`)  
**GAP type:** GAP-T (Technological & Architecture) / GAP-M (Methodological)  
**Ngày:** 2026-08-31  
**Evidence table nguồn:** `team-synthesis/evidence-table-merged.md`  
**N =** 11 bài báo core (5 bài cơ sở: `M023`, `M039`, `M040`, `M041`, `M042` + 6 bài Hội đồng Pháp y Tầng 2: `M043`, `M044`, `M045`, `M046`, `M047`, `M048`)

---

## 1. Mô tả GAP

Hiện nay, chưa có nghiên cứu nào thiết kế và đánh giá thực nghiệm một **Kiến trúc AI 2 Tầng Phân Cấp (2-Tier Cascaded AI Framework)** kết hợp mô hình ngôn ngữ tiền huấn luyện nhỏ gọn cục bộ trên CPU (Fast-Path Local PLM) và Mô hình Ngôn ngữ Lớn trên Đám mây (Cloud LLM Reasoning Fallback) nhằm giải quyết triệt để nghịch lý đánh đổi giữa **Độ chính xác (Accuracy)**, **Độ trễ thời gian thực (Inference Latency < 250ms)** và **Chi phí vận hành API (Operational Cost)** trong bài toán phát hiện tin nhắn lừa đảo.

**Bằng chứng từ evidence table:**
*   **Cột Phương pháp luận & Kiến trúc (Tool / LLM):** Các nghiên cứu hiện tại bị phân cực cực đoan thành 2 thái cực:
    1.  *Thái cực LLM đám mây nặng (`M040`)*: Đánh giá 9 mô hình Generative AI lớn (GPT-4, Claude, LLaMA) cho khả năng tổng quát hóa tốt trên các chiêu trò lừa đảo mới, nhưng phụ thuộc hoàn toàn vào API đám mây.
    2.  *Thái cực mô hình nhẹ cục bộ (`M023`, `M039`, `M041`, `M042`)*: Đánh giá các mô hình đơn lẻ như BiGRU, TF-IDF+LR, MacBERT-BiLSTM, DistilBERT chạy độc lập.
*   **Cột Kết quả thực nghiệm (Empirical Results) & Độ trễ:** 
    *   Bài báo `M041` *(HC Phap, 2026)* chứng minh mô hình Edge-AI (BiGRU+MaskedPool) đạt độ trễ CPU siêu nhanh **0.25 ms** với kích thước bộ nhớ chỉ **5.21 MB**, trong khi DistilBERT mất **40.78 ms** (256 MB) và các LLM lớn (`M040`, `M032`) mất tới **13.000 – 15.000 ms** (13–15 giây) kèm chi phí token đắt đỏ ($0.002 – $0.01/call).
    *   Tuy nhiên, `M041` và `M023` thừa nhận các mô hình nhẹ bị suy giảm độ chính xác và khả năng phân biệt ngữ cảnh sâu khi kẻ lừa đảo sử dụng các kịch bản thao túng tâm lý phức tạp.
*   **Cột Hạn chế (Limitations & Threats to Validity):** 
    *   `M041` chỉ rõ: *"Chi phí tính toán của Transformer cản trở việc suy luận liên tục trên thiết bị; cần hiệu chuẩn ngưỡng phạt lỗi vận hành"*.
    *   `M042` chỉ rõ: *"Mô hình MacBERT-BiLSTM thiếu tri thức mở rộng bên ngoài và không có cơ chế tối ưu độ trễ cho môi trường thực tế"*.
    *   `M023` ghi nhận: *"Sự đánh đổi thực tế giữa độ phức tạp mô hình, khả năng diễn giải và hiệu năng trong các kịch bản bị giới hạn tài nguyên"*.
    *   **Khoảng trống xuất hiện:** Không có bất kỳ công trình nào trong 5 paper đề xuất cơ chế định tuyến thông minh (Confidence-based Routing Trigger) để kết hợp ưu điểm tốc độ của mô hình nhẹ với khả năng suy luận sâu của LLM.

---

## 2. Kiểm tra phản chứng

| Paper | Đã làm GAP này không? | Chi tiết |
| :--- | :--- | :--- |
| **M023** *(Xie, 2025)* | Không | So sánh KNN, Logistic Regression, Random Forest và fine-tuned BERT độc lập trên tập dữ liệu tin nhắn lừa đảo. Tác giả đánh giá từng mô hình riêng lẻ, không xây dựng cơ chế phối hợp cascaded 2 tầng để tối ưu độ trễ/chi phí. |
| **M039** *(Jiang et al., 2026)* | Không | Đề xuất kiến trúc lai BERT-BiLSTM-EAA kết hợp cơ chế Attention tăng cường. Mô hình chạy như một khối monolithic duy nhất, không có cơ chế phân tầng suy luận cục bộ/đám mây. |
| **M040** *(Topcuoglu et al., 2026)* | Không | Khảo sát 9 mô hình Generative AI lớn và fine-tuned BERT để phát hiện lừa đảo. Nghiên cứu chỉ đo lường hiệu năng phát hiện đơn lẻ của từng LLM qua prompt, không giải quyết bài toán độ trễ di động hay tối ưu chi phí API qua kiến trúc phân tầng. |
| **M041** *(HC Phap, 2026)* | Có (một phần) | Nghiên cứu chuyên sâu về tối ưu hóa Edge-AI cho phát hiện Smishing bằng kiến trúc BiGRU+MaskedPool+WBCE (đạt 0.25 ms CPU latency, 5.21 MB). Tuy nhiên, tác giả chỉ dừng lại ở mô hình Edge đơn lẻ, không tích hợp tầng Fallback LLM đám mây để cứu các ca khó có độ tự tin thấp (<90%). |
| **M042** *(Chen & Chen, 2024)* | Không | Đề xuất mô hình MacBERT kết hợp BiLSTM và Enhanced Attention (BERT-BiLSTM-EAA). Nghiên cứu chỉ tập trung nâng cao F1-score (đạt 85.18%), hoàn toàn không khảo sát chi phí tính toán, thời gian suy luận hay kiến trúc cascaded. |

**Kết luận:** **GAP 2 ĐƯỢC XÁC NHẬN** (Không có bài báo nào trong 5 paper giải quyết bài toán tối ưu hóa đồng thời Accuracy - Latency - Cost thông qua kiến trúc AI 2 tầng Cascaded).

---

### Supplementary Validation (Vì N = 5 < 10)

| Lớp | Hành động | Kết quả |
| :--- | :--- | :--- |
| **L1 Targeted search** | Query: `("cascaded" OR "two-tier" OR "hierarchical") AND ("scam detection" OR "smishing") AND ("LLM" OR "PhoBERT")` trên Google Scholar & IEEE Xplore (2026-08-31) | **8 kết quả**, 0 phản chứng (các bài báo chỉ nói về mạng nơ-ron phân tầng cổ điển hoặc phân loại ảnh, không có kiến trúc cascaded kết hợp Fast-Path CPU PLM + Cloud LLM cho SMS/Scam). |
| **L2 Forward snowball** | Dùng `M041` *(HC Phap, 2026, J. Inf. Telecommun.)* làm anchor paper, kiểm tra các nghiên cứu trích dẫn mới nhất | **0 GAP / 0 phản chứng** (các bài trích dẫn chỉ mở rộng sang tập dữ liệu mạng 5G hoặc IoT traffic, không làm kiến trúc 2-tier hybrid cascade). |
| **L3 Survey anchor** | Đối chiếu bài SLR của *Saias (2025, ACM Computing Surveys - M004)* tổng hợp N=30 paper về NLP cho An toàn thông tin | Khảo sát ghi nhận sự phân mảnh giữa mô hình nhẹ (Lightweight ML) và LLM lớn, **hoàn toàn chưa có công trình nào tích hợp cơ chế định tuyến tin cậy (Confidence Routing) kết hợp cả hai**. |

→ **Kết luận:** **GAP 2 CONFIRMED** qua cả 3 lớp kiểm tra bổ sung.

---

## 3. Feasibility Check

| Tiêu chí | Mức | Ghi chú |
| :--- | :---: | :--- |
| **Dataset** | 🟢 | Sử dụng tập dữ liệu chuẩn hóa kết hợp từ `M041` (UCI, LSDST-2022) và bộ dữ liệu tiếng Việt `Scam-VN-SMS` ($\ge 500$ mẫu) của nhóm. Đã có sẵn nhãn ground truth. |
| **API / Tool** | 🟢 | Tầng 1 dùng PhoBERT-base mã nguồn mở (0đ chi phí). Tầng 2 dùng Gemini 2.0 Flash / GPT-4o-mini qua API (nhờ Tầng 1 lọc 80% lưu lượng nên chi phí API $\le \$2$ tổng cho toàn bộ bài đo). |
| **Tính toán** | 🟢 | Tầng 1 (PhoBERT CPU Inference) chạy trực tiếp trên laptop/server tiêu chuẩn (CPU Intel i5/i7) với RAM < 500MB. Huấn luyện fine-tune PhoBERT chỉ cần Google Colab T4 miễn phí. |
| **Ground truth** | 🟢 | Nhãn nhị phân (`scam` vs `ham`) và đa nhãn taxonomy đã được xác thực, không tốn thêm thời gian gán nhãn thủ công. |
| **Code base** | 🟢 | Thư viện Transformers (HuggingFace), PyTorch, FastAPI, và mã nguồn mở `BiGRU+WBCE` từ tác giả bài `M041` có sẵn trên GitHub để kế thừa. |
| **Kỹ năng** | 🟢 | Đã làm chủ kỹ thuật huấn luyện PhoBERT, viết Custom Loss Function (WBCE) và tích hợp API Streaming / Routing logic trên Python FastAPI. |
| **Thời gian** | 🟢 | Pipeline đo đạc độ trễ (Profiling benchmark) và đo lường F1-score có thể hoàn thành trong 1.5 – 2 tuần. |

**Kết quả:** 0 🔴, 0 🟡, 7 🟢 → **Kết luận:** **TUYỆT ĐỐI AN TOÀN (Safe to Proceed)**, không có bất kỳ cản trở nào về tài nguyên hay kỹ thuật.

### Kế hoạch xử lý & Downscope (nếu có rủi ro)
- Nếu việc tích hợp PhoBERT lên CPU cục bộ vượt quá 300ms, sẽ áp dụng kỹ thuật **Dynamic Quantization (INT8)** hoặc dùng kiến trúc **BiGRU+MaskedPool** (theo bài `M041`) làm Tầng 1 để ép độ trễ xuống dưới 10ms mà không làm giảm độ nhạy phát hiện lừa đảo.

---

## 4. Phát biểu GAP chính thức

> *"Chưa có nghiên cứu nào thiết kế và chứng minh hiệu quả của một Kiến trúc AI 2 Tầng Phân Cấp (2-Tier Cascaded AI: Fast-Path Local CPU PLM + Cloud LLM Reasoning Fallback) kết hợp hàm mất mát Weighted Binary Cross-Entropy (WBCE) nhằm cân bằng tối ưu giữa Độ chính xác (F1 > 95%), Độ trễ thực tế (< 250ms trên CPU) và Chi phí vận hành (giảm 80% chi phí API) cho hệ thống phòng chống lừa đảo di động."*

---

## 5. Đề xuất sơ bộ cho nhóm (chuẩn bị họp RBL-3)

*   **Dataset khả thi:** 
    *   Tập benchmark quốc tế từ `M041` (UCI + LSDST-2022) để so sánh baseline khách quan.
    *   Tập dữ liệu Tiếng Việt `ScamShield-VN-Corpus` ($\ge 500$ mẫu đa dạng teencode do Minh Quang xây dựng) để kiểm chứng thực tế.
*   **Metric đề xuất:** 
    *   *Độ chính xác:* Macro-F1, Precision, Recall (ưu tiên giảm thiểu tối đa False Negative rate).
    *   *Hiệu năng triển khai:* P95/P99 Inference Latency (ms), CPU/Memory Footprint (MB), và Cost per 1,000 queries ($).
*   **LLM / Tool đề xuất:** 
    *   *Tầng 1 (Local CPU):* `PhoBERT-base` (hoặc `BiGRU+MaskedPool`) fine-tuned với hàm mất mát **WBCE** (phạt nặng lỗi bỏ lọt lừa đảo).
    *   *Tầng 2 (Cloud Fallback - Hội đồng Pháp y Đa Tác tử):* Nâng cấp từ Single LLM lên Consolidated 3-Agent Forensic Council (tinh giản từ 5 tác tử theo Occam's Razor) (kế thừa `M043` MultiPhishGuard, `M044` PoLL, `M045` NAACL 2025 Council) với cơ chế Early-Exit Fast-Path (<1.2s) và vai trò Public Defender dập tắt Alarm Fatigue khi Confidence Score của Tầng 1 $< 90\%$.
*   **Baseline đề xuất:** So sánh trực tiếp với:
    1.  *Mô hình đơn tầng truyền thống:* SVM + TF-IDF, Logistic Regression từ `M023`.
    2.  *Mô hình Deep Learning đơn lẻ:* Standalone DistilBERT và MacBERT-BiLSTM từ `M041`, `M042`.
    3.  *Mô hình Pure Cloud LLM:* Gọi trực tiếp GPT-4o-mini / Gemini-2.0-Flash 100% không qua tầng đệm để đối chiếu chi phí và độ trễ.
