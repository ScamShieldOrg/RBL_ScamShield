# -*- coding: utf-8 -*-
"""
Unit test for 3-Agent Forensic Council consensus and veto bounds.
Tests:
1. Investigator overwhelming consensus prevents Defender from flipping label from 0.80 to UNKNOWN.
2. Dynamic scam_type inference from cues and specialist findings.
3. council_deliberation structure integrity.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipeline.forensic_council import ForensicCouncil

def test_defender_veto_cannot_flip_strong_scam():
    council = ForensicCouncil()
    
    # Simulate completed results: 2 investigators strongly confident in SCAM (0.80, 0.85),
    # 1 Defender voting LOW-RISK.
    completed_results = [
        {
            "role_key": "cyber_financial_analyst",
            "role_id": "ROLE_CYBER_BANK",
            "display_name": "Cyber-Financial Analyst",
            "model_used": "gpt-6.1-sol",
            "weight": 0.35,
            "vote": "SCAM-RISK",
            "scam_prob": 0.85,
            "confidence": 0.90,
            "risk_level": "CRITICAL",
            "key_cues": ["bank_impersonation", "fake_url"],
            "analysis": "Phát hiện tên miền giả mạo Vietcombank và đòi cập nhật sinh trắc học.",
            "latency_ms": 12.0,
            "api_calls_count": 1,
            "cost_usd": 0.0001,
        },
        {
            "role_key": "psycholinguistic_slang_profiler",
            "role_id": "ROLE_PSYCHO_TEENCODE",
            "display_name": "Psycholinguistic Profiler",
            "model_used": "gemini-3.8-flash",
            "weight": 0.35,
            "vote": "SCAM-RISK",
            "scam_prob": 0.80,
            "confidence": 0.85,
            "risk_level": "HIGH",
            "key_cues": ["urgency_pressure"],
            "analysis": "Tạo áp lực khóa tài khoản trong 24h.",
            "latency_ms": 11.0,
            "api_calls_count": 1,
            "cost_usd": 0.0001,
        },
        {
            "role_key": "public_defender_advocate",
            "role_id": "ROLE_DEFENDER",
            "display_name": "Public Defender",
            "model_used": "gpt-6.1-sol",
            "weight": 0.30,
            "vote": "LOW-RISK",
            "scam_prob": 0.20,
            "confidence": 0.85,
            "risk_level": "LOW",
            "key_cues": [],
            "analysis": "Không thấy yêu cầu OTP trực tiếp.",
            "latency_ms": 10.0,
            "api_calls_count": 1,
            "cost_usd": 0.0001,
        },
    ]

    msg = "Vietcombank: Tai khoan cua ban bi khoa, vui long vao https://vietcombank.vn-fake.top de xac thuc trong 24h."
    consensus = council._compute_consensus(completed_results, start_overall=0.0, message=msg)

    # In the old code: 0.25 flat deduction reduced weighted score to ~0.55 (UNKNOWN).
    # In the fixed code: overwhelming investigator consensus prevents defender veto from flipping to UNKNOWN.
    assert consensus["final_label"] == "SCAM-RISK", f"Expected SCAM-RISK, got {consensus['final_label']}"
    assert consensus["consensus_scam_prob"] >= 0.60, f"Score should remain >= 0.60, got {consensus['consensus_scam_prob']}"
    assert "council_deliberation" in consensus, "council_deliberation should be present in consensus"
    delib = consensus["council_deliberation"]
    assert "cyber_banking_specialist" in delib
    assert "psycho_teencode_specialist" in delib
    assert "public_defender" in delib
    assert consensus["scam_type"] != "", "scam_type should not be empty"

def test_defender_veto_applies_when_ambiguous():
    council = ForensicCouncil()
    
    # When evidence is genuinely ambiguous (investigators are not both confident > 0.75):
    completed_results = [
        {
            "role_key": "cyber_financial_analyst",
            "role_id": "ROLE_CYBER_BANK",
            "weight": 0.35,
            "vote": "SCAM-RISK",
            "scam_prob": 0.62,
            "confidence": 0.65,
            "risk_level": "HIGH",
            "analysis": "Có yếu tố đáng ngờ nhưng chưa rõ.",
        },
        {
            "role_key": "psycholinguistic_slang_profiler",
            "role_id": "ROLE_PSYCHO_TEENCODE",
            "weight": 0.35,
            "vote": "UNKNOWN",
            "scam_prob": 0.50,
            "confidence": 0.55,
            "risk_level": "MEDIUM",
            "analysis": "Ngữ cảnh thông thường.",
        },
        {
            "role_key": "public_defender_advocate",
            "role_id": "ROLE_DEFENDER",
            "weight": 0.30,
            "vote": "LOW-RISK",
            "scam_prob": 0.20,
            "confidence": 0.85,
            "risk_level": "LOW",
            "analysis": "Tin nhắn thông báo dịch vụ chuẩn.",
        },
    ]

    msg = "TB: Quy khach da dang ky goi cuoc 4G thanh cong."
    consensus = council._compute_consensus(completed_results, start_overall=0.0, message=msg)

    # Defender should intervene and reduce false positive alarm
    assert consensus["defender_intervened"] is True
    assert consensus["final_label"] in ["LOW-RISK", "UNKNOWN"]
