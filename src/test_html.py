import unittest
from md_to_html import extract_title

class test(unittest.TestCase):
    def test_header(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
