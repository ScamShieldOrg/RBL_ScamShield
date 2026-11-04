# 🔧 KẾ HOẠCH CÀI ĐẶT CODE - TIER 2 AUDIT FIXES

**Ngày:** 2026-10-20  
**Trạng thái:** Ready for Development  
**Sprint:** 1-4 (Oct 20 - Nov 8)  

---

## 📝 FILE CHANGES MATRIX

| File | Type | Status | Priority |
|------|------|--------|----------|
| `pipeline/forensic_council.py` | Edit | 🔴 CRITICAL | 1 |
| `pipeline/two_tier_router.py` | Edit | 🟠 HIGH | 2 |
| `config/council_registry.yaml` | Edit | 🟠 HIGH | 3 |
| `pipeline/pii_masking.py` | Create | 🟠 HIGH | 4 |
| `pipeline/tier2_gating_policy.py` | Create | 🟠 HIGH | 5 |
| `experiments/tier2_council/runner_p_single.py` | Create | 🟡 MEDIUM | 6 |
| `experiments/tier2_council/analyze_error_correlation.py` | Create | 🟡 MEDIUM | 7 |

---

## 🔴 TASK 1: CRITICAL FIX - forensic_council.py

### Change 1.1: Thay SUSPICIOUS_REVIEW → UNKNOWN

**Location:** Lines 461-474  
**Current Code:**
```python
# Determine Final Label
unanimous_thresh = self.consensus_rules.get("unanimous_scam_threshold", 0.85)
suspected_thresh = self.consensus_rules.get("suspected_scam_threshold", 0.60)
ham_thresh = self.consensus_rules.get("ham_threshold", 0.40)

if weighted_scam_prob >= suspected_thresh:
    final_label = "SCAM"
    risk_level = "CRITICAL" if weighted_scam_prob >= unanimous_thresh else "HIGH"
elif weighted_scam_prob < ham_thresh:
    final_label = "HAM"
    risk_level = "LOW"
else:
    final_label = "SUSPICIOUS_REVIEW"  # ❌ WRONG - Should be UNKNOWN
    risk_level = "MEDIUM"
```

**Fixed Code:**
```python
# Determine Final Label (3-Label Schema: SCAM-RISK, LOW-RISK, UNKNOWN)
unanimous_thresh = self.consensus_rules.get("unanimous_scam_threshold", 0.85)
suspected_thresh = self.consensus_rules.get("suspected_scam_threshold", 0.60)
ham_thresh = self.consensus_rules.get("ham_threshold", 0.40)

if weighted_scam_prob >= suspected_thresh:
    final_label = "SCAM-RISK"  # Scam probability high
    risk_level = "CRITICAL" if weighted_scam_prob >= unanimous_thresh else "HIGH"
elif weighted_scam_prob < ham_thresh:
    final_label = "LOW-RISK"  # Legitimate message
    risk_level = "LOW"
else:
    final_label = "UNKNOWN"  # ✓ Ambiguous - requires audit
    risk_level = "MEDIUM"
    
    # Log UNKNOWN trigger reasons
    unknown_reasons = []
    if self._check_vote_contradiction(completed_results):
        unknown_reasons.append("vote_contradiction")
    if weighted_scam_prob < 0.55:
        unknown_reasons.append("low_consensus_confidence")
    if defender_intervened:
        unknown_reasons.append("defender_veto_applied")
    
    logger.info(f"UNKNOWN label triggered: {unknown_reasons}")
```

### Change 1.2: Thêm Vote Schema cho UNKNOWN

**Location:** Lines 242-255 (User Prompt)  
**Current Code:**
```python
user_prompt = f"""Phân tích tin nhắn tiếng Việt sau đây dưới góc nhìn chuyên môn của bạn:

\"\"\"{message}\"\"\"

Bắt buộc trả về định dạng JSON thuần túy theo schema sau:
{{
    "role_id": "{role_id}",
    "vote": "SCAM" hoặc "HAM",  # ❌ Only 2 options
    "scam_prob": 0.0 - 1.0,
    ...
}}"""
```

