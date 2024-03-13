import unittest
from unittest.mock import MagicMock

from wall.wall_executor import WallExecutor, ValidationResult


class TestWallExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = WallExecutor()
        self.executor.xml_scanner = MagicMock()
        self.executor.prompt_validator = MagicMock()
        self.executor.remote_wall_checker = MagicMock()

    def test_validate_prompt(self):
        self.executor.xml_scanner.check_for_xml_tag.return_value = False
        self.executor.prompt_validator.validate_prompt.return_value = True
        self.executor.remote_wall_checker.call_remote_wall.return_value = ValidationResult(
            contains_pii=False,
            potential_jailbreak=False,
            potential_xml_escaping=False,
            suspicious_user=False,
            suspicious_session=False
        )

        result = self.executor.validate_prompt("test_prompt")

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.contains_pii)
        self.assertFalse(result.potential_jailbreak)
        self.assertFalse(result.potential_xml_escaping)
        self.assertFalse(result.suspicious_user)
        self.assertFalse(result.suspicious_session)

    def tearDown(self):
        self.executor.xml_scanner = None
        self.executor.prompt_validator = None
        self.executor.remote_wall_checker = None


if __name__ == "__main__":
    unittest.main()
