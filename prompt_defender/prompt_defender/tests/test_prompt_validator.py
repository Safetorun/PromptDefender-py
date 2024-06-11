import unittest
from ..wall.prompt_validator import PromptValidator


class TestPromptValidator(unittest.TestCase):

    def test_validate_length(self):
        pv = PromptValidator(max_length=5)
        self.assertTrue(pv.is_user_input_safe("This prompt is longer than acceptable").unacceptable_prompt)

    def test_validate_length_is_ok(self):
        pv = PromptValidator(max_length=100)
        self.assertFalse(pv.is_user_input_safe("This prompt is not longer than acceptable").unacceptable_prompt)

    def test_is_user_input_safe(self):
        pv = PromptValidator(max_length=100, acceptable_values=['hello', 'world'])
        self.assertFalse(pv.is_user_input_safe('hello').unacceptable_prompt)
        self.assertFalse(pv.is_user_input_safe('world').unacceptable_prompt)
        self.assertTrue(pv.is_user_input_safe('invalid').unacceptable_prompt)
        self.assertTrue(pv.is_user_input_safe('hell').unacceptable_prompt)

        pv = PromptValidator(max_length=None, acceptable_values=None)
        self.assertFalse(pv.is_user_input_safe('any value').unacceptable_prompt)


if __name__ == '__main__':
    unittest.main()