**Fixed Code:**
```python
user_prompt = f"""Phân tích tin nhắn tiếng Việt sau đây dưới góc nhìn chuyên môn của bạn:

\"\"\"{message}\"\"\"

Bắt buộc trả về định dạng JSON thuần túy theo schema sau:
{{
    "role_id": "{role_id}",
    "vote": "SCAM" hoặc "HAM" hoặc "UNKNOWN",  # ✓ 3 options
    "scam_prob": 0.0 - 1.0,
    "confidence": 0.0 - 1.0,
    "risk_level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
    "key_cues": ["danh sách các từ khóa hoặc dấu hiệu cụ thể"],
    "analysis": "1-2 câu lý giải chuyên môn ngắn gọn"
}}"""
```

### Change 1.3: Thêm Helper Method

**Location:** After line 405 (before `async def evaluate_council`)  
**New Method:**
```python
def _check_vote_contradiction(self, completed_results: List[Dict[str, Any]]) -> bool:
    """
    Kiểm tra mâu thuẫn phiếu bầu (2-3 split).
    True nếu các agent không đồng thuận rõ ràng.
    """
    scam_votes = sum(1 for r in completed_results if r["vote"] == "SCAM")
    ham_votes = sum(1 for r in completed_results if r["vote"] == "HAM")
    unknown_votes = sum(1 for r in completed_results if r["vote"] == "UNKNOWN")
    
    # Nếu không có majority clear (>= 2 votes cùng loại trong 3 agents hoặc mâu thuẫn)
    return max(scam_votes, ham_votes, unknown_votes) < 3

def _compute_error_correlation(self, completed_results: List[Dict[str, Any]]) -> float:
    """
    Tính độ tương quan sai lầm của các agent.
    Nếu > 0.4, cảnh báo về Common Mode Failure.
    (Placeholder - implement in analyze script)
    """
    return 0.0
```

### Change 1.4: Update Rationale Output

**Location:** Lines 478-485  
**Current Code:**
```python
unified_rationale = (
    f"**Kết luận Hội đồng:** {'LỪA ĐẢO NGUY HIỂM' if final_label == 'SCAM' else 'TIN NHẮN HỢP PHÁP'}.\n"
    f"Tỷ lệ đồng thuận điều chỉnh: {weighted_scam_prob*100:.1f}%. "
    f"({'Kích hoạt Early-Exit Fast-Path' if early_exit_triggered else 'Biểu quyết đầy đủ 5 thành viên'}).\n"
    + "\n".join(analyses)
)
```

**Fixed Code:**
```python
conclusion_text = {
    "SCAM-RISK": "🚨 LỪA ĐẢO NGUY HIỂM - YÊU CẦU CẢNH BÁO",
    "LOW-RISK": "✓ TIN NHẮN HỢP PHÁP - KHÔNG CÓ RỦI RO",
    "UNKNOWN": "⚠️ KHÔNG XÁC ĐỊNH - CẦN KIỂM TOÁN THÊM"
}[final_label]

unified_rationale = (
    f"**Kết luận Hội đồng:** {conclusion_text}\n"
    f"Tỷ lệ đồng thuận điều chỉnh: {weighted_scam_prob*100:.1f}%. "
    f"({'Kích hoạt Early-Exit Fast-Path' if early_exit_triggered else 'Biểu quyết đầy đủ {len(completed_results)} thành viên'}).\n"
    + "\n".join(analyses)
)
```

---

## 🟠 TASK 2: HIGH PRIORITY - two_tier_router.py

### Change 2.1: Thêm PII Masking trước Escalate

**Location:** Before line 172 (before `council_res = self.council.evaluate_sync()`)  
**New Code:**
```python
# Import PII Masker
from .pii_masking import PIIMasker

# ...in classify() method...

# Step 2B: Escalate to Tier 2 with PII Masking
if self.use_council and self.council:
    routing_reason = (
        f"Tầng 1 phân vân ({t1_confidence*100:.1f}% < {self.tau*100:.0f}%), rơi vào vùng rủi ro bỏ sót lừa đảo (FNR). "
        f"Kích hoạt Tầng 2 (Consolidated 3-Agent Forensic Council) với cơ chế Early-Exit và phản biện chống Alarm Fatigue."
    )
    logger.info(f"Escalating message to Tier 2 Forensic Council. Reason: {fallback_trigger}")
    
    # ✓ NEW: Apply PII Masking per NĐ 13/2023 Điều 25
    masker = PIIMasker()
    masked_message, pii_map = masker.mask_message(message)
    logger.info(f"PII Masking applied. Tokens masked: {len(pii_map)}")
    
    try:
        # Pass masked message to Council
        council_res = self.council.evaluate_sync(masked_message)
        
        # Log audit trail
        audit_log = {
            "timestamp": time.time(),
            "original_message_hash": hashlib.sha256(message.encode()).hexdigest(),
            "masked_message_hash": hashlib.sha256(masked_message.encode()).hexdigest(),
            "pii_tokens_masked": len(pii_map),
            "council_decision": council_res["final_label"]
        }
        logger.info(f"Audit Trail: {json.dumps(audit_log)}")
        
        # ... rest of code ...
```

