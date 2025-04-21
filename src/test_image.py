import unittest

from textnode import TextNode

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(TextNode.extract_markdown_images(text), expected)

    def test_extract_multiple_images(self):
        text = "![one](https://one.com) and ![two](https://two.com)"
        expected = [("one", "https://one.com"), ("two", "https://two.com")]
        self.assertListEqual(TextNode.extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "Here is a [link](https://example.com)"
        expected = [("link", "https://example.com")]
        self.assertListEqual(TextNode.extract_markdown_links(text), expected)

    def test_extract_multiple_links(self):
        text = "[one](https://one.com) and [two](https://two.com)"
        expected = [("one", "https://one.com"), ("two", "https://two.com")]
        self.assertListEqual(TextNode.extract_markdown_links(text), expected)

    def test_ignore_image_links_in_links(self):
        text = "This is ![an image](https://img.com) and [a link](https://link.com)"
        expected = [("a link", "https://link.com")]
        self.assertListEqual(TextNode.extract_markdown_links(text), expected)

if __name__ == "__main__":
    unittest.main()
