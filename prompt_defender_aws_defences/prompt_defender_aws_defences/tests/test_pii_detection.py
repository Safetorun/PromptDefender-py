import unittest
from unittest.mock import patch, Mock

from botocore.exceptions import BotoCoreError, ClientError

from ..wall.pii_detection import AwsPIIScanner, AwsPIIScannerWallExecutor, ScanResult, PiiEntity


class TestAwsPIIScanner(unittest.TestCase):
    @patch('boto3.Session')
    def test_scan_detects_pii(self, mock_boto_session):
        mock_comprehend = Mock()
        mock_comprehend.detect_pii_entities.return_value = {
            'Entities': [{'Type': 'EMAIL', 'Score': 0.99}]
        }
        mock_boto_session.return_value.client.return_value = mock_comprehend

        pii_scanner = AwsPIIScanner()
        result = pii_scanner.scan("My email is john.doe@example.com")

        self.assertTrue(result.containing_pii)
        self.assertEqual(len(result.entities), 1)
        self.assertEqual(result.entities[0].Type, 'EMAIL')
        self.assertAlmostEqual(result.entities[0].Score, 0.99)

    @patch('boto3.Session')
    def test_scan_no_pii_detected(self, mock_boto_session):
        mock_comprehend = Mock()
        mock_comprehend.detect_pii_entities.return_value = {
            'Entities': []
        }
        mock_boto_session.return_value.client.return_value = mock_comprehend

        pii_scanner = AwsPIIScanner()
        result = pii_scanner.scan("There is no PII here.")

        self.assertFalse(result.containing_pii)
        self.assertEqual(len(result.entities), 0)

    @patch('boto3.Session')
    def test_scan_handles_boto_error(self, mock_boto_session):
        mock_comprehend = Mock()
        mock_comprehend.detect_pii_entities.side_effect = BotoCoreError
        mock_boto_session.return_value.client.return_value = mock_comprehend

        pii_scanner = AwsPIIScanner()
        result = pii_scanner.scan("My email is john.doe@example.com")

        self.assertFalse(result.containing_pii)
        self.assertEqual(len(result.entities), 0)

    @patch('boto3.Session')
    def test_scan_handles_client_error(self, mock_boto_session):
        mock_comprehend = Mock()
        mock_comprehend.detect_pii_entities.side_effect = ClientError({'Error': {}}, 'detect_pii_entities')
        mock_boto_session.return_value.client.return_value = mock_comprehend

        pii_scanner = AwsPIIScanner()
        result = pii_scanner.scan("My email is john.doe@example.com")

        self.assertFalse(result.containing_pii)
        self.assertEqual(len(result.entities), 0)


class TestAwsPIIScannerWallExecutor(unittest.TestCase):
    def setUp(self):
        self.wall_executor = AwsPIIScannerWallExecutor()

    @patch.object(AwsPIIScanner, 'scan', return_value=ScanResult(containing_pii=True, entities=[PiiEntity(Type='EMAIL', Score=0.99)]))
    def test_is_user_input_safe_detects_pii(self, mock_scan):
        result = self.wall_executor.is_user_input_safe("My email is john.doe@example.com")
        self.assertTrue(result.unacceptable_prompt)

    @patch.object(AwsPIIScanner, 'scan', return_value=ScanResult(containing_pii=False, entities=[]))
    def test_is_user_input_safe_no_pii_detected(self, mock_scan):
        result = self.wall_executor.is_user_input_safe("There is no PII here.")
        self.assertFalse(result.unacceptable_prompt)

    @patch.object(AwsPIIScanner, 'scan', return_value=ScanResult(containing_pii=True, entities=[PiiEntity(Type='EMAIL', Score=0.99)]))
    def test_is_user_input_safe_returns_modified_prompt(self, mock_scan):
        prompt = "My email is john.doe@example.com"
        result = self.wall_executor.is_user_input_safe(prompt)
        self.assertEqual(result.modified_prompt, prompt)


if __name__ == '__main__':
    unittest.main()