### Change 2.2: Thêm Tier 2 Gating Policy Check

**Location:** Before line 162 (`fallback_trigger = ...`)  
**New Code:**
```python
# NEW: Check if message should escalate to Tier 2
from .tier2_gating_policy import Tier2GatingPolicy

gating_policy = Tier2GatingPolicy()
should_escalate = gating_policy.should_escalate_to_tier2(
    message=message,
    tier1_result=t1_result,
    user_context={"user_requested_audit": force_tier2}
)

if not should_escalate and not force_tier2:
    # Direct return from Tier 1 - no escalation needed
    total_elapsed_ms = (time.perf_counter() - start_overall) * 1000
    routing_reason = (
        f"Tin nhắn không đáp ứng tiêu chí escalate Tier 2. "
        f"Tier 1 quyết định trực tiếp: {t1_result['label']}"
    )
    return {
        "message": message,
        "final_label": t1_result["label"],
        # ... rest of fields ...
        "routing_reason": routing_reason,
        "gating_policy_applied": True,
    }
```

### Change 2.3: Update Label Mapping (SCAM-RISK, LOW-RISK, UNKNOWN)

**Location:** Lines 176-178  
**Current Code:**
```python
council_res = self.council.evaluate_sync(message)
# ...
"is_scam": (council_res["final_label"] == "SCAM"),
```

**Fixed Code:**
```python
council_res = self.council.evaluate_sync(masked_message)
# ...
"is_scam": (council_res["final_label"] == "SCAM-RISK"),
"is_unknown": (council_res["final_label"] == "UNKNOWN"),
```

---

## 🟠 TASK 3: HIGH PRIORITY - config/council_registry.yaml

### Change 3.1: Update Consensus Rules

**Location:** Lines 116-122  
**Current Code:**
```yaml
consensus_rules:
  unanimous_scam_threshold: 0.85
  suspected_scam_threshold: 0.60
  borderline_threshold: 0.40
  ham_threshold: 0.40
  public_defender_veto_boost: 0.25
```

**Fixed Code:**
```yaml
consensus_rules:
  # 3-Label Schema
  scam_risk_threshold: 0.60      # >= 0.60 → SCAM-RISK
  low_risk_threshold: 0.40       # < 0.40 → LOW-RISK
  unknown_range: [0.40, 0.60]    # 0.40-0.60 → UNKNOWN
  
  # Confidence thresholds
  unanimous_scam_threshold: 0.85  # For CRITICAL risk level
  suspected_scam_threshold: 0.60  # For HIGH risk level
  public_defender_veto_boost: 0.25  # Anti-false-alarm
  
  # UNKNOWN triggers
  unknown_triggers:
    vote_contradiction_enabled: true
    low_confidence_threshold: 0.55
    defender_veto_enabled: true
```

### Change 3.2: Add Data Masking Policy

**Location:** After `circuit_breaker:` section  
**New Section:**
```yaml
data_masking_policy:
  enabled: true
  compliance_standard: "NĐ 13/2023 Điều 25"
  
  # PII patterns to mask
  patterns:
    cmnd_cccd:
      regex: '\b\d{9}(\d{3})?\b'
      replacement: '<ID_CARD:XXXXXXXX>'
    phone_number:
      regex: '\b(?:0|\+84)[0-9]{9}\b'
      replacement: '<PHONE:XXXXXXXX>'
    otp_code:
      regex: '\b\d{6}\b(?=.*otp|.*mã)'
      replacement: '<OTP_CODE:XXXXXX>'
    bank_account:
      regex: '\b\d{8,17}\b'
      replacement: '<ACCOUNT:XXXXXXXX>'
  
  # Audit logging
  audit_log:
    enabled: true
    retention_days: 30  # Delete after 30 days per NĐ 13/2023
    log_file: 'logs/pii_audit.jsonl'
```

### Change 3.3: Add Tier 2 Gating Policy

