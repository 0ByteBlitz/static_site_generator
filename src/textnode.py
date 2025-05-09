import re

from enum import Enum

from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text)
        elif text_node.text_type == TextType.LINK:
            if not text_node.url:
                raise ValueError("Link node must have a URL.")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            if not text_node.url:
                raise ValueError("Image node must have a URL.")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        else:
            raise ValueError(f"Unsupported text type: {text_node.text_type}")
    
    @staticmethod
    def split_nodes_delimiter(old_nodes, delimiter, text_type):
        new_nodes = []
        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue
            
            parts = node.text.split(delimiter)
            
            if len(parts) % 2 == 0:
                raise Exception(f"Invalid Markdown: unmatched delimiter '{delimiter}' in '{node.text}'")

            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part:
                        new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    if part:
                        new_nodes.append(TextNode(part, text_type))
        return new_nodes
    
    @staticmethod
    def extract_markdown_images(text):
        pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        return re.findall(pattern, text)

    @staticmethod
    def extract_markdown_links(text):
        pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
        return re.findall(pattern, text)

    @staticmethod
    def split_nodes_image(old_nodes):
        new_nodes = []
        pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"  # Regex to match the image markdown syntax

        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue

            text = node.text
            last_index = 0

            for match in re.finditer(pattern, text):
                start, end = match.span()
                alt_text = match.group(1)
                url = match.group(2)

                # Add the text before the image (excluding the '!' part)
                if start > last_index:
                    pre_text = text[last_index:start]
                    new_nodes.append(TextNode(pre_text, TextType.TEXT))

                # Add the image node (alt text and url)
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

                last_index = end

            # Add any remaining text after the last match
            if last_index < len(text):
                remaining_text = text[last_index:]
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))

        return new_nodes


    @staticmethod
    def split_nodes_link(old_nodes):
        new_nodes = []
        pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue

            text = node.text
            last_index = 0

            for match in re.finditer(pattern, text):
                start, end = match.span()
                link_text = match.group(1)
                url = match.group(2)

                # Add the text before the link
                if start > last_index:
                    pre_text = text[last_index:start]
                    new_nodes.append(TextNode(pre_text, TextType.TEXT))

                # Add the link node
                new_nodes.append(TextNode(link_text, TextType.LINK, url))

                last_index = end

            # Add any remaining text after the last match
            if last_index < len(text):
                remaining_text = text[last_index:]
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))

        return new_nodes
    

    @staticmethod
    def text_to_textnode(text):
        new_nodes = []
        # Split the text into parts based on the delimiters
        bold_parts = TextNode.split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
        italic_parts = TextNode.split_nodes_delimiter(bold_parts, "*", TextType.ITALIC)
        code_parts = TextNode.split_nodes_delimiter(italic_parts, "`", TextType.CODE)
        link_parts = TextNode.split_nodes_link(code_parts)
        image_parts = TextNode.split_nodes_image(link_parts)
        # Add the parts to the new nodes list
        for node in image_parts:
            if node.text_type == TextType.TEXT and node.text.strip() == "":
                continue
            new_nodes.append(node)
        return new_nodes
    
    

    
