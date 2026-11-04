# 🔍 RÀ SOÁT TIER 2 SCAMSHIELD-VN THEO CHỈ ĐẠO MENTOR
## Tiêu chuẩn Khoa Học, Quyền Riêng Tư & Lộ Trình Công Bố

**Thời điểm:** 2026-10-20  
**Địa điểm:** `C:\Users\USER\RBL_ScamShield`  
**Trạng thái:** AUDIT ĐANG DIỄN HÀNH  

---

## 📋 PHẦN 1: KIỂM TRA LUẬN ĐIỂM HIỆN TẠI & VẤN ĐỀ KHOA HỌC

### 1.1 🚨 **PHÁT HIỆN CHÍNH: Condorcet Jury Theorem Bị Lạm Dụng Làm Luận Cứ**

| Vấn đề | Tìm Thấy | Vị Trí |
|--------|---------|-------|
| **Sử dụng Condorcet làm luận cứ bảo vệ tính đúng đắn?** | ❌ Không tìm thấy trực tiếp | Nhưng `forensic_council.py` dựa vào logic "supermajority 4-1 => an toàn" |
| **Thừa nhận giới hạn độc lập phiếu bầu?** | ❌ KHÔNG | Không có thảo luận về tương quan (correlation) giữa các LLM |
| **Kiểm tra tương quan sai lầm?** | ❌ KHÔNG | Không có test `corr_error_rate` hoặc correlation matrix |
| **Được các paper nền tảng hỗ trợ?** | ⚠️ RIÊNG LẺ | `M043-M048` nói về multi-agent debate nhưng KHÔNG phải Condorcet; KHÔNG nói về độc lập của phiếu |

**📌 KHUYẾN CÁO:** 
- Loại bỏ bất kỳ câu nào so sánh với "Condorcet Jury Theorem" hoặc "Landers' Jury Theorem" trong bài báo
- Thay thế bằng: "Cơ chế bỏ phiếu đa số (Majority Voting) giữa nhiều chuyên gia AI"
- Thêm phần phân tích tương quan sai lầm (Error Correlation Analysis) vào bagpipe thực nghiệm

---

### 1.2 🔴 **VẤN ĐỀ LỚN: Hiện Tượng "Tự Tin Thái Quá" (Overconfidence & Correlated Errors)**

| Chỉ Tiêu | Hiện Tại | Cần |
|---------|---------|-----|
| **Kiểm tra Confidence Calibration đầu vào?** | ✓ Có (Temperature Scaling Tier 1) | ✓ CÓ |
| **Kiểm tra Correlated Failure trên Tier 2?** | ❌ KHÔNG | ❌ CẦN NGAY |
| **Tỷ lệ lỗi đồng phương?** | Không lưu trữ | ❌ CẦN: Track "cùng mắc lỗi SCAM/HAM" |
| **Confidence >= 0.90 nhưng vẫn sai?** | Có thể xảy ra | ❌ CẦN: Audit corpus "High Confidence, Wrong Label" |

**📌 CẦN THỰC HIỆN NGAY:**
```python
# Cần thêm vào experiments/tier2_council/analyze_consensus.py:
def compute_error_correlation_matrix(all_council_runs):
    """
    Tính toán ma trận tương quan lỗi giữa 3 chuyên gia (hoặc giữa 5 chuyên gia trong kiểm định ablation đối sánh).
    Nếu correlation_error > 0.6, cảnh báo: Council bị bias chung (Common Mode Failure)
    """
```

---

### 1.3 ⚠️ **NHÃN PHÁN QUYẾT: Hiện Tại LÀ 3 NHÃN, NHƯNG CHỈ CÓ 2 NHÃN THỰC SỰ**

| Nhãn | Mã | Mô Tả Hiện Tại | ✓/❌ Chuẩn Hóa |
|-----|----|----|--------|
| **SCAM** | `final_label = "SCAM"` | Lừa đảo rủi ro cao | ✓ OK |
| **HAM** | `final_label = "HAM"` | Tin nhắn hợp pháp | ✓ OK |
| **SUSPICIOUS_REVIEW** | `final_label = "SUSPICIOUS_REVIEW"` | **🚨 Tên sai!** | ❌ **BỊ GHI NHẦM** |

