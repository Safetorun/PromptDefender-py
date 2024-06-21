import unittest

from ..core.drawbridge_executor import DrawbridgeExecutor, DrawbridgeResponse


class TestDrawbridgeExecutor(unittest.TestCase):
    def setUp(self):
        self.drawbridge_executor = DrawbridgeExecutor()

    def test_validate_response_and_clean(self):
        # Test the validate_response_and_clean method with a safe response
        response = "This is a safe response."
        result = self.drawbridge_executor.validate_response_and_clean(response)
        self.assertIsInstance(result, DrawbridgeResponse)
        self.assertTrue(result.is_safe)
        self.assertEqual(result.cleaned_response, response)


if __name__ == '__main__':
    unittest.main()