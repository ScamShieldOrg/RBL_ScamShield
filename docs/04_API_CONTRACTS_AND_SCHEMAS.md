# 04. API CONTRACTS & SCHEMAS — HỢP ĐỒNG DỮ LIỆU FRONTEND & BACKEND

Tài liệu này là **Quy chuẩn Giao tiếp Kỹ thuật (Data Contract)** giữa giao diện người dùng (Frontend React do bạn phát triển) và dịch vụ máy chủ (Backend Spring Boot của Huy Nguyễn & Auth API của Hoàng Trân).

---

## 1. Tiêu Chuẩn Chung

* **Base URL:** `http://localhost:8080/api/v1` (Môi trường Local Dev) hoặc `https://api.scamshield.vn/api/v1` (Production).
* **Định dạng dữ liệu:** `application/json; charset=utf-8`.
* **Xác thực:** Header `Authorization: Bearer <JWT_TOKEN>` cho các tính năng người dùng đã đăng ký (`REGISTERED_USER`). Khách vãng lai (`GUEST`) có thể gọi endpoint `/scan` với hạn mức giới hạn (Rate-limited by IP).

---

## 2. Chi Tiết Các Endpoint Trọng Tâm

### 2.1. Kiểm Tra Lừa Đảo Trực Tiếp (SCRUM-12: Register User Check Scam)
* **Endpoint:** `POST /api/v1/scan`
* **Quyền:** `PUBLIC` (với hạn ngạch) hoặc `USER` (đầy đủ phân tích Council).

#### Request Payload:
```json
{
  "content": "string (nội dung tin nhắn / văn bản cần quét)",
  "sender": "string (số điện thoại hoặc Brandname gửi đến, có thể null)",
  "check_type": "TEXT", // Enum: "TEXT" | "URL" | "PHONE" | "BANK_ACCOUNT"
  "target_bank": "VCB", // Tùy chọn, mã ngân hàng (nếu check_type là BANK_ACCOUNT)
  "target_account_number": "1029384756" // Tùy chọn
}
```

#### Response Payload (200 OK):
```json
{
  "status": "success",
  "data": {
    "scan_id": "SC-20261005-0012",
    "timestamp": "2026-10-05T08:30:00Z",
    "tier_executed": 2, // 1: ViSoBERT On-Device | 2: Cloud 3-Agent Council
    "verdict": {
      "risk_level": "CRITICAL", // "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
      "final_label": "SCAM-RISK", // "SCAM-RISK" | "LOW-RISK" | "UNKNOWN"
      "risk_score": 96.5, // 0.0 -> 100.0
      "scam_category": "Mạo danh Cơ quan Nhà nước / Thuế (Phishing & Extortion)",
      "confidence": 0.98,
      "summary": "Tin nhắn giả danh Cục Thuế nhằm đe dọa người dùng truy cập link giả mạo đánh cắp tài sản."
    },
    "radar_metrics": {
      "urgency": 95,
      "authority_impersonation": 98,
      "financial_lure": 80,
      "suspicious_channel": 92,
      "data_harvesting": 90
    },
    "council_breakdown": {
      "architecture": "Consolidated 3-Agent Heterogeneous Council",
      "consensus_ratio": "3/3",
      "lead_model": "gpt-6.1-sol",
      "early_exit_triggered": true,
      "agents": [
        {
          "seat": "Seat A (cyber_financial_analyst)",
          "role_id": "ROLE_CYBER_BANK",
          "verdict": "SCAM-RISK",
          "scam_prob": 0.98,
          "finding": "Tên miền vneid-thuetphcm.com giả mạo cơ quan nhà nước, vi phạm quy chuẩn cổng dịch vụ công."
        },
        {
          "seat": "Seat B (psycholinguistic_slang_profiler)",
          "role_id": "ROLE_PSYCHO_TEENCODE",
          "verdict": "SCAM-RISK",
          "scam_prob": 0.95,
          "finding": "Cưỡng ép tâm lý hoảng sợ bằng kỳ hạn 24 giờ và dọa phong tỏa tài khoản."
        },
        {
          "seat": "Seat C (public_defender_advocate)",
          "role_id": "ROLE_DEFENDER",
          "verdict": "SCAM-RISK",
          "scam_prob": 0.92,
          "finding": "Không tìm thấy căn cứ thông báo hành chính hợp pháp; đối chiếu quy chuẩn xác định nguy cơ lừa đảo cao."
        }
      ]
    },
    "actionable_recommendations": [
      "Tuyệt đối không nhấp vào đường liên kết.",
      "Không cung cấp số CCCD, tài khoản ngân hàng hoặc mã OTP.",
      "Thông báo ngay cho người thân và nhấn nút 'Báo cáo lừa đảo' để bảo vệ cộng đồng."
    ]
  }
}
```

