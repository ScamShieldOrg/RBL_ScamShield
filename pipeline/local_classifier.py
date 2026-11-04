"""
==============================================================================
ScamShield-VN: Tier 1 Local Fast-Path Classifier (ViSoBERT ONNX / CPU)
==============================================================================
Author: ScamShield Core Engineering Team
Description:
    Local on-device text classifier powered by fine-tuned ViSoBERT
    with Temperature Scaling calibration (T*=1.0) and Cost-Sensitive
    Weighted Binary Cross Entropy (WBCE, alpha=5.0).
==============================================================================
"""

import os
import json
import time
import math
import re
import logging
from typing import Dict, List, Optional, Any, Tuple
import numpy as np

try:
    import onnxruntime as ort
except ImportError:
    ort = None

try:
    from tokenizers import Tokenizer
except ImportError:
    Tokenizer = None

logger = logging.getLogger("ScamShield.LocalClassifier")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s", datefmt="%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class LocalViSoBERTClassifier:
    """
    Tier 1 Fast-Path Local CPU Classifier powered by Fine-Tuned ViSoBERT.
    Designed for sub-45ms latency and zero monetary cost on user devices / edge servers.
    """

    def __init__(
        self,
        model_path: Optional[str] = None,
        config_path: Optional[str] = None,
        temperature: float = 1.0,
        cost_alpha: float = 5.0,
        enable_regex_heuristics: bool = True,
    ):
        """
        Initialize the Tier 1 Local Classifier.

        Args:
            model_path: Path to serialized ONNX or PyTorch weights.
            config_path: Path to scamshield_config.json.
            temperature: Post-hoc Temperature Scaling parameter (T*).
            cost_alpha: Weighted BCE penalty ratio for False Negatives (alpha=5.0).
            enable_regex_heuristics: Whether to run instant pre-regex pattern matching.
        """
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.release_dir = os.path.join(base_dir, "visobert_5runs_release")
        
        # Priority: Quantized INT8 ONNX > Full ONNX > release folder
        int8_onnx = os.path.join(self.release_dir, "visobert_tier1_int8.onnx")
        full_onnx = os.path.join(self.release_dir, "visobert_tier1.onnx")
        models_int8 = os.path.join(base_dir, "models", "visobert_tier1_int8.onnx")
        models_full = os.path.join(base_dir, "models", "visobert_tier1.onnx")
        
        if model_path:
            self.model_path = model_path
        elif os.path.exists(int8_onnx):
            self.model_path = int8_onnx
        elif os.path.exists(models_int8):
            self.model_path = models_int8
        elif os.path.exists(full_onnx):
            self.model_path = full_onnx
        elif os.path.exists(models_full):
            self.model_path = models_full
        else:
            self.model_path = self.release_dir

        self.config_path = config_path or os.path.join(base_dir, "models", "scamshield_config.json")
        self.enable_regex_heuristics = enable_regex_heuristics

        # Load config if available
        self.temperature = temperature
        self.cost_alpha = cost_alpha
        self.tokenizer = None
        self.onnx_session = None
        self.pytorch_model = None

        # 1. Initialize Tokenizer
        tok_json_path = os.path.join(self.release_dir, "tokenizer.json")
        if os.path.exists(tok_json_path) and Tokenizer is not None:
            try:
                self.tokenizer = Tokenizer.from_file(tok_json_path)
                self.tokenizer.enable_padding(length=128, pad_id=1, pad_token='<pad>')
                self.tokenizer.enable_truncation(max_length=128)
                logger.info(f"Successfully loaded Tokenizer from {tok_json_path}")
            except Exception as e:
                logger.warning(f"Could not load Tokenizer from {tok_json_path}: {e}")

        # 2. Initialize Real ONNX Runtime Inference Session (Primary)
        self.has_onnx = False
        if ort is not None and os.path.exists(self.model_path) and self.model_path.endswith(".onnx"):
            try:
                session_options = ort.SessionOptions()
                session_options.intra_op_num_threads = min(4, os.cpu_count() or 4)
                session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
                self.onnx_session = ort.InferenceSession(self.model_path, sess_options=session_options, providers=["CPUExecutionProvider"])
                self.has_onnx = True
                logger.info(f"Successfully initialized Tier 1 ONNX INT8 Session: {self.model_path}")
            except Exception as e:
                logger.warning(f"Could not load ONNX session from {self.model_path}: {e}")

        # 3. Secondary Fallback: PyTorch Model
        if not self.has_onnx and os.path.exists(self.release_dir):
            try:
                import torch
                from transformers import AutoModelForSequenceClassification
                self.pytorch_model = AutoModelForSequenceClassification.from_pretrained(self.release_dir)
                self.pytorch_model.eval()
                logger.info("Loaded PyTorch ViSoBERT model as fallback")
            except Exception as e:
                logger.warning(f"Could not load PyTorch ViSoBERT model: {e}")

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.temperature = cfg.get("optimal_temperature_T", self.temperature)
                    self.cost_alpha = cfg.get("pos_weight_alpha", self.cost_alpha)
            except Exception as e:
                logger.warning(f"Could not load {self.config_path}: {e}")

        # Common Vietnamese Scam Patterns for Heuristic Fast-Path Boost (Accented & Unaccented)
        self.scam_indicators = [
            r"(?i)(trúng\s*thưởng|trung\s*thuong|nhận\s*quà|nhan\s*qua|tri\s*ân|tri\s*an)",
            r"(?i)(khóa\s*tài\s*khoản|khoa\s*tai\s*khoan|tạm\s*khóa|tam\s*khoa|xác\s*thực|xac\s*thuc|cập\s*nhật\s*sinh\s*trắc|sinh\s*trac)",
            r"(?i)(bộ\s*công\s*an|bo\s*cong\s*an|viện\s*kiểm\s*sát|vien\s*kiem\s*sat|lệnh\s*bắt|lenh\s*bat|tạm\s*giam|tam\s*giam|rửa\s*tiền|rua\s*tien|ma\s*túy|ma\s*tuy)",
            r"(?i)(việc\s*nhẹ\s*lương\s*cao|viec\s*nhe|tuyển\s*ctv|tuyen\s*ctv|đánh\s*giá\s*sản\s*phẩm|danh\s*gia\s*san\s*pham|hoa\s*hồng|hoa\s*hong|nhiệm\s*vụ|nhan\s*viec)",
            r"(?i)(vay\s*tiền|vay\s*tien|duyệt\s*ngay|duyet\s*ngay|không\s*cần\s*thế\s*chấp|khong\s*can\s*the\s*chap|lãi\s*suất\s*0%|lai\s*suat)",
            r"(?i)(link\s*đăng\s*nhập|link\s*dang\s*nhap|truy\s*cập\s*link|truy\s*cap\s*link|nhập\s*mã\s*otp|nhap\s*ma\s*otp|nhắn\s*zalo|nhan\s*zalo)",
            r"(?i)(https?://[^\s]+\.(xyz|top|vip|cc|tk|ml|ga|cf|gq|info|online|site))",
        ]
        self.compiled_scam_regex = [re.compile(p) for p in self.scam_indicators]

        # Common Vietnamese Ham / Legitimate Indicators (OTP, Telecom, Banking alerts, Masked tokens)
        self.ham_indicators = [
            r"(?i)(mã\s*otp|ma\s*otp|otp\s*của\s*quý\s*khách|otp\s*xac\s*thuc|hieu\s*luc\s*trong\s*\d+\s*phut|hieu\s*luc\s*\[TIME\]|không\s*chia\s*sẻ|khong\s*chia\s*se|khong\s*cung\s*cap)",
            r"(?i)(tài\s*khoản\s*thanh\s*toán|tiền\s*điện|tiền\s*nước|tien\s*dien|tien\s*nuoc|vcb\s*digibank|digibank|shopeepay|vietcombank|mbbank|bidv|vietinbank|techcombank)",
            r"(?i)(gói\s*cước|goi\s*cuoc|gia\s*hạn\s*thành\s*công|gia\s*han\s*thanh\s*cong|data\s*sử\s*dụng|data\s*su\s*dung|quy\s*khach|thue\s*bao)",
            r"(?i)(chuyen\s*khoan\s*nhanh|chuyen\s*tien\s*nhanh\s*247|chi\s*tiet\s*gd|giao\s*dich\s*thanh\s*cong|bien\s*dong\s*so\s*du|so\s*du\s*tk|nguoi\s*nhan:\s*\[NAME\]|so\s*tien:\s*\[MONEY\])",
            r"(?i)(cảm\s*ơn\s*quý\s*khách|cam\s*on\s*quy\s*khach|hỏi\s*thăm|hoi\s*tham|bài\s*giảng|bai\s*giang|lms|thầy|cô)",
            r"(?i)(ăn\s*lẩu|an\s*lau|đi\s*chơi|di\s*choi|cà\s*phê|ca\s*phe|alo\s*nhé|alo\s*nhe)",
        ]
        self.compiled_ham_regex = [re.compile(p) for p in self.ham_indicators]

        logger.info(
            f"Initialized Tier 1 ViSoBERT Local Classifier (ONNX={self.has_onnx}, "
            f"Temperature={self.temperature}, WBCE Alpha={self.cost_alpha})"
        )

    def _apply_temperature_scaling(self, logits: List[float]) -> Tuple[List[float], float]:
        """
        Apply Temperature Scaling: z_calibrated = z / T
        Returns (calibrated_probs, scam_probability)
        """
        calibrated_logits = [z / self.temperature for z in logits]
        max_logit = max(calibrated_logits)
        exp_logits = [math.exp(z - max_logit) for z in calibrated_logits]
        sum_exp = sum(exp_logits)
        probs = [e / sum_exp for e in exp_logits]
        scam_prob = probs[1]  # Class 1 = Scam
        return probs, scam_prob

    def _extract_semantic_features(self, text: str) -> Tuple[float, float, List[str]]:
        """
        Fast semantic & lexical feature extraction for simulated / fallback CPU inference.
        Returns: (scam_score, ham_score, matched_cues)
        """
        scam_score = 0.0
        ham_score = 0.0
        matched_cues = []

        # Check scam cues
        for idx, pattern in enumerate(self.compiled_scam_regex):
            match = pattern.search(text)
            if match:
                scam_score += 1.85
                matched_cues.append(f"ScamPattern[{match.group(0)[:30]}]")

        # Check ham cues
        for idx, pattern in enumerate(self.compiled_ham_regex):
            match = pattern.search(text)
            if match:
                ham_score += 1.60
                matched_cues.append(f"HamPattern[{match.group(0)[:30]}]")

        # URL heuristics
        urls = re.findall(r"https?://[^\s]+", text)
        if urls:
            for url in urls:
                if any(bad in url for bad in [".xyz", ".top", ".vip", ".cc", "bit.ly", "tinyurl", "linktr.ee"]):
                    scam_score += 2.2
                    matched_cues.append(f"SuspiciousDomain[{url}]")
                elif any(brand in url for brand in ["vcb", "bidv", "vietinbank", "mbbank", "techcombank"]):
                    # Possible phishing if combined with non-official domain
                    if not any(domain in url for domain in ["vietcombank.com.vn", "bidv.com.vn", "vietinbank.vn", "mbbank.com.vn", "techcombank.com"]):
                        scam_score += 3.5
                        matched_cues.append(f"BrandSpoofingURL[{url}]")

        # Urgency & Financial triggers (Formal & Conversational / Social Engineering)
        urgency_words = [
            "ngay", "khẩn cấp", "24h", "hết hạn", "phạt", "tòa án", "phong tỏa", "gấp",
            "mượn", "cho mượn", "chuyển vô", "mã qr", "ma qr", "giật ví",
            "mất điện thoại", "mat dien thoai", "cứu với", "anh họ", "vay tiền", "tuyển ctv"
        ]
        for uw in urgency_words:
            if uw in text.lower():
                scam_score += 0.65
                matched_cues.append(f"SocialEmergencyCue[{uw}]")

        # Normal conversational tone without financial urgency
        if len(text.split()) < 6 and not urls and scam_score == 0:
            ham_score += 1.2

        return scam_score, ham_score, matched_cues

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Classify a message using Tier 1 ViSoBERT CPU engine with Temperature Scaling.

        Args:
            text: Raw input SMS / chat message.

        Returns:
            dict containing prediction results, probabilities, confidence, and latency.
        """
        start_time = time.perf_counter()

        # Step 1: Feature / Logit computation
        scam_score, ham_score, matched_cues = self._extract_semantic_features(text)

        # 1. Primary: Real ViSoBERT ONNX INT8 CPU Inference
        if self.onnx_session is not None and self.tokenizer is not None:
            try:
                enc = self.tokenizer.encode(text)
                input_ids = np.array([enc.ids], dtype=np.int64)
                attention_mask = np.array([enc.attention_mask], dtype=np.int64)
                outputs = self.onnx_session.run(None, {"input_ids": input_ids, "attention_mask": attention_mask})
                raw_scam_logit = float(outputs[0][0][0])
                raw_ham_logit = -raw_scam_logit

                # Post-hoc Temperature Scaling calibration (z_cal = z / T*)
                calibrated_logit = raw_scam_logit / self.temperature
                scam_prob = 1.0 / (1.0 + math.exp(-calibrated_logit))
                scam_prob = max(0.0001, min(0.9999, scam_prob))
                confidence = max(scam_prob, 1.0 - scam_prob)
                predicted_class = 1 if scam_prob >= 0.5 else 0
                predicted_label = "SCAM" if predicted_class == 1 else "HAM"
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0

                return {
                    "tier": "Tier 1 (Local ViSoBERT ONNX INT8/CPU)",
                    "label": predicted_label,
                    "class_id": predicted_class,
                    "raw_logits": [round(raw_ham_logit, 4), round(raw_scam_logit, 4)],
                    "calibrated_scam_prob": round(scam_prob, 4),
                    "confidence": round(confidence, 4),
                    "latency_ms": round(elapsed_ms, 2),
                    "cost_usd": 0.0,
                    "matched_cues": matched_cues,
                    "temperature": self.temperature,
                    "model_path": self.model_path,
                }
            except Exception as e:
                logger.warning(f"ONNX inference error: {e}. Falling back to PyTorch/Heuristics.")

        # 2. Secondary: PyTorch ViSoBERT 5-runs model inference
        if self.pytorch_model is not None and self.tokenizer is not None:
            import torch
            try:
                enc = self.tokenizer.encode(text)
                input_ids = torch.tensor([enc.ids], dtype=torch.long)
                attention_mask = torch.tensor([enc.attention_mask], dtype=torch.long)
                with torch.no_grad():
                    out = self.pytorch_model(input_ids=input_ids, attention_mask=attention_mask)
                    raw_scam_logit = out.logits.item()

                calibrated_logit = raw_scam_logit / self.temperature
                scam_prob = 1.0 / (1.0 + math.exp(-calibrated_logit))
                scam_prob = max(0.0001, min(0.9999, scam_prob))
                confidence = max(scam_prob, 1.0 - scam_prob)
                predicted_class = 1 if scam_prob >= 0.5 else 0
                predicted_label = "SCAM" if predicted_class == 1 else "HAM"
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0

                return {
                    "tier": "Tier 1 (Local ViSoBERT PyTorch/CPU)",
                    "label": predicted_label,
                    "class_id": predicted_class,
                    "raw_logits": [round(-raw_scam_logit, 4), round(raw_scam_logit, 4)],
                    "calibrated_scam_prob": round(scam_prob, 4),
                    "confidence": round(confidence, 4),
                    "latency_ms": round(elapsed_ms, 2),
                    "cost_usd": 0.0,
                    "matched_cues": matched_cues,
                    "temperature": self.temperature,
                    "model_path": self.release_dir,
                }
            except Exception as e:
                logger.warning(f"PyTorch prediction error: {e}. Falling back to heuristics.")

        # 3. Emergency Heuristic Fallback (Only when no model weights can be loaded)
        bias_alpha = math.log(self.cost_alpha) * 0.4
        raw_ham_logit = (ham_score - scam_score) + 1.2
        raw_scam_logit = (scam_score - ham_score) + bias_alpha
        raw_logits = [raw_ham_logit, raw_scam_logit]

        calibrated_probs, scam_prob = self._apply_temperature_scaling(raw_logits)
        confidence = max(calibrated_probs)
        predicted_class = 1 if scam_prob >= 0.5 else 0
        predicted_label = "SCAM" if predicted_class == 1 else "HAM"
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "tier": "Tier 1 (Emergency Heuristic Fallback)",
            "label": predicted_label,
            "class_id": predicted_class,
            "raw_logits": [round(z, 4) for z in raw_logits],
            "calibrated_scam_prob": round(scam_prob, 4),
            "confidence": round(confidence, 4),
            "latency_ms": round(elapsed_ms, 2),
            "cost_usd": 0.0,
            "matched_cues": matched_cues,
            "temperature": self.temperature,
            "model_path": "No Model Weights Loaded",
        }


# Backwards compatibility alias
LocalPhoBERTClassifier = LocalViSoBERTClassifier
