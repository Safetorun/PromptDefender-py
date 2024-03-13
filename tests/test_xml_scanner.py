import unittest
from wall.xml_scanner import BasicXmlScanner


class TestBasicXmlScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = BasicXmlScanner(xml_tag='tag')

    def test_check_for_xml_tag(self):
        text_to_scan = "<tag>Some content</tag>"
        self.assertTrue(self.scanner.check_for_xml_tag(text_to_scan))

        text_to_scan = "No tags here"
        self.assertFalse(self.scanner.check_for_xml_tag(text_to_scan))


if __name__ == '__main__':
    unittest.main()