**Location:** After `data_masking_policy:` section  
**New Section:**
```yaml
tier2_gating_policy:
  enabled: true
  
  # 4 conditions for escalation
  conditions:
    low_confidence:
      enabled: true
      threshold: 0.85  # If Tier 1 confidence < 0.85
    unknown_url:
      enabled: true
      check_blacklist: true
      check_whitelist: true
    user_requested_audit:
      enabled: true
    rare_lexicon:
      enabled: true
      min_rare_words: 3
  
  # Decision logic: escalate if ANY condition true
  escalation_logic: "OR"
```

---

## 🟠 TASK 4: HIGH PRIORITY - CREATE pipeline/pii_masking.py

**New File:** `pipeline/pii_masking.py`  
**Size:** ~200 lines

```python
"""
==============================================================================
ScamShield-VN: PII Masking Engine (NĐ 13/2023 Compliance)
==============================================================================
Purpose: Automatically redact/mask Personally Identifiable Information (PII)
before escalating messages to Cloud LLM services in Tier 2.

Complies with: Nghị định 13/2023/NĐ-CP (Chỉnh lý pháp lệnh bảo vệ dữ liệu cá nhân)
Reference: Điều 25 - Quyền của chủ thể dữ liệu trong xử lý dữ liệu
==============================================================================
"""

import re
import json
import hashlib
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

logger = logging.getLogger("ScamShield.PIIMasking")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class PIIMasker:
    """
    Redacts/masks PII (Personal Identifiable Information) from messages
    before cloud escalation. Supports: CMND, Phone, OTP, Account numbers, Names.
    """
    
    def __init__(self, salt: str = "scamshield-vn-2026"):
        """
        Args:
            salt: Security salt for hashing (for PII_map reversal only in audit)
        """
        self.salt = salt
        self.pii_patterns = {
            "cmnd": {
                "pattern": r'\b\d{9}(?:\d{3})?\b',
                "label": "ID_CARD",
                "example": "123456789"
            },
            "phone": {
                "pattern": r'\b(?:0|\+84)[0-9]{9}\b',
                "label": "PHONE",
                "example": "0987654321"
            },
            "otp": {
                "pattern": r'\b\d{6}\b',
                "label": "OTP_CODE",
                "example": "123456"
            },
            "account": {
                "pattern": r'\b\d{8,17}\b',
                "label": "ACCOUNT",
                "example": "1234567890123456"
            },
            "email": {
                "pattern": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                "label": "EMAIL",
                "example": "user@example.com"
            }
        }
    
    def mask_message(self, message: str, aggressive: bool = True) -> Tuple[str, Dict]:
        """
        Masks all PII in message. Returns (masked_message, pii_map).
        
        Args:
            message: Original message text
            aggressive: If True, mask even partial patterns (e.g., any 8-digit number)
        
        Returns:
            (masked_message, pii_map) where pii_map contains:
              {
                "<TYPE:HASH>": {
                  "type": "CMND" | "PHONE" | "OTP" | "ACCOUNT" | "EMAIL",
                  "original": "***hidden***",  # Never store plaintext
                  "hash": "abc123...",
                  "timestamp": "2026-10-20T10:15:00Z"
                }
              }
        """
        masked_text = message
        pii_map = {}
        
        # Apply patterns in order of specificity
        pattern_order = ["cmnd", "phone", "otp", "account", "email"]
        
        for pattern_key in pattern_order:
            spec = self.pii_patterns[pattern_key]
            pattern = spec["pattern"]
            label = spec["label"]
            
            matches = re.finditer(pattern, masked_text)
            for match in matches:
                original_value = match.group(0)
                
                # Skip if already masked
                if original_value.startswith("<"):
                    continue
                
                # Create hash token
                hash_obj = hashlib.sha256(f"{original_value}:{self.salt}".encode())
                hash_hex = hash_obj.hexdigest()[:8]
                token = f"<{label}:{hash_hex}>"
                
                # Replace in text
                masked_text = masked_text.replace(original_value, token, 1)
                
                # Record in map (WITHOUT storing plaintext)
                pii_map[token] = {
                    "type": label,
                    "hash": hash_hex,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "masked_at": "tier2_escalation"
                }
                
                logger.info(f"Masked {label}: {token}")
        
        # Audit log
        if pii_map:
            logger.warning(
                f"PII Masking: {len(pii_map)} tokens masked. "
                f"Original length: {len(message)}, Masked length: {len(masked_text)}"
            )
        
        return masked_text, pii_map
    
    def unmask_for_audit(self, masked_text: str, pii_map: Dict) -> Optional[str]:
        """
        Restore original message from masked text + map.
        ONLY for authorized audit operations. Requires explicit log entry.
        
        Returns:
            Original message, or None if map is incomplete/invalid
        """
        unmasked = masked_text
        
        for token, pii_info in pii_map.items():
            # For audit purposes: restore to placeholder (not actual value)
            # Actual value stored separately in encrypted audit database
            unmasked = unmasked.replace(token, f"[REDACTED_{pii_info['type']}]")
        
        logger.warning(f"Audit Unmask operation performed at {datetime.utcnow().isoformat()}Z")
        return unmasked
    
    def mask_batch(self, messages: List[str]) -> List[Tuple[str, Dict]]:
        """
        Mask multiple messages in batch.
        
        Returns:
            List of (masked_message, pii_map) tuples
        """
        return [self.mask_message(msg) for msg in messages]
    
    @staticmethod
    def is_pii_present(text: str) -> bool:
        """Quick check if message likely contains PII."""
        pii_keywords = [
            r'\b\d{9,}\b',  # Long number sequences
            r'\b\d{3}-\d{3}-\d{4}\b',  # Phone format
            r'\b\d{6}\b',  # OTP pattern
            r'@',  # Email indicator
        ]
        return any(re.search(p, text) for p in pii_keywords)


# Example usage
if __name__ == "__main__":
    masker = PIIMasker()
    
    test_msg = "Vietcombank thông báo: Tài khoản 0987654321 có giao dịch. OTP: 123456. CMND: 012345678. Liên hệ: 0123456789"
    
    masked, pii_map = masker.mask_message(test_msg)
    print("Original:", test_msg)
    print("Masked:", masked)
    print("PII Map:", json.dumps(pii_map, indent=2))
    
    # Verify no PII in masked message
    assert not re.search(r'\b0987654321\b', masked), "Phone number not masked!"
    assert not re.search(r'\b123456\b', masked), "OTP not masked!"
    print("✓ Masking verification passed")
```

