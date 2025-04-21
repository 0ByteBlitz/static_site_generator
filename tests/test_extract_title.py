import unittest

from main import extract_title

class TestMarkdownFunctions(unittest.TestCase):
    def test_extract_title(self):
        # Test with valid markdown with an H1 header
        markdown = "# Hello World\nThis is a test."
        title = extract_title(markdown)
        self.assertEqual(title, "Hello World")

        # Test with invalid markdown (no H1 header)
        markdown = "This is a test."
        with self.assertRaises(ValueError):
            extract_title(markdown)

        # Test with markdown with leading/trailing spaces around the title
        markdown = "   # Leading Spaces\nThis is a test."
        title = extract_title(markdown)
        self.assertEqual(title, "Leading Spaces")

if __name__ == "__main__":
    unittest.main()
