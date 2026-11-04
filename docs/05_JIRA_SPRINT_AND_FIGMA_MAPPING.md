# 05. JIRA SPRINT & FIGMA MAPPING — CHI TIẾT CÁC MÀN HÌNH SPRINT 0

Tài liệu này tổng hợp toàn bộ thông tin chi tiết về **4 màn hình được giao cho Nguyễn Trung Hiếu** trong **SCRUM Sprint 0** (30/09/2026 – 14/10/2026), bao gồm liên kết Figma, thiết kế giao diện (UI Specs), hành vi trải nghiệm (UX Flow) và checklist nghiệm thu (Definition of Done).

---

## 1. Bảng Kế Hoạch Thực Hiện Của Hiếu

| Mã Ticket | Tên màn hình | Hạn chót (Due) | Figma Node ID | Mức độ ưu tiên | Trạng thái hiện tại |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **SCRUM-12** | **Register User Check Scam** | **2026-10-05 (GẤP)** | [`2012-25`](https://www.figma.com/design/nSTfJq0bQ7b6ndY1G7Bx3w/ScamShield-UI?node-id=2012-25) | 🔴 Cao nhất | `To Do` / Cần dựng ngay |
| **SCRUM-13** | **Scam Check History** | **2026-10-05 (GẤP)** | [`2012-333`](https://www.figma.com/design/nSTfJq0bQ7b6ndY1G7Bx3w/ScamShield-UI?node-id=2012-333) | 🔴 Cao nhất | `To Do` / Cần dựng ngay |
| **SCRUM-14** | **Submit Scam Report** | **2026-10-07** | [`2012-886`](https://www.figma.com/design/nSTfJq0bQ7b6ndY1G7Bx3w/ScamShield-UI?node-id=2012-886) | 🟡 Trung bình | `To Do` |
| **SCRUM-15** | **Report Tracking** | **2026-10-07** | [`2012-1906`](https://www.figma.com/design/nSTfJq0bQ7b6ndY1G7Bx3w/ScamShield-UI?node-id=2012-1906) | 🟡 Trung bình | `To Do` |

* **Link Master Figma Project:** `https://www.figma.com/design/nSTfJq0bQ7b6ndY1G7Bx3w/ScamShield-UI`

---

## 2. Chi Tiết Từng Màn Hình

### 2.1. SCRUM-12: Màn Hình "Register User Check Scam" (Figma Node `2012-25`)

Màn hình cốt lõi nhất của ứng dụng, nơi người dùng đã đăng nhập nhập nội dung để hệ thống chạy suy luận 2 tầng.

#### Các thành phần giao diện (UI Components):
1. **Header & User Welcome:** Hiển thị tên người dùng và hạn ngạch quét chuyên sâu còn lại trong ngày.
2. **Tab chuyển đổi loại dữ liệu (Input Mode Selector):**
   * *Tab 1 (Mặc định):* Tin nhắn văn bản (SMS / Tin nhắn Zalo, Telegram, Facebook).
   * *Tab 2:* Đường link liên kết (URL / Domain).
   * *Tab 3:* Số điện thoại / Số tài khoản ngân hàng.
3. **Khu vực nhập liệu (Input Area):**
   * Ô `textarea` lớn với placeholder hướng dẫn rõ ràng.
   * Nút bấm nhanh: *"Dán từ bộ nhớ tạm (Paste)"* và *"Xóa nội dung"*.
   * Ô nhập số người gửi (Sender) tùy chọn.
4. **Nút kích hoạt (CTA Button):**
   * Nút *"Phân Tích Bằng AI"* với hiệu ứng gradient nổi bật.
   * Trạng thái Loading: Hiển thị thanh tiến trình 2 tầng (*"Đang kiểm tra Tier 1 Edge..."* $\rightarrow$ *"Hội đồng AI Tier 2 đang thẩm định..."*).
5. **Thẻ kết quả phán quyết (Verdict Result Card):**
   * Điểm rủi ro tổng hợp (Risk Score $0 - 100$) dạng Gauge hoặc Vòng tròn lớn.
   * Huy hiệu phân loại:
     * `🟢 AN TOÀN` (Điểm < 30)
     * `🟡 NGHI VẤN` (Điểm 30 - 75)
     * `🔴 NGUY HIỂM / LỪA ĐẢO` (Điểm > 75)
   * Tóm tắt nguyên nhân bằng tiếng Việt dễ hiểu cho người lớn tuổi.
6. **Biểu đồ Radar 5 Trục (Radar Risk Chart):**
   * Trực quan hóa 5 yếu tố: Ép buộc thời gian, Mạo danh cơ quan, Bẫy tài chính, Kênh nghi vấn, Ý đồ thu thập dữ liệu.
7. **Chi tiết Hội đồng 3 AI Hợp Nhất (Council Breakdown Accordion):**
   * Tỷ lệ đồng thuận (ví dụ: `3/3 ĐỒNG THUẬN` hoặc `2/1 PHÂN VÂN -> UNKNOWN`).
   * Danh sách quan điểm rút gọn của 3 chuyên gia:
     1. Chuyên gia An ninh Mạng & Quy trình Ngân hàng (cyber_financial_analyst)
     2. Chuyên gia Tâm lý Tội phạm & Biến thể Ngôn ngữ (psycholinguistic_slang_profiler)
     3. Luật sư Bào chữa Công cộng chống báo động giả (public_defender_advocate)
8. **Hành động tiếp theo (Actions):**
   * Nút *"Báo cáo ngay vào Blacklist"* (chuyển tiếp sang màn hình SCRUM-14 kèm nội dung điền sẵn).
   * Nút *"Lưu vào Lịch sử"* hoặc *"Chia sẻ cảnh báo cho người thân"*.

---

### 2.2. SCRUM-13: Màn Hình "Scam Check History" (Figma Node `2012-333`)

Màn hình lưu trữ toàn bộ các lần quét trước đó của tài khoản người dùng, phục vụ việc tra cứu lại và theo dõi biến động rủi ro.

#### Các thành phần giao diện:
1. **Bộ lọc và Tìm kiếm (Filter & Search Bar):**
   * Ô tìm kiếm từ khóa theo nội dung hoặc số gửi.
   * Bộ lọc theo mức độ rủi ro: `Tất cả` | `Nguy hiểm (Đỏ)` | `Nghi vấn (Vàng)` | `An toàn (Xanh)`.
2. **Danh sách thẻ lịch sử (History Cards List):**
   * Mỗi mục gồm:
     * Icon loại kiểm tra (Icon tin nhắn, link, số điện thoại).
     * Thời gian quét (ví dụ: *"10 phút trước"*, *"03/10/2026 14:30"*).
     * Trích đoạn nội dung (Snippet 2 dòng).
     * Badge mức độ nguy hiểm và điểm số (ví dụ: `🔴 96.5% - Mạo danh Cục Thuế`).
3. **Modal xem chi tiết (Scan Detail Modal):**
   * Nhấp vào bất kỳ mục nào sẽ hiển thị lại toàn bộ bản phân tích Radar và lời khuyên phòng tránh của lần quét đó.
4. **Phân trang (Pagination Controls):** Next, Prev, số trang.

---

### 2.3. SCRUM-14: Màn Hình "Submit Scam Report" (Figma Node `2012-886`)

Màn hình đóng góp dữ liệu cho mạng lưới Blacklist cộng đồng (Crowdsourced Intelligence).

#### Các thành phần giao diện:
1. **Lựa chọn loại đối tượng báo cáo:** Số điện thoại | Đường link (URL) | Số tài khoản ngân hàng | Tin nhắn mạo danh.
2. **Thông tin đối tượng:** Nhập chính xác số điện thoại, link lừa đảo hoặc số tài khoản + tên ngân hàng.
3. **Danh mục thủ đoạn lừa đảo (Category Select):**
   * Giả danh công an / cơ quan nhà nước.
   * Lừa đảo tuyển dụng / việc làm online.
   * Lừa đảo đầu tư tài chính / tiền ảo.
   * Bẫy trúng thưởng / voucher giả.
   * Mạo danh người thân mượn tiền.
4. **Mô tả chi tiết & Số tiền thiệt hại (nếu có):** Textarea mô tả quá trình bị tiếp cận.
5. **Đính kèm bằng chứng (File/Image Upload):** Cho phép tải lên ảnh chụp màn hình tin nhắn, biên lai chuyển khoản.
6. **Cam kết thông tin:** Checkbox xác nhận thông tin trung thực trước khi gửi duyệt.

---

### 2.4. SCRUM-15: Màn Hình "Report Tracking" (Figma Node `2012-1906`)

Màn hình giúp người dùng theo dõi vòng đời xử lý báo cáo của mình sau khi gửi lên hệ thống.

#### Các trạng thái vòng đời (Lifecycle States):
1. `PENDING (Chờ tiếp nhận):` Báo cáo đã gửi thành công vào hàng đợi.
2. `AI_ANALYZING (Hội đồng AI thẩm tra):` Hệ thống đối soát tự động với cơ sở dữ liệu NCSC và quét lặp.
3. `VERIFIED_SCAM (Đã xác thực & Đưa vào Blacklist):` Báo cáo được duyệt, cộng điểm uy tín cho người dùng (Gamification đóng góp cộng đồng).
4. `REJECTED (Từ chối):` Báo cáo thiếu căn cứ hoặc không phải lừa đảo, kèm ghi chú phản hồi từ kiểm duyệt viên (Moderator).
