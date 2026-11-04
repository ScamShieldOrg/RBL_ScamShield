"""
==============================================================================
ScamShield-VN: Dynamic Model Registry for Google Generative AI (Tier 2 Cloud)
==============================================================================
Author: ScamShield Core Engineering Team
Description:
    Dynamic Google Gemini REST API discovery module without hardcoding model
    versions in application code. Discovers models at runtime via 
    GET /v1beta/models, classifies into tiers (lite, standard, pro), caches in 
    memory with TTL, and implements Circuit Breaker protection.
==============================================================================
"""

import os
import json
import time
import re
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import requests
import yaml

# Configure logging
logger = logging.getLogger("ScamShield.ModelRegistry")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s", 
        datefmt="%H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class ModelRegistry:
    """
    Dynamic Model Registry for Google Gemini Cloud Fallback (Tier 2).
    Discovers available models via REST API, caches with TTL, and routes by tier.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        config_path: Optional[str] = None,
        auto_discover: bool = True,
    ):
        """
        Initialize the Dynamic Model Registry.

        Args:
            api_key: Google Gemini API key. Defaults to GEMINI_API_KEY or GOOGLE_API_KEY env vars.
            config_path: Path to gemini_models.yaml configuration file.
            auto_discover: Whether to discover models immediately on initialization.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
        self.config_path = config_path or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "config", "gemini_models.yaml"
        )
        self.config = self._load_config()
        
        # State & Caching
        self.cached_models_by_tier: Dict[str, List[str]] = {
            "lite": [],
            "standard": [],
            "pro": [],
        }
        self.all_discovered_models: List[Dict[str, Any]] = []
        self.last_fetch_time: float = 0.0
        self.ttl_seconds: int = self.config.get("cache", {}).get("ttl_seconds", 43200)
        
        # Circuit Breaker state
        self.consecutive_failures: int = 0
        self.failure_threshold: int = self.config.get("circuit_breaker", {}).get("failure_threshold", 3)
        self.cooldown_seconds: int = self.config.get("circuit_breaker", {}).get("cooldown_seconds", 300)
        self.circuit_open_until: float = 0.0

        # Load file cache or bootstrap fallbacks
        self._load_cached_state()

        if auto_discover and self.api_key:
            self.refresh(force=False)

    def _load_config(self) -> Dict[str, Any]:
        """Load YAML configuration or return safe defaults."""
        default_config = {
            "api": {
                "discovery_endpoint": "https://generativelanguage.googleapis.com/v1beta/models",
                "request_timeout_seconds": 10,
            },
            "cache": {
                "ttl_seconds": 43200,
                "file_cache_path": "config/.gemini_models_cache.json",
            },
            "circuit_breaker": {
                "failure_threshold": 3,
                "cooldown_seconds": 300,
            },
            "tier_routing": {
                "priority": ["lite", "standard", "pro"],
                "patterns": {
                    "lite": ["flash-lite", "flash_lite", "8b", "lite"],
                    "standard": ["flash", "instant"],
                    "pro": ["pro", "ultra", "advanced"],
                },
                "exclusions": ["embedding", "tts", "audio", "imagen", "vision-only", "robotics", "aqa"],
            },
            "bootstrap_fallbacks": {
                "lite": "gemini-3.5-flash-lite",
                "standard": "gemini-3.5-flash",
                "pro": "gemini-3.8-flash",
            },
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded = yaml.safe_load(f)
                    if isinstance(loaded, dict):
                        default_config.update(loaded)
                        logger.info(f"Loaded dynamic registry configuration from {self.config_path}")
            except Exception as e:
                logger.warning(f"Failed to parse config file {self.config_path}: {e}. Using defaults.")
        return default_config

    def _load_cached_state(self):
        """Load previously saved cache from disk, or initialize with bootstrap fallbacks."""
        cache_file = self.config.get("cache", {}).get("file_cache_path", "config/.gemini_models_cache.json")
        if not os.path.isabs(cache_file):
            cache_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), cache_file)

        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.cached_models_by_tier = data.get("tiers", {})
                    self.last_fetch_time = data.get("timestamp", 0.0)
                    logger.info(f"Loaded {sum(len(v) for v in self.cached_models_by_tier.values())} cached models from disk.")
                    return
            except Exception as e:
                logger.warning(f"Could not read model cache file: {e}")

        # Populate with bootstrap fallbacks
        fallbacks = self.config.get("bootstrap_fallbacks", {})
        for tier, model_name in fallbacks.items():
            self.cached_models_by_tier[tier] = [model_name]

    def _save_cached_state(self):
        """Save discovered models to disk for cold-start persistence."""
        cache_file = self.config.get("cache", {}).get("file_cache_path", "config/.gemini_models_cache.json")
        if not os.path.isabs(cache_file):
            cache_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), cache_file)

        try:
            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({
                    "timestamp": self.last_fetch_time,
                    "tiers": self.cached_models_by_tier,
                    "total_models": len(self.all_discovered_models)
                }, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to persist model cache: {e}")

    def is_circuit_open(self) -> bool:
        """Check if Circuit Breaker is active (blocking live discovery)."""
        if time.time() < self.circuit_open_until:
            return True
        return False

    def refresh(self, force: bool = False) -> bool:
        """
        Query Google Generative AI REST API to discover models.

        Args:
            force: If True, bypasses TTL check.

        Returns:
            bool: True if discovery succeeded or valid cache used, False on failure.
        """
        now = time.time()

        # Check TTL
        if not force and (now - self.last_fetch_time) < self.ttl_seconds and any(self.cached_models_by_tier.values()):
            return True

        # Check Circuit Breaker
        if self.is_circuit_open():
            logger.warning(f"Circuit Breaker ACTIVE. Remaining cooldown: {int(self.circuit_open_until - now)}s. Using cached models.")
            return True

        if not self.api_key:
            logger.warning("No Gemini API key supplied. Utilizing bootstrap fallback models.")
            return False

        endpoint = self.config.get("api", {}).get("discovery_endpoint", "https://generativelanguage.googleapis.com/v1beta/models")
        timeout = self.config.get("api", {}).get("request_timeout_seconds", 10)

        logger.info(f"Discovering live Google Gemini models via {endpoint}...")
        try:
            resp = requests.get(
                endpoint,
                params={"key": self.api_key},
                timeout=timeout,
                headers={"Accept": "application/json"}
            )

            if resp.status_code != 200:
                self.consecutive_failures += 1
                logger.error(f"Google API Discovery returned HTTP {resp.status_code}: {resp.text[:200]}")
                if self.consecutive_failures >= self.failure_threshold:
                    self.circuit_open_until = now + self.cooldown_seconds
                    logger.critical(f"Circuit Breaker TRIPPED! Google API unreachable. Cooling down for {self.cooldown_seconds}s.")
                return False

            data = resp.json()
            models_list = data.get("models", [])
            if not models_list:
                logger.warning("No models returned in Google API response.")
                return False

            # Reset circuit breaker on success
            self.consecutive_failures = 0
            self.circuit_open_until = 0.0
            self.all_discovered_models = models_list

            # Classify models into tiers
            self._classify_models(models_list)
            self.last_fetch_time = now
            self._save_cached_state()

            logger.info(
                f"Model Discovery Complete: Lite={len(self.cached_models_by_tier['lite'])}, "
                f"Standard={len(self.cached_models_by_tier['standard'])}, Pro={len(self.cached_models_by_tier['pro'])}"
            )
            return True

        except Exception as e:
            self.consecutive_failures += 1
            logger.error(f"Error querying Google Gemini model discovery API: {e}")
            if self.consecutive_failures >= self.failure_threshold:
                self.circuit_open_until = now + self.cooldown_seconds
                logger.critical(f"Circuit Breaker TRIPPED due to exceptions. Cooling down for {self.cooldown_seconds}s.")
            return False

    def _classify_models(self, raw_models: List[Dict[str, Any]]):
        """Filter out unsupported models and categorize into lite, standard, pro tiers."""
        patterns = self.config.get("tier_routing", {}).get("patterns", {})
        exclusions = self.config.get("tier_routing", {}).get("exclusions", [])

        tiers: Dict[str, List[str]] = {"lite": [], "standard": [], "pro": []}

        for m in raw_models:
            name = m.get("name", "")
            # Strip 'models/' prefix
            clean_name = name.replace("models/", "")
            
            # Check supported generation methods (must support text generation)
            supported_methods = m.get("supportedGenerationMethods", [])
            if "generateContent" not in supported_methods:
                continue

            # Check exclusions
            lower_name = clean_name.lower()
            if any(exc.lower() in lower_name for exc in exclusions):
                continue

            # Exclude experimental / obsolete preview checkpoints if needed, or sort properly
            # Classify into tier
            matched_tier = None
            for p in patterns.get("lite", []):
                if p.lower() in lower_name:
                    matched_tier = "lite"
                    break
            
            if not matched_tier:
                for p in patterns.get("pro", []):
                    if p.lower() in lower_name:
                        matched_tier = "pro"
                        break

            if not matched_tier:
                for p in patterns.get("standard", []):
                    if p.lower() in lower_name:
                        matched_tier = "standard"
                        break

            # If still unmatched but is a Gemini model, categorize as standard
            if not matched_tier and "gemini" in lower_name:
                matched_tier = "standard"

            if matched_tier:
                tiers[matched_tier].append(clean_name)

        # Sort each tier to put the newest versions first
        def version_key(model_str: str) -> tuple:
            # Extract version numbers like 2.5, 2.0, 1.5
            nums = re.findall(r"\d+\.?\d*", model_str)
            v_val = float(nums[0]) if nums else 0.0
            # Prefer non-preview over preview / experimental
            is_exp = 1 if ("exp" in model_str or "preview" in model_str) else 0
            return (v_val, -is_exp, len(model_str))

        for tier in tiers:
            tiers[tier].sort(key=version_key, reverse=True)

        # Fallback to bootstrap if any tier ended up empty
        fallbacks = self.config.get("bootstrap_fallbacks", {})
        for tier, fallback_model in fallbacks.items():
            if not tiers[tier]:
                tiers[tier] = [fallback_model]

        self.cached_models_by_tier = tiers

    def get_model(self, tier: str = "lite") -> str:
        """
        Get the best current active model name for a specific tier.

        Args:
            tier: One of 'lite', 'standard', 'pro'.

        Returns:
            str: Model name identifier (e.g. 'gemini-2.5-flash-lite').
        """
        tier = tier.lower()
        if tier not in self.cached_models_by_tier or not self.cached_models_by_tier[tier]:
            # Try cascade priority: lite -> standard -> pro
            for fallback_tier in self.config.get("tier_routing", {}).get("priority", ["lite", "standard", "pro"]):
                if self.cached_models_by_tier.get(fallback_tier):
                    return self.cached_models_by_tier[fallback_tier][0]
            # Final safety fallback
            return self.config.get("bootstrap_fallbacks", {}).get(tier, "gemini-2.5-flash-lite")

        return self.cached_models_by_tier[tier][0]

    def list_available_models(self, tier: Optional[str] = None) -> List[str]:
        """List all available models in the registry."""
        if tier:
            return list(self.cached_models_by_tier.get(tier.lower(), []))
        all_models = []
        for t_models in self.cached_models_by_tier.values():
            all_models.extend(t_models)
        return list(dict.fromkeys(all_models))

    def generate_content(
        self,
        prompt: str,
        tier: str = "lite",
        system_instruction: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:
        """
        Execute REST API call to Google Gemini for Tier 2 deep analysis.
        Completely decoupled from Google GenAI SDK versions.

        Args:
            prompt: User message / prompt for classification.
            tier: 'lite', 'standard', or 'pro'.
            system_instruction: Optional system instruction / role prompt.
            temperature: Sampling temperature (default 0.1 for high determinism).
            max_tokens: Max output tokens.

        Returns:
            dict containing: {
                'success': bool,
                'model_used': str,
                'tier': str,
                'text': str,
                'latency_ms': float,
                'raw_response': dict
            }
        """
        start_time = time.perf_counter()
        model_name = self.get_model(tier)

        if not self.api_key:
            return {
                "success": False,
                "model_used": model_name,
                "tier": tier,
                "text": "Simulated Tier 2 Analysis: API Key not configured. Fallback evaluation applied.",
                "latency_ms": (time.perf_counter() - start_time) * 1000,
                "error": "MISSING_API_KEY",
            }

        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        
        payload: Dict[str, Any] = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "responseMimeType": "application/json"
            }
        }

        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        try:
            resp = requests.post(
                endpoint,
                params={"key": self.api_key},
                json=payload,
                timeout=15,
                headers={"Content-Type": "application/json"}
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            if resp.status_code == 200:
                data = resp.json()
                try:
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        generated_text = parts[0].get("text", "") if parts else ""
                        return {
                            "success": True,
                            "model_used": model_name,
                            "tier": tier,
                            "text": generated_text,
                            "latency_ms": elapsed_ms,
                            "raw_response": data
                        }
                except Exception as parse_err:
                    logger.error(f"Error parsing Gemini response: {parse_err}")

            # If request failed with specific model, try standard or pro tier fallback
            logger.warning(f"Tier {tier} model '{model_name}' returned HTTP {resp.status_code}: {resp.text[:150]}")
            return {
                "success": False,
                "model_used": model_name,
                "tier": tier,
                "text": "",
                "latency_ms": elapsed_ms,
                "error": f"HTTP_{resp.status_code}: {resp.text[:200]}"
            }

        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            logger.error(f"REST API Exception calling Gemini model '{model_name}': {e}")
            return {
                "success": False,
                "model_used": model_name,
                "tier": tier,
                "text": "",
                "latency_ms": elapsed_ms,
                "error": str(e)
            }
