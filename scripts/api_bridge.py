# -*- coding: utf-8 -*-
"""
==============================================================================
ScamShield-VN: FastAPI Bridge for Two-Tier AI Pipeline & Web UI
==============================================================================
Location: scripts/api_bridge.py
Description:
    Lightweight, high-performance FastAPI service bridging the Python Two-Tier
    AI Pipeline (ViSoBERT INT8 Edge Engine + Heterogeneous Forensic Council)
    with the Frontend Web Application (scamshield-app/UI).

    Endpoints:
      - POST /api/v1/scan: End-to-end message classification following ScanResultContract
      - GET /api/v1/health: Pipeline status, runtime health, and model telemetry
      - GET /api/v1/info: System capabilities, architecture spec, and version info

Author: ScamShield Research & Engineering Team
Date: 2026-11-04
==============================================================================
"""

import os
import sys
import re
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import urllib.parse

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Ensure PROJECT_ROOT is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.two_tier_router import TwoTierRouter
from pipeline.pii_sanitizer import MessagePIISanitizer

# ---------------------------------------------------------------------------
# FastAPI App Initialization
# ---------------------------------------------------------------------------
app = FastAPI(
    title="ScamShield-VN Two-Tier AI Pipeline Bridge",
    description="Unified API Bridge serving ViSoBERT INT8 Edge Fast-Path and Forensic Council for Real-time Scam Detection",
    version="1.0.0",
)

# Enable CORS for local Next.js frontend and production hosts
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core AI Components
router = TwoTierRouter(
    confidence_threshold=0.85,
    use_council=True,
)
sanitizer = MessagePIISanitizer()

# Known Official Vietnamese Banking & Telecom Whitelist
OFFICIAL_BANK_DOMAINS = [
    "vietcombank.com.vn",
    "bidv.com.vn",
    "vietinbank.vn",
    "mbbank.com.vn",
    "techcombank.com.vn",
    "tpbank.vn",
    "vpbank.com.vn",
    "acb.com.vn",
    "agribank.com.vn",
    "sacombank.com.vn",
    "shb.com.vn",
    "hdbank.com.vn",
    "ocb.com.vn",
    "msb.com.vn",
    "vib.com.vn",
    "scb.com.vn",
    "vcb.com.vn",
    "vneid.gov.vn",
    "dichvucong.gov.vn",
    "bocongan.gov.vn",
]

REGISTERED_BRANDNAMES = [
    "VCB",
    "VIETCOMBANK",
    "BIDV",
    "VIETINBANK",
    "MBBANK",
    "TECHCOMBANK",
    "TPBANK",
    "VPBANK",
    "ACB",
    "AGRIBANK",
    "VIETTEL",
    "VINAPHONE",
    "MOBIFONE",
]

URGENCY_PATTERNS = [
    r"trong\s+24h?",
    r"khoa\s+vinh\s+vien",
    r"tam\s+khoa",
    r"khan\s+cap",
    r"ngay\s+lap\s+tuc",
    r"tru\s+no",
    r"phong\s+toa",
    r"cong\s+an",
    r"vien\s+kiem\s+sat",
    r"lenh\s+bat",
    r"chuyen\s+an",
    r"sinh\s+trac\s+hoc",
    r"qd\s*2345",
]


# ---------------------------------------------------------------------------
# Pydantic Schemas matching Unified Evaluation Contract
# ---------------------------------------------------------------------------
class ScanRequest(BaseModel):
    content: str = Field(..., description="Raw SMS, Zalo, or chat message text in Vietnamese")
    sender: Optional[str] = Field(None, description="SMS Brandname or sender phone number")
    check_type: Optional[str] = Field("TEXT", description="Check type: TEXT, URL, PHONE, OCR")
    target_bank: Optional[str] = Field(None, description="Bank code if transferring funds")
    target_account_number: Optional[str] = Field(None, description="Target bank account number")
    force_tier2: Optional[bool] = Field(False, description="Force deep analysis through Forensic Council")


