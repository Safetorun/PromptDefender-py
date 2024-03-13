import unittest
from wall.prompt_validator import PromptValidator


class TestPromptValidator(unittest.TestCase):

    def test_validate_length(self):
        pv = PromptValidator(max_length=5)
        self.assertFalse(pv.validate_prompt("This prompt is longer than acceptable"))

    def test_validate_length_is_ok(self):
        pv = PromptValidator(max_length=100)
        self.assertTrue(pv.validate_prompt("This prompt is longer than acceptable"))

    def test_validate_prompt(self):
        pv = PromptValidator(max_length=100, acceptable_values=['hello', 'world'])
        self.assertTrue(pv.validate_prompt('hello'))
        self.assertTrue(pv.validate_prompt('world'))
        self.assertFalse(pv.validate_prompt('invalid'))
        self.assertFalse(pv.validate_prompt('hell'))

        pv = PromptValidator(max_length=None, acceptable_values=None)
        self.assertTrue(pv.validate_prompt('any value'))


if __name__ == '__main__':
    unittest.main()