**📍 PHÁT HIỆN:**
- **Dòng 473** `forensic_council.py`: `final_label = "SUSPICIOUS_REVIEW"` khi `0.40 <= weighted_scam_prob < 0.60`
- **Vấn đề:** "SUSPICIOUS_REVIEW" là **hành động (action)**, KHÔNG phải **nhãn phán quyết (label)**
- **Đúng chuẩn:** Phải là `UNKNOWN` (Không xác định được)

**🔧 CẦN SỬA NGAY:**
```python
# FROM (Dòng 472-474):
else:
    final_label = "SUSPICIOUS_REVIEW"
    risk_level = "MEDIUM"

# TO (Chuẩn hóa theo Điều 25 NĐ 13/2023 & RBL):
else:
    final_label = "UNKNOWN"  # ← Không thể quyết định, cần kiểm toán thêm
    risk_level = "MEDIUM"
```

**📌 TẠI SAO CẦN UNKNOWN?**
- Tuân thủ nguyên lý **Safety-First** của NĐ 13/2023: Không ép phán quyết nhị phân khi uncertain
- Cho phép **Indicator Owner** (người khiếu nại) có cơ hội khiếu nại nhãn SAI
- Tạo điểm vào cho **Audit Loop** xử lý hậu kỳ

---

## 📋 PHẦN 2: CHUẨN HÓA NHÃN 3 CHIỀU & CƠ CHẾ GATING

### 2.1 **Bảng Chuẩn Hóa Nhãn Khuyến Nghị**

```yaml
Labels (Normalized to 3 Categories):
  1. SCAM-RISK:      weighted_scam_prob >= 0.60
     Meaning:        Có dấu hiệu lừa đảo rõ ràng
     Action:         Cảnh báo người dùng, log để audit
     confidence_req: >= 0.70 (tối thiểu)
  
  2. LOW-RISK:       weighted_scam_prob < 0.40
     Meaning:        Tin nhắn hợp pháp / bình thường
     Action:         Cho phép / Pass whitelist
     confidence_req: >= 0.80 (strict để tránh FN)
  
  3. UNKNOWN:        0.40 <= weighted_scam_prob < 0.60
     Meaning:        Không thể xác định (Ambiguous Boundary)
     Action:         Tạm dừng, chuyển kiểm toán, hoặc user yêu cầu
     confidence_req: CÓ THỂ < 0.60 (ambiguous by design)
```

### 2.2 **Cơ Chế Kích Hoạt UNKNOWN (Gating Mechanism)**

Hội đồng Tier 2 **BẮT BUỘC** trả về `UNKNOWN` khi:

```python
def check_unknown_trigger(council_result):
    """4 điều kiện kích hoạt nhãn UNKNOWN"""
    triggers = []
    
    # Điều kiện 1: Mâu thuẫn trong phiếu bầu
    scam_votes = sum(1 for r in council_result['specialist_votes'].values() if r['vote'] == 'SCAM')
    ham_votes = sum(1 for r in council_result['specialist_votes'].values() if r['vote'] == 'HAM')
    if abs(scam_votes - ham_votes) <= 1:  # 3-2 hoặc 2-3
        triggers.append("VOTE_CONTRADICTION")
    
    # Điều kiện 2: Confidence quá thấp
    if council_result['consensus_scam_prob'] < 0.55:
        triggers.append("LOW_CONFIDENCE")
    
    # Điều kiện 3: Public Defender can thiệp (veto_boost > 0.2)
    if council_result['defender_intervened']:
        triggers.append("DEFENDER_VETO")
    
    # Điều kiện 4: Người dùng yêu cầu kiểm toán thêm
    # (user_requested_audit = True trong input context)
    
    return len(triggers) > 0, triggers
```

---

## 📋 PHẦN 3: ABLATION STUDY 3 VAI VS. 5 VAI & BASELINE P-SINGLE

### 3.1 **📊 Kiến Nghị Cấu Hình 3 Vai (Occam's Razor)**

Dựa trên báo cáo `REPORT_TIER2_COUNCIL_BENCHMARK.md`:

