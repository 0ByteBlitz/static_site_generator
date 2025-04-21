import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from textnode import TextNode, TextType


class TestTextNodeSplitter(unittest.TestCase):

    def test_code_delimiter(self):
        node = TextNode("Here is some `code` inside text", TextType.TEXT)
        result = TextNode.split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Here is some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" inside text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_bold_delimiter(self):
        node = TextNode("This has a **bold** word", TextType.TEXT)
        result = TextNode.split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This has a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_bold_delimiters(self):
        node = TextNode("A **bold** and another **strong** word", TextType.TEXT)
        result = TextNode.split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and another ", TextType.TEXT),
            TextNode("strong", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("No formatting here", TextType.TEXT)
        result = TextNode.split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("No formatting here", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter_raises(self):
        node = TextNode("Oops this is **broken", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            TextNode.split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertIn("unmatched delimiter", str(context.exception))

    def test_mixed_text_nodes(self):
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
        ]
        result = TextNode.split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
