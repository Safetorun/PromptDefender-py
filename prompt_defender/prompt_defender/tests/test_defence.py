import unittest

from prompt_defender import Defence, KeepExecutor, CompositeWallExecutorBuilder, build_drawbridge, build_xml_scanner, \
    build_prompt_validator


class TestDefence(unittest.TestCase):
    def setUp(self):
        compose_wall = CompositeWallExecutorBuilder()
        compose_wall.add_wall_executor(build_xml_scanner)
        compose_wall.add_wall_executor(build_prompt_validator())

        self.defence = Defence(
            wall=compose_wall.build(),
            keep=lambda: KeepExecutor(),
            drawbridge=build_drawbridge(allow_unsafe_scripts=True)
        )

    def test_prepare_prompt(self):
        prepared_prompt = self.defence.prepare_prompt("Your job is to answer user questions about cats {user_question}",
                                                      False)
        self.assertIsNotNone(prepared_prompt)

    def test_check_user_input(self):
        prepared_prompt = self.defence.prepare_prompt("Your job is to answer user questions about cats {user_question}",
                                                      False)
        result = self.defence.is_user_input_safe("What is the best cat? " + prepared_prompt.safe_prompt)
        self.assertIsNotNone(result)

    def test_check_prompt_output(self):
        output = self.defence.check_prompt_output("This should all be okay ")
        self.assertTrue(output.is_safe)
        self.assertIsNotNone(output.cleaned_response)


if __name__ == '__main__':
    unittest.main()
