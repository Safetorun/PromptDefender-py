import unittest
from wall.prompt_validator import PromptValidator


class TestPromptValidator(unittest.TestCase):

    def test_validate_length(self):
        pv = PromptValidator(max_length=5)
        self.assertTrue(pv.validate_prompt("This prompt is longer than acceptable").unacceptable_prompt)

    def test_validate_length_is_ok(self):
        pv = PromptValidator(max_length=100)
        self.assertFalse(pv.validate_prompt("This prompt is not longer than acceptable").unacceptable_prompt)

    def test_validate_prompt(self):
        pv = PromptValidator(max_length=100, acceptable_values=['hello', 'world'])
        self.assertFalse(pv.validate_prompt('hello').unacceptable_prompt)
        self.assertFalse(pv.validate_prompt('world').unacceptable_prompt)
        self.assertTrue(pv.validate_prompt('invalid').unacceptable_prompt)
        self.assertTrue(pv.validate_prompt('hell').unacceptable_prompt)

        pv = PromptValidator(max_length=None, acceptable_values=None)
        self.assertFalse(pv.validate_prompt('any value').unacceptable_prompt)


if __name__ == '__main__':
    unittest.main()