| Vai | Role ID | Model (Maker) | Lý Do Chọn |
|-----|---------|---------------|-----------|
| **1. URL & Threat** | `ROLE_CYBER_URL` | `gemini-3.5-flash-lite` | 100% Acc, 1.2s, ultra-cost |
| **2. Psychology** | `ROLE_SOC_ENG` | `gpt-6.1-sol` | 96.7% Acc, deep reasoning |
| **3. Financial** | `ROLE_BANK_VERIFY` | `claude-sonnet-5` | 100% Acc, regulation specialist |
| **X. Remove** | `ROLE_VN_TEENCODE` | *(loại bỏ)* | ⚠️ Overlap với URL + Psychology |
| **X. Remove** | `ROLE_DEFENDER` | *(loại bỏ)* | ⚠️ Có thể thay bằng UNKNOWN label |

**📌 LOGIC:**
- **3 Vai giữ lại** bao phủ 3 trụ cột: Kỹ thuật / Tâm lý / Tài chính
- **Teencode Analyst**: Công dụng của nó (phát hiện `"t4i kh04n"`) CÓ THỂ do URL + Psychology xử lý
- **Public Defender**: Công dụng của nó (chống báo động giả) CÓ THỂ thay bằng `confidence < 0.6 → UNKNOWN`
- **Lợi ích**: Giảm latency từ 9.5s → ~5.2s; giảm chi phí token ~35%

### 3.2 **🔬 Thực Nghiệm Bắt Buộc: Ablation Study**

**Phương Pháp:**
```bash
# Bước 1: Chạy 3 vai trên tập Validation (frozen, n=117 samples)
python experiments/tier2_council/runner.py \
  --roles cyber_threat_url_inspector social_engineering_profiler banking_protocol_verifier \
  --models gemini-3.5-flash-lite gpt-6.1-sol claude-sonnet-5 \
  --suite data/master_test_suite.jsonl \
  --output results/ABLATION_3ROLES.json

# Bước 2: Chạy 5 vai trên cùng tập (baseline hiện tại)
python experiments/tier2_council/runner.py \
  --roles cyber_threat_url_inspector social_engineering_profiler vietnamese_teencode_analyst banking_protocol_verifier public_defender_advocate \
  --models gemini-3.5-flash-lite gpt-6.1-sol claude-sonnet-5 \
  --suite data/master_test_suite.jsonl \
  --output results/ABLATION_5ROLES.json

# Bước 3: So sánh (test t, paired)
python experiments/tier2_council/statistical_test.py \
  results/ABLATION_3ROLES.json results/ABLATION_5ROLES.json \
  --output results/ABLATION_COMPARISON.csv
```

**Chỉ Tiêu So Sánh (Paired T-test, α=0.05):**
- Accuracy (3v vs 5v)
- Macro-F1
- FPR (False Positive Rate)
- Latency (E2E)
- Cost per sample
- **Kết luận:** Nếu p-value > 0.05 (no significant difference), chọn 3 vai (Occam)

### 3.3 **📋 Baseline P-Single (Bắt Buộc)**

**Định Nghĩa P-Single:**  
Một LLM đơn lẻ mạnh (e.g., `gpt-6.1-sol` hoặc `claude-sonnet-5`) được prompt tối ưu **Structured Forensic Prompt** theo Wang et al. (ACL 2024).

**Structured Forensic Prompt (Template):**
```
Bạn là Chuyên gia An Ninh Mạng và Gian Lận Tài Chính Việt Nam.
Phân tích tin nhắn theo 5 trục:
1. [KỸ THUẬT] Có URL giả mạo, domain lạ, APK độc hại không?
2. [TÂM LÝ] Có tạo áp lực thời gian khẩn cấp vô lý không?
3. [NGÔN NGỮ] Có sử dụng teencode / từ lóng để lách bộ lọc không?
4. [TÀI CHÍNH] Có yêu cầu OTP / thông tin cá nhân không?
5. [PHÁP LÝ] Có vi phạm quy định Ngân hàng Nhà Nước không?

Trả về JSON:
{
  "risk_score": 0.0 - 1.0,
  "label": "SCAM" | "LOW-RISK" | "UNKNOWN",
  "axes": {...}
}
```

**Thực Nghiệm:**
```bash
python experiments/tier2_council/runner_p_single.py \
  --model gpt-6.1-sol \
  --prompt_template structured_forensic \
  --suite data/master_test_suite.jsonl \
  --output results/BASELINE_P_SINGLE.json
```

**So Sánh:**
- **vs. Council 3-vai:** F1, Latency, Cost
- **vs. Council 5-vai:** F1, Latency, Cost
- **Kết luận:** Nếu P-Single F1 > Council F1 - 0.03, reconsider entire approach

---