---

## 🟠 TASK 5: HIGH PRIORITY - CREATE pipeline/tier2_gating_policy.py

**New File:** `pipeline/tier2_gating_policy.py`  
**Size:** ~150 lines

```python
"""
Tier 2 Gating Policy: Determines when Tier 1 output should escalate to Cloud LLM.

Purpose: Prevent unnecessary cloud escalation (save costs/latency/privacy risk)
while catching ambiguous cases that need deeper analysis.

4 Escalation Conditions (OR logic):
1. Tier 1 Low Confidence: confidence < 0.85
2. Unknown URL: Message contains URL not in whitelist/blacklist
3. User Requested Audit: Explicit user trigger (force_tier2=True)
4. Rare Lexicon: Message has 3+ words not in standard vocabulary
"""

import re
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("ScamShield.Tier2GatingPolicy")


class Tier2GatingPolicy:
    """Controls escalation from Tier 1 to Tier 2 Cloud Council."""
    
    def __init__(self):
        # Known benign domains & URLs
        self.whitelist_domains = [
            "vietcombank.com.vn",
            "mbbank.com.vn",
            "techcombank.com.vn",
            "agribank.com.vn",
            "bidv.com.vn",
            "sacombank.com.vn",
            "ebank.viettelbank.com.vn",
        ]
        
        # Known malicious domains (sample)
        self.blacklist_domains = [
            "vietcombank-login.com",
            "mbbank-verify.top",
            "tpbank-security.xyz",
        ]
        
        # Standard Vietnamese vocabulary (sample - should expand)
        self.standard_vocab = set([
            "vietcombank", "mbbank", "techcombank",
            "otp", "mã", "xác thực", "khóa",
            "tin nhắn", "giao dịch", "tài khoản",
        ])
    
    def should_escalate_to_tier2(
        self,
        message: str,
        tier1_result: Dict[str, Any],
        user_context: Dict[str, Any]
    ) -> bool:
        """
        Returns True if message should escalate to Tier 2.
        
        4 Conditions (OR logic):
        1. Tier 1 confidence too low
        2. Unknown URL detected
        3. User explicitly requested audit
        4. Rare/suspicious lexicon detected
        """
        
        conditions_met = []
        
        # Condition 1: Low Confidence
        if self._check_low_confidence(tier1_result):
            conditions_met.append("LOW_CONFIDENCE")
        
        # Condition 2: Unknown URL
        if self._check_unknown_url(message):
            conditions_met.append("UNKNOWN_URL")
        
        # Condition 3: User Requested
        if user_context.get("user_requested_audit", False):
            conditions_met.append("USER_REQUESTED")
        
        # Condition 4: Rare Lexicon
        if self._check_rare_lexicon(message):
            conditions_met.append("RARE_LEXICON")
        
        should_escalate = len(conditions_met) > 0
        
        if should_escalate:
            logger.info(f"Escalation triggered: {conditions_met}")
        
        return should_escalate
    
    def _check_low_confidence(self, tier1_result: Dict[str, Any]) -> bool:
        """Condition 1: Tier 1 confidence < 0.85"""
        confidence = tier1_result.get("confidence", 1.0)
        return confidence < 0.85
    
    def _check_unknown_url(self, message: str) -> bool:
        """Condition 2: Message contains URL not in white/blacklist"""
        urls = re.findall(r'https?://[^\s]+', message)
        
        for url in urls:
            domain = self._extract_domain(url)
            
            # Check against whitelist
            if any(whitelisted in domain for whitelisted in self.whitelist_domains):
                continue  # Benign domain
            
            # Check against blacklist
            if any(blacklisted in domain for blacklisted in self.blacklist_domains):
                return True  # Malicious - escalate
            
            # Unknown domain - escalate
            return True
        
        return False
    
    def _check_rare_lexicon(self, message: str) -> bool:
        """Condition 4: Count words not in standard vocabulary"""
        words = re.findall(r'\w+', message.lower())
        rare_count = sum(1 for w in words if w not in self.standard_vocab)
        
        # If >= 3 rare words, escalate
        return rare_count >= 3
    
    @staticmethod
    def _extract_domain(url: str) -> str:
        """Extract domain from URL."""
        match = re.search(r'https?://([^\s/]+)', url)
        return match.group(1) if match else ""


if __name__ == "__main__":
    policy = Tier2GatingPolicy()
    
    test_cases = [
        {
            "message": "Vietcombank: https://vietcombank.com.vn/login",
            "tier1_result": {"confidence": 0.95},
            "user_context": {},
            "expected": False  # Benign URL + high confidence
        },
        {
            "message": "Cập nhật: https://vietcombank-login.xyz",
            "tier1_result": {"confidence": 0.85},
            "user_context": {},
            "expected": True  # Unknown URL
        },
    ]
    
    for i, test in enumerate(test_cases):
        result = policy.should_escalate_to_tier2(
            test["message"],
            test["tier1_result"],
            test["user_context"]
        )
        status = "✓" if result == test["expected"] else "✗"
        print(f"{status} Test {i+1}: {result} (expected {test['expected']})")
```

