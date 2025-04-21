import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    
    def test_bold_italic_code_link_image(self):
        text = "This is **bold text**, this is *italic text*, and this is a `code block`. Here's an ![image](https://i.imgur.com/example.jpg) and a [link](https://example.com)."
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(", this is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(", and this is a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(". Here's an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/example.jpg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT)
        ]
        nodes = TextNode.text_to_textnode(text)
        self.assertEqual(nodes, expected_nodes)

    def test_no_formatting(self):
        text = "This is just plain text."
        expected_nodes = [
            TextNode("This is just plain text.", TextType.TEXT)
        ]
        nodes = TextNode.text_to_textnode(text)
        self.assertEqual(nodes, expected_nodes)
    
    def test_single_bold(self):
        text = "**Bold Text**"
        expected_nodes = [
            TextNode("Bold Text", TextType.BOLD)
        ]
        nodes = TextNode.text_to_textnode(text)
        self.assertEqual(nodes, expected_nodes)

    def test_single_italic(self):
        text = "*Italic Text*"
        expected_nodes = [
            TextNode("Italic Text", TextType.ITALIC)
        ]
        nodes = TextNode.text_to_textnode(text)
        self.assertEqual(nodes, expected_nodes)

    def test_single_code(self):
        text = "`Code Block`"
        expected_nodes = [
            TextNode("Code Block", TextType.CODE)
        ]
        nodes = TextNode.text_to_textnode(text)
        self.assertEqual(nodes, expected_nodes)

    def test_single_image(self):
        text = "![Image Alt Text](https://i.imgur.com/example.jpg)"
        expected_nodes = [
            TextNode("Image Alt Text", TextType.IMAGE, "https://i.imgur.com/example.jpg")
        ]
        nodes = TextNode.text_to_textnode(text)
        self.assertEqual(nodes, expected_nodes)

    def test_single_link(self):
        text = "[Link Text](https://example.com)"
        expected_nodes = [
            TextNode("Link Text", TextType.LINK, "https://example.com")
        ]
        nodes = TextNode.text_to_textnode(text)
        self.assertEqual(nodes, expected_nodes)

if __name__ == "__main__":
    unittest.main()
