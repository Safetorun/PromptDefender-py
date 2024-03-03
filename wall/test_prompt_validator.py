import unittest
from wall.prompt_validator import BasicXmlScanner


class TestBasicXmlScanner(unittest.TestCase):
    def test_check_for_xml_tag(self):
        # Test when xml_tag is None and prompt does not contain any XML tags
        scanner = BasicXmlScanner(xml_tag=None)
        self.assertFalse(scanner.check_for_xml_tag("No tags here"))

        # Test when xml_tag is None and prompt contains XML tags
        self.assertFalse(scanner.check_for_xml_tag("<tag>Some content</tag>"))

        # Test when xml_tag is not None and prompt does not contain the specified XML tag
        scanner = BasicXmlScanner(xml_tag='tag')
        self.assertFalse(scanner.check_for_xml_tag("No tags here"))

        # Test when xml_tag is not None and prompt contains the specified XML tag
        self.assertTrue(scanner.check_for_xml_tag("<tag>Some content</tag>"))


if __name__ == '__main__':
    unittest.main()
