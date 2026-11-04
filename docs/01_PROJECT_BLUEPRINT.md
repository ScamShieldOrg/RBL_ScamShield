# 01. PROJECT BLUEPRINT — BẢN THIẾT KẾ TỔNG THỂ SCAMSHIELD-VN

> **Đề tài Capstone:** FA26SE079 — ScamShield: Scam Message and Call Detection Platform  
> **Phương pháp nghiên cứu:** Research-Based Learning (RBL) & Systematic Literature Review (PRISMA 2020)  
> **Thành viên nghiên cứu & phát triển:** Nguyễn Trung Hiếu (`cristand2825@gmail.com`)  
> **Team size:** 5 thành viên (Hiếu, Huy, Phúc, Trân, Quang)

---

## 1. Bối Cảnh Thực Tiễn & Tầm Nhìn Dự Án

Tại Việt Nam, các chiến dịch lừa đảo trực tuyến và viễn thông (Smishing, Vishing, Phishing, mạo danh cơ quan công quyền, lừa đảo việc làm, thao túng đầu tư tài chính) đang bùng nổ với tốc độ chưa từng có. Các thủ đoạn ngày càng tinh vi với công nghệ Deepfake, mã độc giả mạo ứng dụng chính phủ (như VNeID giả, Dịch vụ công giả mạo) và hạ tầng kỹ thuật rửa tiền xuyên biên giới.

### Vấn đề cốt lõi của các giải pháp hiện tại:
1. **Ứng dụng tĩnh (Static Blockers):** Chỉ dựa trên Blacklist thủ công hoặc các mô hình Machine Learning / Regex cổ điển. Không thể bắt kịp các kịch bản lừa đảo biến tướng zero-day.
2. **LLM đơn lẻ (Single Cloud LLMs):** Tốn kém chi phí API, độ trễ phản hồi cao (3 - 10 giây), phụ thuộc hoàn toàn vào kết nối mạng, nguy cơ rò rỉ dữ liệu nhạy cảm của người dùng (Privacy concerns), và dễ bị ảo giác (hallucination) hoặc bị lừa ngược bởi Jailbreak prompt.
3. **Thiếu khả năng giải thích minh bạch (Black-box AI):** Chỉ đưa ra nhãn "Spam/Ham" mà không chỉ rõ cho nạn nhân *vì sao* đây là bẫy lừa đảo, dẫn đến người dân vẫn rơi vào bẫy tâm lý sợ hãi hoặc lòng tham.

### Sứ mệnh của ScamShield-VN:
Xây dựng một hệ sinh thái phòng vệ đa tầng toàn diện gồm:
* **Ứng dụng di động & Web cho người dân (ScamShield App):** Quét nhanh tin nhắn, link, số điện thoại, số tài khoản; trực quan hóa mức độ nguy hiểm qua Radar 5 trục và cảnh báo tức thì.
* **Mạng lưới Trí tuệ Đe dọa Đóng kín (Closed-Loop Threat Intelligence):** Tiếp nhận báo cáo lừa đảo từ cộng đồng, quy trình kiểm duyệt (Moderator Workflow), liên thông dữ liệu cảnh báo thời gian thực.
* **Lõi suy luận AI 2 Tầng (Two-Tier Hybrid Pipeline):** Kết hợp mô hình ngôn ngữ tiếng Việt On-Device nhỏ gọn (PhoBERT/ViSoBERT) và Hội đồng Đa LLM Giám định Độc lập (Consolidated 3-Agent Multi-LLM Forensic Council).

---

## 2. Bản Đồ Phân Công Đội Ngũ (Jira Scrum Board)

| Thành viên | Trách nhiệm RBL / Nghiên cứu | Trách nhiệm Sản phẩm / App (Sprint 0) | Jira Tickets |
| :--- | :--- | :--- | :--- |
| **Nguyễn Trung Hiếu** *(Chủ repo này)* | **Core Deep Learning & Transformer:** PhoBERT-base, ViSoBERT, XAI Frameworks, Kiến trúc 2 tầng & Hội đồng 3 LLMs (Consolidated 3-Agent Council) | **User Check Scam UI, Scan History, Submit Scam Report & Report Tracking** | **SCRUM-12, SCRUM-13, SCRUM-14, SCRUM-15** |
| **Quang Nguyễn** | Edge Computing & Mobile Optimization (ONNX Runtime, Quantization INT8) | Setup Frontend React, Auth Screens UI, Community Blacklist Screen | SCRUM-1, SCRUM-6, SCRUM-11 |
| **Huy Nguyễn** | Threat Intelligence, Crowdsourced Moderation Loop, Database deduplication | Setup Backend Spring Boot, Normal & Partner Register APIs | SCRUM-2, SCRUM-16, SCRUM-17 |
| **Phan Trần Hoàng Trân** | Data Imbalance & Feature Engineering (SMOTE, Synthetic Data, Resampling) | Backend Auth APIs, JWT Security, Role-Based Access Control (RBAC) | SCRUM-5 |
| **Hoàng Hải Phúc** | LLM Prompt Optimization, In-Context Learning, Synthetic Phishing Generation | Guest Check Scam Flow, Scam Dashboard, Education Hub, Gamification Leaderboard | SCRUM-7, SCRUM-8, SCRUM-9, SCRUM-10 |

---

## 3. Kiến Trúc Hệ Thống Tổng Thể

```
[ Người Dùng Web / Mobile ]
            │
            ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   GIAO DIỆN SCAMSHIELD (React Vite)                     │
│  - Màn hình Kiểm tra lừa đảo (SCRUM-12)                                │
│  - Màn hình Lịch sử kiểm tra (SCRUM-13)                                │
│  - Màn hình Báo cáo lừa đảo đóng góp cộng đồng (SCRUM-14)              │
│  - Màn hình Theo dõi tiến độ báo cáo (SCRUM-15)                        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / REST API (JWT)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               BACKEND GATEWAY (Spring Boot / FastAPI)                  │
│  - Định tuyến phân quyền (RBAC), Quản lý Session & Rate Limit          │
│  - Bộ điều hợp kết nối Threat DB & Deduplication                       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   LÕI TRÍ TUỆ NHÂN TẠO 2 TẦNG (TWO-TIER AI)            │
│                                                                        │
│  [ TẦNG 1: On-Device / Edge Screener ]                                 │
│  - PhoBERT-base / ViSoBERT ONNX (< 50ms, Offline, Confidence >= 0.90)  │
│                                                                        │
│  [ TẦNG 2: Cloud Forensic Council - 3 Chuyên Gia AI Hợp Nhất ]         │
│  - Kích hoạt khi Tầng 1 mập mờ (Confidence < 0.90)                     │
│  - Hội đồng: Cyber-Financial, Psycholinguistic-Teencode, Public Defender│
│  - Trọng tài Consensus Engine + Cơ chế Veto dập tắt Alarm Fatigue       │
└────────────────────────────────────────────────────────────────────────┘
```
