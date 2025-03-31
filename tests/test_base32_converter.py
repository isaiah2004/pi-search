import unittest
from src.utils.base32_converter import ascii_to_base32

class TestBase32Converter(unittest.TestCase):

    def test_conversion_basic(self):
        self.assertEqual(ascii_to_base32("hello"), "H7LLO")
        self.assertEqual(ascii_to_base32("world"), "W7RLD")

    def test_conversion_with_special_characters(self):
        self.assertEqual(ascii_to_base32("hello, world!"), "H7LLO4W7RLD3")
        self.assertEqual(ascii_to_base32("test-case"), "T7STC7SE")

    def test_empty_string(self):
        self.assertEqual(ascii_to_base32(""), "")

    def test_conversion_with_spaces(self):
        self.assertEqual(ascii_to_base32("hello world"), "H7LLO7W7RLD")

    def test_conversion_with_mixed_case(self):
        self.assertEqual(ascii_to_base32("Hello World"), "H7LLO7W7RLD")

if __name__ == "__main__":
    unittest.main()