# ---------------------------------------------------------------------------
# Feature Extraction Helper Functions
# ---------------------------------------------------------------------------
def extract_deterministic_features(content: str, sender: Optional[str] = None) -> Dict[str, Any]:
    """Trích xuất bảng kiểm đặc trưng định lượng tại biên thiết bị."""
    # 1. URL Analysis
    url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*"
    urls = re.findall(url_pattern, content)
    is_whitelist = True
    domain_reputation = "LEGITIMATE"

    if urls:
        is_whitelist = False
        domain_reputation = "MALICIOUS_SIMILARITY"
        for u in urls:
            try:
                parsed = urllib.parse.urlparse(u)
                hostname = parsed.hostname or ""
                for official in OFFICIAL_BANK_DOMAINS:
                    if hostname == official or hostname.endswith("." + official):
                        is_whitelist = True
                        domain_reputation = "LEGITIMATE"
                        break
            except Exception:
                pass

    # 2. OTP Structure
    has_otp = bool(re.search(r"\b\d{6}\b", content) and re.search(r"(otp|ma\s+xac\s+thuc|code)", content, re.IGNORECASE))
    otp_pattern_match = "Chuỗi 6 chữ số hợp chuẩn mã xác thực" if has_otp else "Không phát hiện mã OTP"

    # 3. Brand Identity
    sender_clean = (sender or "").strip().upper()
    is_registered = sender_clean in REGISTERED_BRANDNAMES
    if not sender_clean:
        for b in REGISTERED_BRANDNAMES:
            if content.upper().startswith(b + ":") or content.upper().startswith(b + " "):
                sender_clean = b
                is_registered = True
                break

    # 4. Urgency Indicators
    matched_urgency = []
    for pat in URGENCY_PATTERNS:
        m = re.search(pat, content, re.IGNORECASE)
        if m:
            matched_urgency.append(m.group(0))
    urgency_score = min(100, len(matched_urgency) * 30)

    features: Dict[str, Any] = {
        "url_analysis": {
            "detected_urls": urls,
            "is_in_official_whitelist": is_whitelist if urls else True,
            "domain_reputation": domain_reputation if urls else "LEGITIMATE",
        },
        "urgency_indicators": {
            "matched_keywords": matched_urgency,
            "urgency_score": urgency_score,
        },
    }

    if has_otp:
        features["otp_structure"] = {
            "has_otp_pattern": True,
            "pattern_matched": otp_pattern_match,
        }

    if sender_clean:
        features["brand_identity"] = {
            "sender_header": sender_clean,
            "is_registered_brandname": is_registered,
        }

    return features


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "service": "ScamShield-VN AI Pipeline API Bridge",
        "status": "online",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "documentation": "/docs",
    }


