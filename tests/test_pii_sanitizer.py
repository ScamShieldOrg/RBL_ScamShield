# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipeline.pii_sanitizer import MessagePIISanitizer

class TestMessagePIISanitizer(unittest.TestCase):

    def setUp(self):
        self.sanitizer = MessagePIISanitizer()

    def test_sanitize_phone_numbers(self):
        msg = "Lien he ngay 0912345678 hoac +84987654321 de nhan thuong."
        clean, manifest = self.sanitizer.sanitize(msg)
        self.assertNotIn("0912345678", clean)
        self.assertNotIn("+84987654321", clean)
        self.assertIn("[PHONE_REDACTED]", clean)
        self.assertEqual(len(manifest["phone"]), 2)

    def test_sanitize_otp_codes(self):
        msg = "Ma OTP cua ban la 839201. Khong chia se ma nay voi bat ky ai."
        clean, manifest = self.sanitizer.sanitize(msg)
        self.assertNotIn("839201", clean)
        self.assertIn("[OTP_REDACTED]", clean)
        self.assertEqual(len(manifest["otp"]), 1)

    def test_sanitize_bank_account(self):
        msg = "Vui long chuyen tien vao STK: 1903657891234 tai Vietcombank."
        clean, manifest = self.sanitizer.sanitize(msg)
        self.assertNotIn("1903657891234", clean)
        self.assertIn("[ACCOUNT_REDACTED]", clean)
        self.assertEqual(len(manifest["account"]), 1)

    def test_sanitize_cccd(self):
        msg = "Xac thuc dinh danh CCCD: 001202009876 truoc 24h."
        clean, manifest = self.sanitizer.sanitize(msg)
        self.assertNotIn("001202009876", clean)
        self.assertIn("[CITIZEN_ID_REDACTED]", clean)

    def test_sanitize_balance(self):
        msg = "Bien dong so du: -500,000 VND. So du con lai: 15,200,000 VND."
        clean, manifest = self.sanitizer.sanitize(msg)
        self.assertNotIn("500,000 VND", clean)
        self.assertIn("[BALANCE_REDACTED]", clean)

if __name__ == "__main__":
    unittest.main()
