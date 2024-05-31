import unittest

import requests_mock

from prompt_defender.wall.prompt_defender_client import PromptDefenderClient, WallResponse


class TestPromptDefenderClient(unittest.TestCase):
    def setUp(self):
        self.client = PromptDefenderClient(api_key="test_key")
        self.mock_server = requests_mock.Mocker()

    def test_call_remote_wall(self):
        with self.mock_server:
            self.mock_server.post("https://prompt.safetorun.com/wall", json={
                "potential_jailbreak": False,
                "contains_pii": False,
                "potential_xml_escaping": False,
                "suspicious_user": False,
                "suspicious_session": False
            })
            response = self.client.call_remote_wall("test_prompt")
            self.assertIsInstance(response, WallResponse)
            self.assertFalse(response.potential_jailbreak)
            self.assertFalse(response.contains_pii)
            self.assertFalse(response.potential_xml_escaping)
            self.assertFalse(response.suspicious_user)
            self.assertFalse(response.suspicious_session)

    def tearDown(self):
        self.mock_server.stop()


if __name__ == "__main__":
    unittest.main()