---

### 2.2. Danh Sách Lịch Sử Quét (SCRUM-13: Scam Check History)
* **Endpoint:** `GET /api/v1/history`
* **Query Parameters:**
  * `page` (int, default: 1)
  * `limit` (int, default: 10)
  * `filter_risk` (string, optional: `ALL` | `DANGEROUS` | `SUSPICIOUS` | `SAFE`)
  * `search` (string, optional: từ khóa tìm kiếm trong nội dung hoặc số gửi)

#### Response Payload (200 OK):
```json
{
  "status": "success",
  "pagination": {
    "current_page": 1,
    "limit": 10,
    "total_records": 34,
    "total_pages": 4
  },
  "data": [
    {
      "id": "SC-20261005-0012",
      "created_at": "2026-10-05T08:30:00Z",
      "check_type": "TEXT",
      "snippet": "Cuc Thue TP.HCM thong bao: Quy khach con no thue 3.200.000d...",
      "sender": "0981234567",
      "risk_level": "DANGEROUS",
      "risk_score": 96.5,
      "scam_category": "Mạo danh Cục Thuế"
    },
    {
      "id": "SC-20261003-4412",
      "created_at": "2026-10-03T09:15:00Z",
      "check_type": "URL",
      "snippet": "https://vietcombank-login-security.net",
      "sender": null,
      "risk_level": "DANGEROUS",
      "risk_score": 99.0,
      "scam_category": "Phishing Vietcombank"
    },
    {
      "id": "SC-20261002-1102",
      "created_at": "2026-10-02T14:20:00Z",
      "check_type": "TEXT",
      "snippet": "Chuc mung ban da trung thuong voucher 500k tu Shopee...",
      "sender": "Shopee Mall",
      "risk_level": "SUSPICIOUS",
      "risk_score": 62.0,
      "scam_category": "Tiếp thị nghi vấn"
    },
    {
      "id": "SC-20261001-0810",
      "created_at": "2026-10-01T08:10:00Z",
      "check_type": "PHONE",
      "snippet": "02838295115",
      "sender": "02838295115",
      "risk_level": "SAFE",
      "risk_score": 5.0,
      "scam_category": "Tổng đài chính thức"
    }
  ]
}
```

---

### 2.3. Báo Cáo Lừa Đảo Cho Cộng Đồng (SCRUM-14: Submit Scam Report)
* **Endpoint:** `POST /api/v1/reports`

#### Request Payload:
```json
{
  "target_type": "URL", // "PHONE" | "URL" | "BANK_ACCOUNT" | "SMS"
  "target_value": "https://vneid-thuetphcm.com",
  "category": "Mạo danh cơ quan nhà nước",
  "description": "Nhận tin nhắn giả danh cục thuế gửi qua đầu số lạ, yêu cầu thanh toán phạt nợ thuế.",
  "loss_amount": 0,
  "evidence_image_urls": [
    "https://storage.scamshield.vn/uploads/evidence-1.jpg"
  ]
}
```

#### Response (201 Created):
```json
{
  "status": "success",
  "message": "Báo cáo đã được tiếp nhận và đưa vào hàng chờ kiểm duyệt.",
  "report_id": "REP-20261005-7789"
}
```

---

### 2.4. Theo Dõi Tiến Độ Báo Cáo (SCRUM-15: Report Tracking)
* **Endpoint:** `GET /api/v1/reports/tracking`

#### Response Payload (200 OK):
```json
{
  "status": "success",
  "data": [
    {
      "report_id": "REP-20261005-7789",
      "created_at": "2026-10-05T09:00:00Z",
      "target_value": "https://vneid-thuetphcm.com",
      "target_type": "URL",
      "status": "AI_ANALYZING", // "PENDING" | "AI_ANALYZING" | "VERIFIED_SCAM" | "REJECTED"
      "status_label": "Hội đồng AI đang đối soát dữ liệu",
      "moderator_notes": null
    },
    {
      "report_id": "REP-20260928-1123",
      "created_at": "2026-09-28T14:15:00Z",
      "target_value": "0912998877",
      "target_type": "PHONE",
      "status": "VERIFIED_SCAM",
      "status_label": "Đã xác thực lừa đảo & cập nhật Blacklist toàn hệ thống",
      "moderator_notes": "Số điện thoại giả danh CSGT phạt nguội. Đã được ghi nhận vào NCSC Blacklist."
    }
  ]
}
```