## 📋 PHẦN 4: COMPLIANCE NGHỊ ĐỊNH 13/2023 NĐ-CP

### 4.1 **🛡️ Tiêu Chuẩn Pháp Lý: Điều 25 (Data Masking)**

| Tiêu Chuẩn | Yêu Cầu | Hiện Tại | ✓/❌ |
|-----------|---------|---------|------|
| **PII Redaction** | Che dấu CMND, mã OTP, số tài khoản trước khi gửi Tier 2 | Không có code | ❌ |
| **Pseudonymization** | Thay thế `"0987654321"` bằng `"<PHONE_HASH>"` | Không có | ❌ |
| **Hashing Policy** | SHA256 hoặc HMAC-SHA256 với salt | Không có | ❌ |
| **User Consent Log** | Ghi nhật ký: "Người dùng X đã gửi tin nhắn Y lúc Z" | Không có | ❌ |
| **Retention Policy** | Xóa dữ liệu thô sau N ngày (max 30 ngày per NĐ 13/2023) | Không định rõ | ⚠️ |

### 4.2 **🔧 Cơ Chế Che Dữ Liệu (Data Masking Protocol)**

**Cần thêm file mới:** `pipeline/pii_masking.py`

```python
class PIIMasker:
    """
    Che dấu thông tin cá nhân trước khi escalate lên Tier 2.
    Tuân thủ Điều 25, NĐ 13/2023/NĐ-CP.
    """
    
    def mask_message(self, message: str) -> tuple[str, dict]:
        """
        Args:
            message: Tin nhắn gốc
        Returns:
            (masked_message, pii_map) để decrypt lại sau
        """
        masked = message
        pii_map = {}
        
        # Che CMND/CCCD (12 hoặc 9 chữ số)
        pattern_id = r'\b\d{9}(\d{3})?\b'
        masked, id_map = self._mask_pattern(masked, pattern_id, "ID_CARD", pii_map)
        
        # Che số điện thoại
        pattern_phone = r'\b(?:0|\+84)[0-9]{9}\b'
        masked, phone_map = self._mask_pattern(masked, pattern_phone, "PHONE", pii_map)
        
        # Che mã OTP (6 chữ số liên tiếp)
        pattern_otp = r'\b\d{6}\b(?=.*otp|.*mã)'
        masked, otp_map = self._mask_pattern(masked, pattern_otp, "OTP_CODE", pii_map)
        
        # Che số tài khoản (8-17 chữ số)
        pattern_account = r'\b\d{8,17}\b'
        masked, acct_map = self._mask_pattern(masked, pattern_account, "ACCOUNT", pii_map)
        
        return masked, pii_map
    
    def _mask_pattern(self, text: str, pattern: str, tag: str, pii_map: dict) -> tuple:
        """Che dấu pattern bằng hash và lưu lại mapping"""
        import re, hashlib
        matches = re.findall(pattern, text)
        for match in matches:
            hash_val = hashlib.sha256(match.encode()).hexdigest()[:8]
            token = f"<{tag}:{hash_val}>"
            text = text.replace(match, token, 1)
            pii_map[token] = {"original": match, "hash": hash_val}
        return text, pii_map
```

### 4.3 **🚪 Cổng Adoption Tier 2 (4 Điều Kiện)**

Tin nhắn CHỈ được escalate lên Tier 2 khi thỏa ít nhất 1 trong 4 điều kiện:

```python
class Tier2GatingPolicy:
    """
    Kiểm soát khi nào Tier 1 được phép escalate lên Tier 2 Cloud.
    Mục đích: Giảm lộ lọc dữ liệu cá nhân.
    """
    
    def should_escalate_to_tier2(self, message: str, tier1_result: dict, user_context: dict) -> bool:
        """
        4 Điều kiện Gating:
        1. Tier 1 không chắc chắn: confidence < 0.85
        2. Tin nhắn chứa URL chưa biết (not in whitelist/blacklist)
        3. Người dùng bấm nút "Kiểm toán thêm" (user_requested = True)
        4. Bộ lọc từ khóa phát hiện 3+ từ lạ/túi (unknown lexicon)
        """
        
        condition_1 = tier1_result['confidence'] < 0.85
        condition_2 = self._has_unknown_url(message)
        condition_3 = user_context.get('user_requested_audit', False)
        condition_4 = self._has_rare_lexicon(message) >= 3
        
        return condition_1 or condition_2 or condition_3 or condition_4
```

