import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from textnode import TextNode, TextType

class TestMarkdownAndTextNodeSplitter(unittest.TestCase):

    # Tests for Markdown Extraction
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


    # Tests for TextNode splitting (Images and Links)
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = TextNode.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Here is a [link to Google](https://www.google.com) and [link to GitHub](https://www.github.com)",
            TextType.TEXT,
        )
        new_nodes = TextNode.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here is a ", TextType.TEXT),
                TextNode("link to Google", TextType.LINK, "https://www.google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link to GitHub", TextType.LINK, "https://www.github.com"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode(
            "This is text with no images",
            TextType.TEXT,
        )
        new_nodes = TextNode.split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with no images", TextType.TEXT)], new_nodes)

    def test_split_links_no_links(self):
        node = TextNode(
            "This is just some text with no links",
            TextType.TEXT,
        )
        new_nodes = TextNode.split_nodes_link([node])
        self.assertListEqual([TextNode("This is just some text with no links", TextType.TEXT)], new_nodes)

    def test_split_images_with_extra_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/image.png) and some more text after",
            TextType.TEXT,
        )
        new_nodes = TextNode.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/image.png"),
                TextNode(" and some more text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_extra_text(self):
        node = TextNode(
            "Visit [Google](https://www.google.com) for searching and [GitHub](https://www.github.com) for code hosting",
            TextType.TEXT,
        )
        new_nodes = TextNode.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://www.google.com"),
                TextNode(" for searching and ", TextType.TEXT),
                TextNode("GitHub", TextType.LINK, "https://www.github.com"),
                TextNode(" for code hosting", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_images_in_one_text(self):
        node = TextNode(
            "This is ![image1](https://i.imgur.com/1.png) and ![image2](https://i.imgur.com/2.png)",
            TextType.TEXT,
        )
        new_nodes = TextNode.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/2.png"),
            ],
            new_nodes,
        )

    def test_multiple_links_in_one_text(self):
        node = TextNode(
            "Click [here](https://example.com) and [there](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = TextNode.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://example.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("there", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )


if __name__ == '__main__':
    unittest.main()
