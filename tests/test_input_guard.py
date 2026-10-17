import json
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from llm_security.input_guard import validate_input


DATASET_PATH = PROJECT_ROOT / "data" / "attack_dataset.json"


HARMLESS_PROMPTS = [
    "Please forget my previous question about solar panels.",
    "What are the rules for installing solar panels?",
    "How do I override a system setting on my computer?",
    "Explain the instructions for maintaining an HVAC system.",
    "Ignore my previous question and explain energy efficiency instead.",
    "What system instructions should employees follow to save electricity?",
]


class TestInputGuard(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(DATASET_PATH, "r", encoding="utf-8") as file:
            cls.test_cases = json.load(file)

    def test_attack_prompts_are_blocked(self):
        attacks = [
            case for case in self.test_cases
            if case["category"] != "benign"
        ]

        for case in attacks:
            with self.subTest(test_id=case["id"]):
                result = validate_input(case["prompt"])
                self.assertFalse(result["allowed"])

    def test_benign_dataset_prompts_are_allowed(self):
        benign_cases = [
            case for case in self.test_cases
            if case["category"] == "benign"
        ]

        for case in benign_cases:
            with self.subTest(test_id=case["id"]):
                result = validate_input(case["prompt"])
                self.assertTrue(result["allowed"])

    def test_harmless_diagnostic_prompts_are_allowed(self):
        for prompt in HARMLESS_PROMPTS:
            with self.subTest(prompt=prompt):
                result = validate_input(prompt)
                self.assertTrue(result["allowed"])

    def test_empty_input_is_rejected(self):
        for prompt in ("", "   ", "\n\t"):
            with self.subTest(prompt=repr(prompt)):
                result = validate_input(prompt)
                self.assertFalse(result["allowed"])
                self.assertEqual(
                    result["reason"],
                    "empty_or_invalid_input",
                )

    def test_non_string_input_is_rejected(self):
        for prompt in (None, 123, [], {}):
            with self.subTest(prompt=repr(prompt)):
                result = validate_input(prompt)
                self.assertFalse(result["allowed"])
                self.assertEqual(
                    result["reason"],
                    "empty_or_invalid_input",
                )


if __name__ == "__main__":
    unittest.main()