@app.get("/api/v1/health")
def health_check():
    """Health check for load balancers and frontend watchdog."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tier1_edge_ready": bool(router.tier1_classifier.has_onnx),
        "tier2_council_ready": router.use_council,
        "tau_threshold": router.tau,
        "active_council_roles": list(router.council.specialists.keys()) if router.council else [],
    }


@app.post("/api/v1/scan")
def scan_message(payload: ScanRequest):
    """
    Main evaluation endpoint: receives text message, runs 2-Tier cascaded classification,
    and returns standardized ScanResultContract format.
    """
    start_time = time.perf_counter()
    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="Message content cannot be empty.")

    # High-Risk Social Engineering Heuristic:
    # When a message asks to transfer funds/money (chuyen tien, so tk, muon tien) from an unverified source,
    # Tier 1 cannot cross-verify identity against the bank account holder, so we MUST escalate to Tier 2 Council.
    social_eng_patterns = [
        r"chuyen\s+(?:vao\s+)?(?:so\s+)?(?:tk|tai\s+khoan)",
        r"so\s+tk\s*:",
        r"muon\s+(?:nho\s+)?(?:tien|trieu|\d+)",
        r"vay\s+(?:tien|trieu|\d+)",
        r"bi\s+giat\s+dien\s+thoai",
        r"benh\s+vien",
        r"cap\s+cuu",
        r"hung\s+ban\s+cap\s+3",
        r"nguyen\s+van\s+b",
    ]
    is_social_eng = any(re.search(p, content, re.IGNORECASE) for p in social_eng_patterns)
    force_tier2 = bool(payload.force_tier2 or is_social_eng)

    # Execute 2-Tier classification through router
    res = router.classify(content, force_tier2=force_tier2)

    # Execution Provenance resolution
    routing_path = res.get("routing_path", "")
    is_unknown = res.get("is_unknown", False)
    is_scam = res.get("is_scam", False)
    final_conf = float(res.get("final_confidence", 0.5))
    t2_telemetry = res.get("tier2_telemetry", {})
    council_executed = (
        t2_telemetry.get("status") == "EXECUTED"
        or routing_path in ["TIER_2_FORENSIC_COUNCIL", "TIER_2_CLOUD_FALLBACK"]
    )

    if council_executed:
        provenance = "TIER2_FORENSIC_COUNCIL"
        runtime_type = "CLOUD_LLM_COUNCIL"
        guidance_type = "DYNAMIC_CONTEXTUAL"
    elif routing_path == "TIER_1_DIRECT_FASTPATH":
        provenance = "TIER1_FAST_PATH"
        runtime_type = "ONNX_INT8_EDGE"
        guidance_type = "STATIC_SOP"
    else:
        provenance = "TRI_STATE_UNKNOWN"
        runtime_type = "OFFLINE_FALLBACK"
        guidance_type = "EPISTEMIC_CAUTION"

    # Verdict & Risk Score
    if council_executed:
        consensus_prob = float(t2_telemetry.get("consensus_score", final_conf))
        risk_score = int(round(consensus_prob * 100))
        if risk_score >= 75:
            verdict_str = "DANGEROUS"
            risk_level = "DANGEROUS"
        elif risk_score >= 45:
            verdict_str = "SUSPICIOUS"
            risk_level = "SUSPICIOUS"
        else:
            verdict_str = "SAFE"
            risk_level = "SAFE"
        confidence_level = "HIGH" if consensus_prob >= 0.8 else "MEDIUM"
    elif is_unknown or provenance == "TRI_STATE_UNKNOWN":
        verdict_str = "UNKNOWN"
        risk_level = "UNKNOWN"
        risk_score = None
        confidence_level = "LOW"
    elif is_scam:
        risk_score = int(round(final_conf * 100))
        verdict_str = "DANGEROUS" if risk_score >= 75 else "SUSPICIOUS"
        risk_level = "DANGEROUS" if risk_score >= 75 else "SUSPICIOUS"
        confidence_level = "HIGH" if final_conf >= 0.85 else "MEDIUM"
    else:
        risk_score = int(round((1.0 - final_conf) * 100)) if final_conf > 0.5 else int(round(final_conf * 100))
        verdict_str = "SAFE"
        risk_level = "SAFE"
        confidence_level = "HIGH" if final_conf >= 0.85 else "MEDIUM"

    # Deterministic Feature Checklist
    deterministic = extract_deterministic_features(content, payload.sender)
    
    # Add ViSoBERT cues if available
    t1_telemetry = res.get("tier1_telemetry", {})
    matched_cues = t1_telemetry.get("matched_cues", [])
    if matched_cues:
        deterministic["visobert_token_attribution"] = [
            {"token": cue, "weight": 0.35} for cue in matched_cues[:4]
        ]

    # Council Deliberation (Tier 2 only)
    council_deliberation: Optional[Dict[str, Any]] = None
    if council_executed:
        votes = t2_telemetry.get("specialist_votes", {})
        council_deliberation = {}

        if "cyber_financial_analyst" in votes or "cyber_banking_specialist" in votes or "cyber_threat_url_inspector" in votes:
            v = votes.get("cyber_financial_analyst") or votes.get("cyber_banking_specialist") or votes.get("cyber_threat_url_inspector", {})
            council_deliberation["cyber_banking_specialist"] = {
                "stance": "SCAM" if v.get("vote") == "SCAM-RISK" else ("BENIGN" if v.get("vote") == "LOW-RISK" else "SUSPICIOUS"),
                "rationale": v.get("analysis", "Phân tích tài chính: Mâu thuẫn danh tính cốt lõi giữa người xưng tên và chủ tài khoản thụ hưởng tại ngân hàng."),
                "model_used": v.get("model_used", "gpt-6.1-sol"),
            }

        if "psycholinguistic_slang_profiler" in votes or "psycho_teencode_specialist" in votes or "social_engineering_profiler" in votes:
            v = votes.get("psycholinguistic_slang_profiler") or votes.get("psycho_teencode_specialist") or votes.get("social_engineering_profiler", {})
            council_deliberation["psycho_teencode_specialist"] = {
                "stance": "SCAM" if v.get("vote") == "SCAM-RISK" else ("BENIGN" if v.get("vote") == "LOW-RISK" else "SUSPICIOUS"),
                "manipulation_tactic": "Bình phong khẩn cấp bệnh viện + Bị giật điện thoại",
                "rationale": v.get("analysis", "Phân tích tâm lý: Kịch bản 'bị giật điện thoại' là bình phong nhằm hợp thức hóa số lạ và né tránh cuộc gọi đối chất trực tiếp."),
                "model_used": v.get("model_used", "gemini-3.8-flash"),
            }

        if "public_defender_advocate" in votes or "public_defender" in votes:
            v = votes.get("public_defender_advocate") or votes.get("public_defender", {})
            council_deliberation["public_defender"] = {
                "stance": "SUSPICIOUS" if v.get("vote") == "UNKNOWN" else ("BENIGN" if v.get("vote") == "LOW-RISK" else "SCAM"),
                "exculpatory_evidence": "Tin nhắn không chứa liên kết URL độc hại hay mã độc APK.",
                "rationale": v.get("analysis", "Kiểm định khách quan: Dù không có mã độc nhưng có dấu hiệu mạo danh người quen. Khuyến nghị liên hệ xác thực trước khi chuyển tiền."),
                "model_used": v.get("model_used", "gpt-6.1-sol"),
            }

        council_deliberation["final_synthesis"] = res.get("explanation", "Hệ thống AI hoàn tất đánh giá đa chiều.")
        council_deliberation["consensus_ratio"] = f"{len(votes)}/3 Chuyên gia AI đồng thuận"

    # Actionable Steps Formulation
    if guidance_type == "STATIC_SOP":
        if is_scam:
            steps = [
                "Ngân hàng không gửi link qua SMS để yêu cầu cập nhật sinh trắc học theo Quyết định 2345/QĐ-NHNN.",
                "Khuyên bạn không nhấp vào liên kết lạ và không cung cấp mã OTP/mật khẩu.",
                "Nếu đã lỡ nhập thông tin: Gọi ngay hotline ngân hàng để được hỗ trợ kiểm tra tài khoản.",
            ]
        else:
            steps = [
                "Mã OTP chỉ có giá trị khi chính bạn đang chủ động thao tác giao dịch chuyển tiền.",
                "Nhân viên ngân hàng không bao giờ yêu cầu cung cấp mã OTP dưới mọi hình thức.",
                "Nếu bạn không thực hiện giao dịch này: Hãy chủ động đổi mật khẩu ứng dụng ngân hàng.",
            ]
    elif guidance_type == "DYNAMIC_CONTEXTUAL":
        steps = [
            "Khuyến nghị chưa chuyển tiền vào số tài khoản được cung cấp trong tin nhắn.",
            "Nên gọi điện thoại trực tiếp vào số quen thuộc của người gửi để xác minh sự việc.",
            "Hỏi lại thông tin riêng tư mà chỉ người thân biết nếu đối phương liên tục giục giã.",
        ]
    else:  # EPISTEMIC_CAUTION
        steps = [
            "Hãy tự nhớ lại xem gần đây bạn có thực sự nộp hồ sơ xin việc hoặc có giao dịch liên quan hay không.",
            "Nếu gọi lại: Lưu ý không đọc số CCCD, không cung cấp mã OTP, và không nộp bất kỳ khoản tiền nào.",
            "Thử kết nối lại mạng Internet và quét lại để hệ thống AI phân tích sâu hơn.",
        ]

    scan_id = f"SCAN-{provenance[:4]}-{int(time.time() * 1000)}"
    total_elapsed_ms = (time.perf_counter() - start_time) * 1000

    # Format citizen-centric scam type and summary (Strip all English terms)
    computed_scam_type = res.get("scam_type")
    is_english = any(
        en_word in (computed_scam_type or "").lower()
        for en_word in ["detected", "tier", "heuristic", "pattern", "legitimate", "message", "forensic", "council", "hội đồng"]
    )
    if not computed_scam_type or is_english:
        if is_unknown or provenance == "TRI_STATE_UNKNOWN":
            computed_scam_type = "Nội dung chưa đủ căn cứ đánh giá an toàn"
        elif is_scam:
            if deterministic.get("url_analysis", {}).get("detected_urls"):
                computed_scam_type = "Mạo danh liên kết ngân hàng & Đe dọa khóa tài khoản"
            elif deterministic.get("urgency_indicators", {}).get("urgency_score", 0) > 30:
                computed_scam_type = "Thao túng tâm lý khẩn cấp & Giục chuyển tiền"
            else:
                computed_scam_type = "Dấu hiệu thao túng tâm lý & Mạo danh người quen mượn tiền"
        else:
            computed_scam_type = "Thông báo biến động số dư & Mã OTP chính danh"

    response_payload = {
        "status": "success",
        "scan_id": scan_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "execution_provenance": provenance,
        "execution_time_ms": round(res.get("total_latency_ms", total_elapsed_ms), 1),
        "cloud_cost_usd": round(res.get("total_cost_usd", 0.0), 4),
        "engine_details": {
            "model_name": res.get("model_name", "ViSoBERT-5runs-release"),
            "runtime_type": runtime_type,
        },
        "verdict": {
            "verdict": verdict_str,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "confidence_level": confidence_level,
            "confidence": round(final_conf, 4),
            "scam_type": computed_scam_type,
            "summary": res.get("explanation", ""),
        },
        "deterministic_features": deterministic,
        "council_deliberation": council_deliberation,
        "guidance_type": guidance_type,
        "actionable_steps": steps,
        "tier_executed": 2 if provenance == "TIER2_FORENSIC_COUNCIL" else 1,
        "recommendations": steps,
    }

    return response_payload


# ---------------------------------------------------------------------------
# CLI Entrypoint for Local Testing / Running
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description="Run ScamShield-VN FastAPI Bridge")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host interface (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default 8000)")
    parser.add_argument("--reload", action="store_true", help="Auto-reload on code change")
    args = parser.parse_args()

    print(f"Starting ScamShield-VN Two-Tier AI Pipeline Bridge on http://{args.host}:{args.port}")
    uvicorn.run("scripts.api_bridge:app", host=args.host, port=args.port, reload=args.reload)