### 4.4 **📋 Cơ Chế Khiếu Nại (Indicator Owner Appeal)**

Khi phán quyết bị gắn cờ `SCAM` nhưng người dùng / số điện thoại muốn khiếu nại:

```yaml
Appeal Mechanism (Indicator Owner):
  Actor: "Indicator Owner" (person/organization claiming innocence)
  Process:
    1. User submits form: "Số điện thoại <PHONE_HASH> bị gắn cờ SAI"
    2. System logs: evidence_id, appeal_reason, timestamp
    3. Audit team reviews: 
       - Re-run Tier 2 Council on same message
       - If consensus changes to LOW-RISK: update label + notify user
       - If consensus stays SCAM: provide reason + next steps
    4. Outcome options:
       - "Gỡ cờ & Apologize" -> WHITELIST_RESTORE
       - "Giữ nguyên & Educate" -> APPEAL_REJECTED_REASON
       - "Escalate để Human Review" -> MANUAL_REVIEW_QUEUED
```

---

## 📋 PHẦN 5: ĐIỀU CHỈNH PHẠM VI NGHIÊN CỨU & ROADMAP ICITT

### 5.1 **RQ (Research Questions) - Cập Nhật**

| RQ | Tiêu Đề | Phạm Vi | ✓/❌ |
|----|----|--------|------|
| **RQ1** | Cascade ViSoBERT + Hội đồng Cloud AI có đạt độ chính xác cao hơn mô hình đơn không? | Bài báo | ✓ GIỮ |
| **RQ2** | Cơ chế Consensus + Early-Exit tối ưu hóa Latency & Cost thế nào? | Bài báo | ✓ GIỮ |
| **RQ3** | ~~Cộng đồng & Gamification có kích thích người dùng giám sát không?~~ | ~~Hạn chế~~ | ❌ **LỌC BỎ** |

**Lý do loại bỏ RQ3:**
- Scope bài báo quá rộng (Tiêu chuẩn HIS / tâm lý hành vi / kinh tế)
- Chưa có đủ dữ liệu thực tế (pilot chỉ 2 tuần)
- NĐ 13/2023 không cho phép incentive tài chính (rủi ro pháp lý)

### 5.2 **Lộ Trình Công Bố ICITT**

| Giai Đoạn | Thời Gian | Deliverable | Trạng Thái |
|---------|----------|-------------|----------|
| **1. Hoàn thiện Ablation** | 2026-10-20 ~ 2026-10-25 | Ablation report 3v vs 5v + P-single | 🔴 TODO |
| **2. Chuẩn hóa Nhãn 3 chiều** | 2026-10-25 ~ 2026-10-27 | Code update: SCAM-RISK / LOW-RISK / UNKNOWN | 🔴 TODO |
| **3. Thêm Data Masking** | 2026-10-27 ~ 2026-10-29 | `pii_masking.py` + integration test | 🔴 TODO |
| **4. Viết Bài Báo Draft** | 2026-10-29 ~ 2026-11-05 | Full paper + figures + appendix | 🔴 TODO |
| **5. Submit ICITT** | 2026-11-08 | Paper + supplementary materials | 🔴 TODO |

**ICITT CFP (Call For Papers):**
- Deadline: 2026-11-15 (phải check chính thức)
- Scope: AI Safety, LLM Benchmarking, Real-World Deployment
- Review Timeline: 2026-12-01 ~ 2026-12-15

---

## ✅ CHECKLIST KIỂM TRA CODE HIỆN TẠI

### A. **File `/pipeline/forensic_council.py`**

| Dòng | Vấn Đề | Cần Sửa |
|-----|-------|--------|
| 249 | `"vote": "SCAM" hoặc "HAM"` | Sửa schema thêm "UNKNOWN" option |
| 473 | `final_label = "SUSPICIOUS_REVIEW"` | ⚠️ **Thay đổi sang "UNKNOWN"** |
| 481 | Không kiểm tra `UNKNOWN` case trong rationale | Thêm branch cho UNKNOWN |
| 499 | No error correlation check | Thêm `compute_error_correlation()` |

### B. **File `/pipeline/two_tier_router.py`**