---

## 🟡 TASK 6: MEDIUM PRIORITY - CREATE experiments/tier2_council/runner_p_single.py

**New File:** `experiments/tier2_council/runner_p_single.py`  
**Size:** ~250 lines  
**Purpose:** Baseline P-Single experiment runner

```python
"""
P-Single Baseline Runner: Execute single LLM with Structured Forensic Prompt.
For comparison against 5-Agent Council.

Reference: Wang et al. (ACL 2024) - Single LLM with optimized prompt ≈ Multi-Agent Consensus
"""

import asyncio
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any

from tqdm import tqdm
import requests


STRUCTURED_FORENSIC_PROMPT = """Bạn là Chuyên gia An Ninh Mạng & Gian Lận Tài Chính Việt Nam.
Phân tích tin nhắn tiếng Việt sau theo phương pháp Structured Forensic:

[MESSAGE_HERE]

PHÂN TÍCH 5 TRỤC:
1. [KỸ THUẬT] URL, domain, APK độc hại?
2. [TÂM LÝ] Áp lực thời gian, lòng tham?
3. [NGÔN NGỮ] Teencode, ký tự lạ?
4. [TÀI CHÍNH] OTP, thông tin cá nhân?
5. [PHÁP LÝ] Vi phạm QĐ NHNN?

JSON:
{"risk_score": 0.0-1.0, "label": "SCAM"|"LOW-RISK"|"UNKNOWN", "axes": {...}}
"""


class PSingleRunner:
    def __init__(self, model: str, api_base: str = "https://vibi.top/v1"):
        self.model = model
        self.api_base = api_base
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    
    async def evaluate_message(self, message: str) -> Dict[str, Any]:
        """Run P-Single on single message."""
        start = time.perf_counter()
        
        user_prompt = STRUCTURED_FORENSIC_PROMPT.replace("[MESSAGE_HERE]", message)
        
        # Call API
        response = await self._call_api(user_prompt)
        
        elapsed_ms = (time.perf_counter() - start) * 1000
        
        return {
            "message": message,
            "model": self.model,
            "response": response,
            "latency_ms": elapsed_ms,
            "timestamp": time.time()
        }
    
    async def _call_api(self, prompt: str) -> Dict:
        """Call OpenAI-compatible API."""
        # Implementation similar to forensic_council._call_vibi_api()
        pass


# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-6.1-sol")
    parser.add_argument("--suite", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    
    runner = PSingleRunner(args.model)
    
    # Load test suite
    with open(args.suite) as f:
        test_samples = [json.loads(line) for line in f]
    
    # Run experiments
    results = []
    for sample in tqdm(test_samples):
        result = asyncio.run(runner.evaluate_message(sample["message"]))
        results.append(result)
    
    # Save
    with open(args.output, 'w') as f:
        for r in results:
            f.write(json.dumps(r) + '\n')
    
    print(f"✓ Saved {len(results)} results to {args.output}")
```

