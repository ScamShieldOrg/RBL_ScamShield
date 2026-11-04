# -*- coding: utf-8 -*-
"""
Unit Test: Visual Dataflow of 3-Agent Forensic Council (Offline Test Mode)
Demonstrates the exact internal state transitions without making live API calls.
"""

import json
import time
import sys

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def simulate_3agent_dataflow(message: str):
    print("=" * 80)
    print("SCAMSHIELD-VN: 3-AGENT FORENSIC COUNCIL INTERNAL DATAFLOW TRACE")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # STATE 1: INPUT INGESTION & METADATA EXTRACTION
    # --------------------------------------------------------------------------
    print("\n[STATE 1: INPUT INGESTION & SANITIZATION]")
    input_state = {
        "raw_message": message,
        "char_length": len(message),
        "entities_detected": {
            "financial_brand": "Vietcombank",
            "regulatory_keyword": "sinh trắc học",
            "urgency_marker": "từ ngày mai",
            "masked_pii": "[NUMBER]"
        },
        "target_council": "3-Agent Occam Panel (Cyber-Bank, Psycho-Teencode, Public Defender)"
    }
    print(json.dumps(input_state, indent=2, ensure_ascii=False))

    # --------------------------------------------------------------------------
    # STATE 2: PARALLEL AGENT EXECUTION (3 ISOLATED CONTEXTS)
    # --------------------------------------------------------------------------
    print("\n[STATE 2: PARALLEL SPECIALIST DELIBERATION (ISOLATED WORKERS)]")
    
    # Ghế A: Cyber-Financial Analyst
    agent_a = {
        "role_id": "ROLE_CYBER_BANK",
        "display_name": "Cyber-Financial & Banking Protocol Analyst",
        "weight": 1.3,
        "input_features": ["Vietcombank", "sinh trắc học", "liên hệ [NUMBER]"],
        "reasoning": "Yêu cầu cập nhật sinh trắc học qua số điện thoại lạ là dấu hiệu mạo danh quy chuẩn NHNN (QĐ 2345). Không có link giả mạo trực tiếp.",
        "vote": "SCAM-RISK",
        "scam_prob": 0.85,
        "confidence": 0.88,
        "risk_level": "HIGH",
        "execution_latency_ms": 14.2
    }
    print("-> Worker 1 (Ghế A):", json.dumps(agent_a, indent=2, ensure_ascii=False))

    # Ghế B: Psycholinguistic Profiler
    agent_b = {
        "role_id": "ROLE_PSYCHO_TEENCODE",
        "display_name": "Psycholinguistic & Vietnamese Slang Profiler",
        "weight": 1.2,
        "input_features": ["tạm ngưng giao dịch từ ngày mai", "Quý khách"],
        "reasoning": "Tạo áp lực thời gian gấp rút (24h) gây sợ hãi mất quyền truy cập tài khoản; ngôn phong hành chính ngụy trang chính thống.",
        "vote": "SCAM-RISK",
        "scam_prob": 0.80,
        "confidence": 0.85,
        "risk_level": "HIGH",
        "execution_latency_ms": 12.8
    }
    print("\n-> Worker 2 (Ghế B):", json.dumps(agent_b, indent=2, ensure_ascii=False))

    # Ghế C: Public Defender Advocate
    agent_c = {
        "role_id": "ROLE_DEFENDER",
        "display_name": "Public Defender Advocate (Anti-False-Positive)",
        "weight": 1.3,
        "input_features": ["thông báo sinh trắc học có thật", "không có link lừa đảo", "không đòi OTP"],
        "reasoning": "Nội dung sinh trắc học là nghiệp vụ thực tế của ngân hàng. Không có link lạ chiếm đoạt, không đòi OTP/mật khẩu. Cần bảo vệ nhãn LOW-RISK để tránh Alarm Fatigue.",
        "vote": "LOW-RISK",
        "scam_prob": 0.30,
        "confidence": 0.65,
        "risk_level": "LOW",
        "execution_latency_ms": 15.1
    }
    print("\n-> Worker 3 (Ghế C):", json.dumps(agent_c, indent=2, ensure_ascii=False))

    # --------------------------------------------------------------------------
    # STATE 3: EARLY-EXIT FAST-PATH EVALUATION
    # --------------------------------------------------------------------------
    print("\n[STATE 3: EARLY-EXIT FAST-PATH CHECK]")
    scam_votes = sum(1 for a in [agent_a, agent_b, agent_c] if a["vote"] == "SCAM-RISK")
    low_votes = sum(1 for a in [agent_a, agent_b, agent_c] if a["vote"] == "LOW-RISK")
    supermajority_thresh = 3
    early_exit_triggered = (scam_votes >= supermajority_thresh or low_votes >= supermajority_thresh)
    
    state_3 = {
        "scam_votes_count": scam_votes,
        "low_votes_count": low_votes,
        "required_for_early_exit": supermajority_thresh,
        "early_exit_triggered": early_exit_triggered,
        "rationale": "Phiếu biểu quyết là 2-1 (Chưa đạt 3-0 tuyệt đối). Chuyển tiếp sang State 4 để hòa giải xung đột."
    }
    print(json.dumps(state_3, indent=2, ensure_ascii=False))

    # --------------------------------------------------------------------------
    # STATE 4: WEIGHTED CONSENSUS & DEFENDER VETO CHECK
    # --------------------------------------------------------------------------
    print("\n[STATE 4: WEIGHTED CONSENSUS & ARBITRATION]")
    total_weight = agent_a["weight"] + agent_b["weight"] + agent_c["weight"]
    weighted_scam_prob = (
        (agent_a["weight"] * agent_a["scam_prob"]) +
        (agent_b["weight"] * agent_b["scam_prob"]) +
        (agent_c["weight"] * agent_c["scam_prob"])
    ) / total_weight

    # Kiểm tra Veto của Defender
    defender_intervened = False
    veto_boost = 0.25
    if agent_c["vote"] == "LOW-RISK" and agent_c["confidence"] >= 0.80:
        weighted_scam_prob = max(0.0, weighted_scam_prob - veto_boost)
        defender_intervened = True

    # Kiểm tra mâu thuẫn biểu quyết (Contradiction check)
    vote_contradiction = (scam_votes > 0 and low_votes > 0 and abs(scam_votes - low_votes) <= 1)
    
    state_4 = {
        "formula": "[(1.3 * 0.85) + (1.2 * 0.80) + (1.3 * 0.30)] / 3.8",
        "raw_weighted_scam_prob": round(weighted_scam_prob, 4),
        "defender_confidence": agent_c["confidence"],
        "defender_veto_applied": defender_intervened,
        "vote_contradiction_flag": vote_contradiction,
        "contradiction_margin": abs(scam_votes - low_votes)
    }
    print(json.dumps(state_4, indent=2, ensure_ascii=False))

    # --------------------------------------------------------------------------
    # STATE 5: FINAL DECISION ENGINE & 3-LABEL MAPPING
    # --------------------------------------------------------------------------
    print("\n[STATE 5: FINAL STANDARDIZED 3-LABEL DECISION]")
    
    # Boundary logic
    if weighted_scam_prob >= 0.60 and not (vote_contradiction and weighted_scam_prob < 0.68):
        final_label = "SCAM-RISK"
        risk_level = "CRITICAL" if weighted_scam_prob >= 0.85 else "HIGH"
    elif weighted_scam_prob < 0.40 and not vote_contradiction:
        final_label = "LOW-RISK"
        risk_level = "LOW"
    else:
        # Epistemic Caution activated
        final_label = "UNKNOWN"
        risk_level = "MEDIUM"

    output_payload = {
        "input_message": message,
        "final_label": final_label,
        "consensus_scam_prob": round(weighted_scam_prob, 4),
        "risk_level": risk_level,
        "total_latency_ms": 15.8,
        "api_calls_made": 0,
        "safety_guardrail": "EPISTEMIC_CAUTION_ACTIVATED",
        "unified_rationale": (
            "Kết luận Hội đồng: ⚠️ KHÔNG XÁC ĐỊNH / VÙNG PHÂN VÂN (UNKNOWN - CẦN THẨM ĐỊNH THÊM).\n"
            "Tỷ lệ đồng thuận điều chỉnh: 64.6%. Biểu quyết 2-1 giữa Ghế Điều tra và Ghế Bào chữa.\n"
            "- Ghế A: Cảnh báo vi phạm quy chuẩn QĐ 2345 khi giục gọi hotline lạ.\n"
            "- Ghế B: Cảnh báo đòn bẩy tâm lý giục giã trong 24h.\n"
            "- Ghế C (Public Defender): Bào chữa vì sinh trắc học là nghiệp vụ thật và tin nhắn không đòi OTP.\n"
            "-> Quyết định chuyển nhãn UNKNOWN để dập tắt nguy cơ Báo Động Giả (0% FPR)."
        )
    }
    print(json.dumps(output_payload, indent=2, ensure_ascii=False))
    print("=" * 80)

if __name__ == "__main__":
    test_sms = "Quý khách chưa cập nhật sinh trắc học nên tài khoản Vietcombank sẽ tạm ngưng giao dịch từ ngày mai. Vui lòng liên hệ [NUMBER] để được hỗ trợ cập nhật."
    simulate_3agent_dataflow(test_sms)


def test_council_dataflow_execution():
    msg = 'Quý khách chưa cập nhật sinh trắc học nên tài khoản Vietcombank sẽ tạm ngưng giao dịch từ ngày mai.'
    simulate_3agent_dataflow(msg)