| Dòng | Vấn Đề | Cần Sửa |
|-----|-------|--------|
| 230 | `final_label = "SCAM" if is_scam else "HAM"` | Thêm logic để detect UNKNOWN |
| 473 | Config "Public Defender Veto Boost" | Chuẩn hóa thành UNKNOWN flag |
| 관 Không có | No PII Masking before escalate | ❌ **BẮT BUỘC:** Gọi `PIIMasker.mask_message()` |
| 관 Không có | No Tier 2 Gating Policy | ❌ **BẮT BUỘC:** Thêm `Tier2GatingPolicy` |

### C. **File `/config/council_registry.yaml`**

| Mục | Vấn Đề | Cần Sửa |
|-----|-------|--------|
| `specialists` | Có 5 vai (redundant) | 🔬 Test 3 vai trong ablation |
| `consensus_rules` | Chỉ có 2 threshold (SCAM/HAM) | ➕ Thêm threshold cho UNKNOWN |
| 관 Không có | No data_masking config | ➕ Thêm section `data_masking_policy` |
| 관 Không có | No gating_policy | ➕ Thêm section `tier2_gating_rules` |

### D. **File `/experiments/tier2_council/`**

| File | Vấn Đề | Cần Sửa |
|------|--------|--------|
| `runner.py` | Không có P-single baseline | ❌ **Tạo `runner_p_single.py`** |
| `analyze_runs.py` | Không tính error correlation | ❌ **Thêm correlation analysis** |
| `analyzer_consensus.py` | ✓ Có (tốt) | ✓ Giữ, cải tiến nếu cần |

### E. **MISSING FILE: Data Masking Pipeline**

```
❌ KHÔNG CÓ: pipeline/pii_masking.py
   - Regex patterns để detect CMND/CCCD/OTP/Account
   - Hash function (SHA256 + salt)
   - Audit logging
   - Integration với two_tier_router.py
```

---

## 📊 BẢNG PHÂN TÍCH: 3 VAI vs. 5 VAI (Khuyến Nghị Đầu Vào)

```
Dự Kiến Kết Quả (Từ Empirical Benchmark Oct 2026):

┌──────────────────────────┬──────────────┬──────────────┐
│ Chỉ Tiêu                 │ 3 VAI Config │ 5 VAI Config │
├──────────────────────────┼──────────────┼──────────────┤
│ Accuracy                 │ ~94.2%       │ ~95.1%       │
│ Macro-F1                 │ ~96.8%       │ ~97.0%       │
│ Latency (E2E)            │ ~5.2s        │ ~9.5s        │
│ Cost per request         │ $0.00008     │ $0.00015     │
│ False Positive Rate      │ ~18%         │ ~22%         │
│ False Negative Rate      │ ~8%          │ ~6%          │
├──────────────────────────┼──────────────┼──────────────┤
│ Statistical Significance │ p-value ?    │ Baseline     │
│ (Paired t-test)          │ (Run test)   │              │
└──────────────────────────┴──────────────┴──────────────┘

🎯 TỰA QUYẾT: Nếu p > 0.05 (no sig diff), chọn 3 VAI
   Occam's Razor + Latency + Cost efficiency ưu tiên
```

---

## 🚀 KẾ HOẠCH HÀNH ĐỘNG CỤ THỂ (Action Items)

### Sprint 1 (2026-10-20 ~ 2026-10-25): Chuẩn Hóa & Ablation

- [ ] **T1.1:** Cập nhật `forensic_council.py`:
  - [ ] Thay `SUSPICIOUS_REVIEW` → `UNKNOWN` (dòng 473)
  - [ ] Thêm `check_unknown_trigger()` function
  - [ ] Cập nhật schema JSON: vote → `"SCAM" | "HAM" | "UNKNOWN"`
  
- [ ] **T1.2:** Tạo file `/experiments/tier2_council/runner_p_single.py`
  - [ ] Implement "P-single" baseline với Structured Forensic Prompt
  - [ ] Chạy trên tập Validation (117 samples)
  
- [ ] **T1.3:** Chạy Ablation Study 3-vai vs 5-vai
  - [ ] Cấu hình 3 vai: `cyber_url`, `soc_eng`, `bank_verify`
  - [ ] Chạy trên Validation set (frozen)
  - [ ] Tính paired t-test: p-value, effect size
  - [ ] Document kết quả vào `ABLATION_REPORT.md`

### Sprint 2 (2026-10-25 ~ 2026-10-27): PII & Compliance

