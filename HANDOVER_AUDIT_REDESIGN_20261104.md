# TÀI LIỆU BÀN GIAO & TỔNG HỢP TOÀN DIỆN HỆ THỐNG
## AUDIT KỸ THUẬT, THỰC NGHIỆM HỌC THUẬT & BẢN THIẾT KẾ LẠI TOÀN DIỆN (REDESIGN PLAN)
**Dự án:** ScamShield-VN (`RBL_ScamShield` & `scamshield-app`)  
**Ngày cập nhật:** 04/11/2026  
**Phiên bản tài liệu:** v1.0.0-COMPACT-HANDOVER  
**Tình trạng Git:** Giữ nguyên trên Working Tree — **TUYỆT ĐỐI KHÔNG CHẠY GIT COMMIT / PUSH CHO ĐẾN KHI ĐƯỢC DUYỆT**.

---

Tài liệu chi tiết đầy đủ được lưu tại:
👉 [docs/HANDOVER_AUDIT_REDESIGN_20261104.md](file:///c:/Users/USER/RBL_ScamShield/docs/HANDOVER_AUDIT_REDESIGN_20261104.md)

### TÓM TẮT CỐT LÕI
1. **Các sai phạm đã được bóc tách & sửa chữa:**
   - Gian lận `gold_label` (Oracle Leakage) đã bị xóa hoàn toàn.
   - Cơ chế giả lập thời gian trễ `+18.2ms` và regex giả đã được thay bằng ViSoBERT INT8 ONNX thật.
   - Router 2 tầng đã được sửa lỗi cộng dồn latency 2 lần và đã kích hoạt Tri-State `UNKNOWN`.
   - Bài báo (`main.tex`, `claims.md`) đã đồng bộ chính xác với thực nghiệm McNemar ($b=33, c=3, \chi^2=23.3611$) và chi phí Table VI ($0.3000 cho 2 calls).
2. **Thiết kế lại UI & Phân định năng lực:**
   - **Tier 1 (ViSoBERT INT8 On-device):** Encoder-only, không thể sinh văn bản tự nhiên. UI chỉ hiển thị Điểm rủi ro vô hướng + Bảng kiểm đặc trưng định lượng (URL Whitelist, Urgency regex, OTP) + Cẩm nang SOP tĩnh.
   - **Tier 2 (Forensic Council LLM):** Autoregressive Decoders, hiển thị biên bản tranh biện đối chất của 3 chuyên gia (Tài chính, Tội phạm mạng, Biện hộ khách quan).
   - **Tri-State UNKNOWN:** Khi thiếu dữ liệu hoặc rớt mạng Cloud, hệ thống giữ nguyên tắc Thận trọng Nhận thức (Epistemic Caution), từ chối gán bừa nhãn.
3. **Kế hoạch cho phiên tiếp theo:**
   - Ưu tiên 1: Refactor Frontend Angular (`scamshield-app/UI`) - Sửa types, mock cases, verdict banner, gỡ bỏ hoàn toàn mã án A05 ảo.
   - Ưu tiên 2: Tạo FastAPI bridge nhẹ nối Python pipeline sang Web UI.
   - Ưu tiên 3: Viết script `analyze_error_correlation.py` hoàn thiện phụ lục bài báo.
4. **Quy tắc bất di bất dịch:**
   - Không đụng đến Git.
   - Không dùng Gemini dưới `gemini-3.5-flash`.
   - Hạn chế Claude, chuẩn hóa trên `gpt-6.1-sol` / `gemini-3.8-flash`.
