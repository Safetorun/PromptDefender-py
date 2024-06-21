import unittest

from ..core.keep_executor import KeepExecutor, SafePromptResponse


class TestKeepExecutor(unittest.TestCase):
    def setUp(self):
        self.keep_executor = KeepExecutor()

    def test_generate_prompt(self):
        safe_prompt_response = self.keep_executor.generate_prompt(
            "Your job is to answer user questions about cats {user_question}", False)
        self.assertIsInstance(safe_prompt_response, SafePromptResponse)
        self.assertIsNotNone(safe_prompt_response.safe_prompt)


if __name__ == '__main__':
    unittest.main()
