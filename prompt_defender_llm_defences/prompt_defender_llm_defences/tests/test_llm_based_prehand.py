import unittest
from unittest.mock import Mock

from ..wall.llm_prehand_defence import LlmBasedPrehand
from prompt_defender.core import ValidationResult


class TestLlmBasedPrehand(unittest.TestCase):
    def setUp(self):
        self.llm_mock = Mock()
        self.parser_mock = Mock()
        self.parser_mock.return_value = 'yes'
        self.llm_mock.return_value = 'yes'
        self.defence = LlmBasedPrehand(llm=self.llm_mock, parser=self.parser_mock)

    def test_check_user_input(self):
        instruction = "Tell me a joke."
        result = self.defence.is_user_input_safe(instruction)
        self.assertEqual(result, ValidationResult(unacceptable_prompt=True, modified_prompt=instruction))


if __name__ == '__main__':
    unittest.main()