---

## 🟡 TASK 7: MEDIUM PRIORITY - CREATE experiments/tier2_council/analyze_error_correlation.py

**New File:** `experiments/tier2_council/analyze_error_correlation.py`  
**Size:** ~200 lines  
**Purpose:** Error correlation analysis to check agent independence

```python
"""
Error Correlation Analysis: Measure co-occurrence of agent failures.
If correlation too high, agents are not truly independent.
"""

import json
import argparse
import numpy as np
from pathlib import Path


def compute_error_correlation_matrix(council_runs: List[Dict]) -> Dict:
    """
    Compute pairwise error correlation between agents.
    """
    agents = ["ROLE_CYBER_URL", "ROLE_SOC_ENG", "ROLE_BANK_VERIFY", 
              "ROLE_VN_TEENCODE", "ROLE_DEFENDER"]
    
    correlation_matrix = {}
    
    for i, agent_a in enumerate(agents):
        for agent_b in agents[i+1:]:
            co_error_count = 0
            both_correct = 0
            
            for run in council_runs:
                vote_a = run["specialist_votes"][agent_a]["vote"]
                vote_b = run["specialist_votes"][agent_b]["vote"]
                ground_truth = run["ground_truth"]
                
                if vote_a == ground_truth and vote_b == ground_truth:
                    both_correct += 1
                elif vote_a != ground_truth and vote_b != ground_truth:
                    if vote_a == vote_b:  # Same wrong answer
                        co_error_count += 1
            
            correlation = co_error_count / max(len(council_runs) - both_correct, 1)
            correlation_matrix[f"{agent_a}-{agent_b}"] = correlation
    
    return correlation_matrix


# ... rest of implementation ...
```

---

## ✅ IMPLEMENTATION CHECKLIST

### Phase 1: Critical Fix (Sprint 1, Day 1-2)
- [ ] Edit `forensic_council.py` (Changes 1.1 - 1.4)
- [ ] Test: `python pipeline/forensic_council.py` outputs SCAM/LOW-RISK/UNKNOWN
- [ ] Verify schema change: vote accepts 3 options

### Phase 2: Infrastructure (Sprint 1, Day 3-4)
- [ ] Create `pii_masking.py` (Task 4)
- [ ] Create `tier2_gating_policy.py` (Task 5)
- [ ] Unit test both modules

### Phase 3: Integration (Sprint 1, Day 5)
- [ ] Edit `two_tier_router.py` (Changes 2.1 - 2.3)
- [ ] Edit `council_registry.yaml` (Changes 3.1 - 3.3)
- [ ] End-to-end test: message → Tier 1 → Tier 2 (with PII masking)

### Phase 4: Experiments (Sprint 1, Day 6-7)
- [ ] Create `runner_p_single.py` (Task 6)
- [ ] Create `analyze_error_correlation.py` (Task 7)
- [ ] Run ablation: 3-VAI vs 5-VAI vs P-Single

---

**Document:** `CODE_IMPLEMENTATION_PLAN.md`  
**Status:** Ready for Development  
**Priority:** CRITICAL → HIGH → MEDIUM
