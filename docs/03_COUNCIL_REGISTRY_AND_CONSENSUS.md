# 03. COUNCIL REGISTRY & CONSENSUS — HỘI ĐỒNG PHÁP Y 3 AGENT (CONSOLIDATED) & CƠ CHẾ ĐỒNG THUẬN

Tài liệu này đặc tả chi tiết cơ chế hoạt động của **Hội Đồng Giám Định Pháp Y Đa Tác Tử Tinh Giản 3 Ghế (Consolidated 3-Agent Multi-LLM Forensic Council)** ở Tầng 2 (Cloud Fallback), danh mục mô hình dự phòng (Failover Registry), và thuật toán trọng tài đồng thuận (Consensus Engine) chuẩn hóa theo Khung RBL.

---

## 1. Bối Cảnh Tinh Giản: Chuyển Đổi Từ 5 Agent Sang 3 Agent (Occam's Razor)

Ban đầu, Tầng 2 được thiết kế với Hội đồng 5 chuyên gia độc lập. Tuy nhiên, qua thực nghiệm kiểm định ablation thực tế trên tập $N=117$ mẫu Master Challenge Suite (kèm kiểm định thống kê McNemar):
* **Kiểm định McNemar:** $\chi^2 = 3.2000, p = 0.0736 \ge 0.05$ (Chấp nhận giả thuyết vô hiệu $H_0$ — không có sự suy giảm chính xác pháp y có ý nghĩa thống kê giữa 5 agent và 3 agent).
* **Hiệu quả tối ưu:** Giảm số cuộc gọi API từ 585 xuống 351 cuộc gọi (tiết kiệm **$40.0\%$ chi phí vận hành token API** và giảm đáng kể độ trễ tích lũy).
* **Giữ vững chỉ số an toàn:** Tỷ lệ báo động giả (False Positive Rate - FPR) đạt mức kỷ lục **$0.00\%$** (triệt tiêu hoàn toàn Alarm Fatigue trên tin nhắn ngân hàng thật).

### Bảng Đối Chiếu Chuyển Đổi (5 Agent Cũ $\rightarrow$ 3 Agent Mới):

| STT | 5 Agent Ban Đầu (Legacy) | Vai Trò & Hạn Chế Cũ | 3 Agent Hợp Nhất (Production) | Cơ Sở Khoa Học & Phân Bổ Mới |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `cyber_threat_url_inspector`<br>*(ROLE_CYBER_URL)* | Giám định URL độc hại, homoglyph, APK lạ. Tách rời với quy trình ngân hàng. | **Ghế 1: `cyber_financial_analyst`**<br>*(ROLE_CYBER_BANK)* | **Hợp nhất Agent 1 & Agent 2:** Các cuộc tấn công lừa đảo viễn thông tại VN luôn kết hợp hạ tầng link giả mạo với mạo danh ngân hàng (QĐ 2345/QĐ-NHNN). Hợp nhất giúp đánh giá toàn diện hạ tầng kỹ thuật và quy chuẩn tài chính mà không phân mảnh ngữ cảnh. |
| **2** | `banking_protocol_verifier`<br>*(ROLE_BANK_VERIFY)* | Đối chiếu quy định NHNN, sinh trắc học 2345. Bị phân mảnh dữ liệu link. | |
| **3** | `social_engineering_profiler`<br>*(ROLE_SOC_ENG)* | Bóc tách đòn bẩy tâm lý khẩn cấp (24h, bắt giữ, lòng tham). | **Ghế 2: `psycholinguistic_slang_profiler`**<br>*(ROLE_PSYCHO_TEENCODE)* | **Hợp nhất Agent 3 & Agent 4:** Tâm lý tội phạm và thủ thuật teencode/lách từ khóa viễn thông có cùng bản chất ngữ nghĩa. Hợp nhất giúp phân tích đồng thời cả tầng nghĩa ngầm (thao túng) lẫn tầng bề mặt ký tự ngụy trang ("t4i kh04n"). |
| **4** | `vietnamese_teencode_analyst`<br>*(ROLE_VN_TEENCODE)* | Giải mã teencode, thay ký tự số lách bộ lọc viễn thông. | |
| **5** | `public_defender_advocate`<br>*(ROLE_DEFENDER)* | Bào chữa công cộng, tìm lý do hợp pháp, dập tắt Alarm Fatigue. | **Ghế 3: `public_defender_advocate`**<br>*(ROLE_DEFENDER)* | **Bảo toàn chủ quyền độc lập:** Giữ nguyên vị thế độc lập và quyền **Veto $-0.25$**. Đây là chốt chặn sinh tử giúp duy trì $0.00\%$ FPR, bảo vệ người dùng không bị chặn nhầm tin nhắn OTP/giao dịch hợp pháp. |

---

## 2. Đặc Tả Chi Tiết 3 Chuyên Gia Pháp Y Hội Đồng (Production Council)

