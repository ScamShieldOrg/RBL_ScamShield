# 📦 THƯ MỤC DỮ LIỆU THÔ (RAW DATASET REPOSITORY)
### Đề tài: ScamShield-VN — Evidence-Grounded Vietnamese Scam & Phishing Detection Platform
> **File:** `data/raw/README.md`  
> **Tuân thủ:** Quality Gate E2 & Tiêu chuẩn liêm chính dữ liệu RBL

---

## 1. Nguồn Dữ Liệu Gốc (Data Sources)

Dữ liệu được thu thập và tổng hợp từ 2 bộ dữ liệu công khai trên Hugging Face Hub:
1. **Nguồn 1:** `trannguyenthaituan/vietnamese_sms_dataset`
   * **URL:** [https://huggingface.co/datasets/trannguyenthaituan/vietnamese_sms_dataset](https://huggingface.co/datasets/trannguyenthaituan/vietnamese_sms_dataset)
2. **Nguồn 2:** `trannguyenthaituan/vietnamese_sms_phishing_sample`
   * **URL:** [https://huggingface.co/datasets/trannguyenthaituan/vietnamese_sms_phishing_sample](https://huggingface.co/datasets/trannguyenthaituan/vietnamese_sms_phishing_sample)

Tên bộ dữ liệu và URL ở trên phản ánh các nguồn được dùng trong quá trình thu thập. Hãy tham khảo trang Hugging Face tương ứng để biết thông tin mô tả, giấy phép và phiên bản hiện hành của từng bộ dữ liệu.

---

## 2. Danh Mục Các Tệp Dữ Liệu Trong Thư Mục

| Tên tệp tin | Số lượng dòng | Cấu trúc các cột (Columns Schema) | Mục đích sử dụng |
| :--- | :---: | :--- | :--- |
| **`vietnamese_sms_merged_all.csv`** | **2.664 mẫu** | `message_id`, `message`, `label`, `source` | Corpus hợp nhất đã xử lý; 2.664 nội dung duy nhất, gồm 2.629 mẫu từ `vietnamese_sms_dataset` và 35 mẫu từ `vietnamese_sms_phishing_sample`. |
| `vietnamese_sms_test.csv` | 597 mẫu | `message`, `label` | Tệp test có sẵn trong thư mục raw (439 nhãn 0, 158 nhãn 1); có 31 nội dung trùng. **Không phải** frozen holdout N=267. |
| `hf_vietnamese_sms_dataset.csv` | 2.991 mẫu | `message_id`, `date`, `message`, `label` | Bản dữ liệu nguồn lưu trong repo; 2.193 nhãn 0, 798 nhãn 1. Có 2.630 nội dung duy nhất (361 dòng trùng nội dung). |
| `hf_vietnamese_sms_phishing_sample_300.csv` | 300 mẫu | `message_id`, `text` | Bản dữ liệu nguồn lưu trong repo; không có cột nhãn. Có 213 nội dung duy nhất (87 dòng trùng nội dung). |
| `vietnamese_sms_full.csv` | 2.991 mẫu | `message_id`, `date`, `message`, `label` | Bản trung gian hiện có trong repo; 2.193 nhãn 0, 798 nhãn 1; 2.630 nội dung duy nhất (361 dòng trùng nội dung). |
| `../processed/frozen_test_267.csv` | 267 mẫu | `original_index`, `message_id`, `message`, `label`, `source` | Frozen holdout thực tế (192 nhãn 0, 75 nhãn 1); 267 nội dung duy nhất. |

---

## 3. Quy Ước Mã Hóa Nhãn (Label Encoding)

* **`0` $\rightarrow$ HAM:** Tin nhắn bình thường, thông báo hợp lệ từ ngân hàng/nhà mạng, mã OTP xác thực, tin nhắn cá nhân hợp pháp.
* **`1` $\rightarrow$ SCAM:** Tin nhắn lừa đảo tài chính, mạo danh đường dẫn ngân hàng (phishing link), tin nhắn trúng thưởng giả, dụ dỗ tuyển dụng lừa tiền cọc, tin nhắn spam độc hại.

---

## 4. Phân Bổ Dữ Liệu & Quy Tắc Niêm Phong (Frozen Test Set Protocol)

Tập dữ liệu hợp nhất **2.664 mẫu** (`vietnamese_sms_merged_all.csv`) gồm:
* **Ham (Nhãn 0):** $1.918$ tin nhắn ($72.0\%$).
* **Scam (Nhãn 1):** $746$ tin nhắn ($28.0\%$).

### Phân Tách Tập Dữ Liệu Cố Định:
Toàn bộ quy trình phân tách sử dụng kỹ thuật phân tầng (*Stratified Split*) với seed cố định: `random_state = 42`:
* **Tập Huấn luyện & Validation nội bộ ($90\%$):** $2.397$ mẫu ($1.726$ Ham, $671$ Scam).
* **Tập Kiểm thử Đóng băng (Frozen Test Set, xấp xỉ $10\%$):** **267 mẫu** ($192$ nhãn 0, $75$ nhãn 1), lưu tại `data/processed/frozen_test_267.csv`.

`data/raw/vietnamese_sms_test.csv` là một tệp khác (597 dòng), không phải frozen holdout nêu trên. Các số liệu trong bảng được đếm trực tiếp từ những CSV hiện có trong repo; chúng mô tả snapshot cục bộ và không khẳng định số dòng hiện tại trên Hugging Face.

> [!CRITICAL]
> **Quy tắc niêm phong (Frozen Isolation Rule):**  
> 1. Tập Frozen Test Set ($N=267$) **tuyệt đối không được dùng để huấn luyện mô hình** hoặc tối ưu tham số/ngưỡng threshold.
> 2. Mọi mô hình trong bài báo (ViSoBERT, PhoBERT-base, FPT ViBERT, PhoBERT-large, Gemini 3.5 Flash) **bắt buộc phải được đánh giá trên cùng một tập $267$ mẫu này** để đảm bảo tính công bằng và điều kiện kiểm định ghép cặp (Paired McNemar Test).
> 3. Không được sửa đổi, xóa dòng hoặc chèn thêm dữ liệu vào tệp `vietnamese_sms_merged_all.csv`.
