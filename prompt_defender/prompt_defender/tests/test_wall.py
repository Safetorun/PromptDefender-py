import unittest
from ..core import WallExecutor, ValidationResult


class TestWallExecutor(unittest.TestCase):
    def setUp(self):
        self.wall_executor = WallExecutor()

    def test_is_user_input_safe(self):
        # Test the is_user_input_safe method with a safe prompt
        prompt = "Tell me a joke."
        result = self.wall_executor.is_user_input_safe(prompt)
        self.assertEqual(result, ValidationResult(unacceptable_prompt=False, modified_prompt=prompt))


if __name__ == '__main__':
    unittest.main()
