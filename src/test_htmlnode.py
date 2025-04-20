import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_single(self):
        node = HTMLNode(tag="a", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(tag="a", props={"href": "https://example.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertIn(' href="https://example.com"', result)
        self.assertIn(' target="_blank"', result)
        self.assertTrue(result.startswith(" "))

    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello", props={"class": "text-bold"})
        repr_str = repr(node)
        self.assertIn("HTMLNode", repr_str)
        self.assertIn("tag=p", repr_str)
        self.assertIn("value=Hello", repr_str)
        self.assertIn("'class': 'text-bold'", repr_str)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me", {"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">Click me</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")

    def test_leaf_raises_without_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None) 

if __name__ == "__main__":
    unittest.main()