```yaml
specialists:

  # Ghế 1: Chuyên gia An ninh Mạng & Quy trình Pháp lý Ngân hàng
  cyber_financial_analyst:
    role_id: "ROLE_CYBER_BANK"
    display_name: "Cyber-Financial & Banking Security Analyst"
    primary_maker_model: "gpt-6.1-sol"
    secondary_checker_model: "gemini-3.5-flash-lite"
    standby_priority_chain:
      - "gemini-3.8-flash"
      - "gpt-6-sol"
      - "gemini-3.5-flash"
    weight: 1.3
    mission: >
      Giám định hạ tầng kỹ thuật (tên miền typosquatting, homoglyph, APK độc hại) 
      kết hợp đối chiếu Quyết định 2345/QĐ-NHNN (ngân hàng KHÔNG BAO GIỜ gửi SMS kèm link bắt đăng nhập cập nhật sinh trắc học).

  # Ghế 2: Chuyên gia Tâm lý Tội phạm & Biến thể Ngôn ngữ Tiếng Việt
  psycholinguistic_slang_profiler:
    role_id: "ROLE_PSYCHO_TEENCODE"
    display_name: "Psycholinguistic & Vietnamese Slang Profiler"
    primary_maker_model: "gpt-6.1-sol"
    secondary_checker_model: "gemini-3.5-flash-lite"
    standby_priority_chain:
      - "gemini-3.8-flash"
      - "gpt-6-sol"
      - "gemini-3.5-flash"
    weight: 1.2
    mission: >
      Phát hiện đòn bẩy tâm lý khẩn cấp vô lý ("trong 24h", "khóa sim ngay"), đe dọa tố tụng (Công an, VKS), 
      hoặc bẫy lòng tham kết hợp giải mã teencode, ký tự số ngụy trang lách bộ lọc mạng ("t4i kh04n", "n9an h4n9").

  # Ghế 3: Luật sư Bào chữa Công cộng & Triệt tiêu Báo động Giả (Alarm Fatigue)
  public_defender_advocate:
    role_id: "ROLE_DEFENDER"
    display_name: "Public Defender & Anti-False-Positive Advocate"
    primary_maker_model: "gpt-6.1-sol"
    secondary_checker_model: "gemini-3.8-flash"
    standby_priority_chain:
      - "gemini-3.5-flash-lite"
      - "gpt-6-sol"
      - "gemini-3.5-flash"
    weight: 1.3
    veto_power: -0.25
    mission: >
      Tìm mọi chứng cứ chứng minh tin nhắn là giao dịch thông thường, mã OTP hợp pháp, thông báo dịch vụ định kỳ. 
      Ưu tiên bảo vệ nhãn LOW-RISK để người dùng không bị tê liệt bởi báo động giả.
```

---

## 3. Thuật Toán Trọng Tài Đồng Thuận Chuẩn Hóa 3 Nhãn

### 3.1. Khung Nhãn Chuẩn Hóa (Standardized 3-Label Framework)
Hội đồng Tier 2 trả về chính xác 1 trong 3 nhãn chuẩn tắc (tuân thủ Điều 25 Nghị định 13/2023/NĐ-CP):
1. **`SCAM-RISK`:** Nguy cơ lừa đảo cao / đặc biệt nghiêm trọng (Điểm đồng thuận $P_{\text{scam}} \ge 0.60$).
2. **`LOW-RISK`:** Tin nhắn an toàn / giao dịch hợp pháp (Điểm đồng thuận $P_{\text{scam}} < 0.40$).
3. **`UNKNOWN`:** Vùng phân vân / ranh giới mập mờ ($0.40 \le P_{\text{scam}} < 0.60$ hoặc có xung đột phiếu bầu sâu sắc).

### 3.2. Công Thức Trọng Số & Can Thiệp Bào Chữa (Public Defender Veto)
1. **Tính xác suất lừa đảo thô có trọng số:**
   $$P_{\text{raw}} = \frac{\sum_{i=1}^3 w_i \cdot p_i}{\sum_{i=1}^3 w_i}$$
   với $w_1 = 1.3$, $w_2 = 1.2$, $w_3 = 1.3$.
2. **Can thiệp Veto chống Báo Động Giả:**
   Nếu `public_defender_advocate` bỏ phiếu `LOW-RISK` với độ tự tin $\ge 0.80$:
   $$P_{\text{adjusted}} = \max\left(0.0, P_{\text{raw}} - 0.25\right)$$
3. **Phán quyết cuối cùng:**
   * Nếu $P_{\text{adjusted}} \ge 0.60$ (và không có mâu thuẫn phiếu đối kháng 2-1 bất định): Nhãn **`SCAM-RISK`**.
   * Nếu $P_{\text{adjusted}} < 0.40$: Nhãn **`LOW-RISK`**.
   * Nếu $0.40 \le P_{\text{adjusted}} < 0.60$ hoặc bất đồng ý kiến phiếu bầu: Kích hoạt nguyên lý Thận trọng Tri thức (Epistemic Caution), xuất nhãn **`UNKNOWN`** để chuyển kiểm toán viên hoặc cảnh báo người dùng xác thực thủ công.

### 3.3. Cơ Chế Thoát Nhanh (Early-Exit Fast-Path)
Khi 3 chuyên gia được kích hoạt song song qua `asyncio`, nếu hệ thống ghi nhận **đồng thuận tuyệt đối 3-0** (`SCAM-RISK` hoặc `LOW-RISK`), quá trình biểu quyết có thể chốt sớm để tối ưu hóa độ trễ phản hồi người dùng.