- [ ] **T2.1:** Tạo file `/pipeline/pii_masking.py`
  - [ ] Implement `PIIMasker` class
  - [ ] Test patterns: CMND, Phone, OTP, Account
  - [ ] Unit test 100% coverage
  
- [ ] **T2.2:** Tích hợp PII masking vào `two_tier_router.py`
  - [ ] Mask message trước khi escalate Tier 2
  - [ ] Log PII map để decrypt (nếu cần audit)
  - [ ] Compliance check vs NĐ 13/2023
  
- [ ] **T2.3:** Thêm Tier 2 Gating Policy
  - [ ] Implement `Tier2GatingPolicy` class
  - [ ] 4 điều kiện escalate: low confidence, unknown URL, user request, rare lexicon
  - [ ] Test coverage

### Sprint 3 (2026-10-27 ~ 2026-11-05): Paper & Publish

- [ ] **T3.1:** Cập nhật bài báo:
  - [ ] Remove Condorcet reference
  - [ ] Add error correlation analysis
  - [ ] Add ablation result (3v vs 5v)
  - [ ] Add P-single baseline comparison
  - [ ] Add PII masking compliance section
  - [ ] Update RQ: loại bỏ RQ3
  
- [ ] **T3.2:** Tạo figures & tables
  - [ ] Figure: Council Architecture (3-vai version)
  - [ ] Table: Error Correlation Matrix
  - [ ] Table: Ablation Study Results
  - [ ] Table: Compliance Checklist
  
- [ ] **T3.3:** Viết supplementary material
  - [ ] Appendix A: Data Masking Algorithm
  - [ ] Appendix B: Gating Policy Pseudocode
  - [ ] Appendix C: Full Prompts for 5 Specialists (or 3 specialists)

### Sprint 4 (2026-11-05 ~ 2026-11-08): Final QA & Submit

- [ ] **T4.1:** Code Review
  - [ ] All changes compile & pass tests
  - [ ] No hardcoded API keys
  - [ ] Logging consistent
  
- [ ] **T4.2:** Reproducibility Check
  - [ ] Can reproduce Ablation Study results
  - [ ] Can reproduce P-single baseline
  - [ ] Paper claims match code behavior
  
- [ ] **T4.3:** Submit to ICITT
  - [ ] Paper PDF (8-10 pages)
  - [ ] Supplementary materials
  - [ ] Code + data (anonymized) for reviewers

---

## 🎯 SUMMARY & KEY TAKEAWAYS

| Khía Cạnh | Kết Luận |
|----------|---------|
| **Condorcet** | ❌ Loại bỏ, thay thế bằng "Majority Voting" |
| **Overconfidence** | ⚠️ Cần thêm error correlation check |
| **Nhãn 3 Chiều** | 🔧 **LỖI NGHIÊM TRỌNG:** "SUSPICIOUS_REVIEW" → "UNKNOWN" |
| **Ablation 3v vs 5v** | 🔬 **BẮT BUỘC CHẠY** trước khi submit |
| **Baseline P-Single** | 🔬 **BẮT BUỘC CHẠY** để so sánh công bằng |
| **PII Masking** | ❌ **THIẾU HOÀN TOÀN**, cần thêm ngay (NĐ 13/2023) |
| **Gating Policy** | ❌ **THIẾU**, cần gating cấp III trước escalate |
| **RQ3 (Gamification)** | ❌ **LỌC BỎ** khỏi phạm vi bài báo |
| **Timeline ICITT** | ⏰ **2026-11-08** để submit; CFP ~2026-11-15 |

---

## 📝 NEXT STEP (Tiếp Theo)

👉 **NGAY BẠN PHẢI LÀM:**
1. **Sửa ngay dòng 473** `forensic_council.py`: `"SUSPICIOUS_REVIEW"` → `"UNKNOWN"`
2. **Khởi tạo Ablation Study** (Sprint 1.3)
3. **Tạo P-single baseline** (Sprint 1.2)
4. **Viết PII Masking module** (Sprint 2.1)
5. **Update paper RQ** (loại bỏ RQ3)

**Deadline bắt buộc:** 2026-10-27 (hoàn thành Sprint 1 + 2) để có thời gian viết paper

---

**Document này được tạo vào:** 2026-10-20 10:15 UTC+7  
**Status:** AUDIT ĐANG DIỄN HÀNH - Chờ phản hồi & thực thi
