import unittest
from wall.xml_scanner import BasicXmlScanner

XML_TAG = "tag"


class TestBasicXmlScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = BasicXmlScanner()

    def test_check_for_xml_tag(self):
        text_to_scan = "<tag>Some content</tag>"
        self.assertTrue(self.scanner.validate_prompt(text_to_scan, XML_TAG).unacceptable_prompt)

        text_to_scan = "No tags here"
        self.assertFalse(self.scanner.validate_prompt(text_to_scan, XML_TAG).unacceptable_prompt)


if __name__ == '__main__':
    unittest.main()
