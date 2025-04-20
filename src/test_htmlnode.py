import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
