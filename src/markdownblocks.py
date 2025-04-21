from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode

from enum import Enum, auto
import re

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    ULIST = auto()
    OLIST = auto()

class MarkdownBlock:
    @staticmethod
    def markdown_to_blocks(markdown):
        blocks = [block.strip() for block in markdown.strip().split("\n\n")]
        return blocks

    @staticmethod
    def block_to_block_type(block):
        if block.startswith("```"):
            return BlockType.CODE
        elif block.startswith("#"):
            return BlockType.HEADING
        elif block.startswith(">"):
            return BlockType.QUOTE
        elif re.match(r"(\*|-|\+)\s", block) or block.startswith("- "):
            return BlockType.ULIST
        elif re.match(r"\d+\.\s", block):
            return BlockType.OLIST
        else:
            return BlockType.PARAGRAPH

    @staticmethod
    def markdown_to_html_node(markdown):
        blocks = MarkdownBlock.markdown_to_blocks(markdown)
        children = []

        for block in blocks:
            block_type = MarkdownBlock.block_to_block_type(block)

            if block_type == BlockType.PARAGRAPH:
                node = MarkdownBlock.handle_paragraph(block)
            elif block_type == BlockType.CODE:
                node = MarkdownBlock.handle_code(block)
            elif block_type == BlockType.HEADING:
                node = MarkdownBlock.handle_heading(block)
            elif block_type == BlockType.QUOTE:
                node = MarkdownBlock.handle_quote(block)
            elif block_type == BlockType.ULIST:
                node = MarkdownBlock.handle_ulist(block)
            elif block_type == BlockType.OLIST:
                node = MarkdownBlock.handle_olist(block)
            else:
                continue

            children.append(node)

        return ParentNode("div", children)

    @staticmethod
    def handle_paragraph(block):
        flat = " ".join(block.split())
        formatted = MarkdownBlock.apply_inline_formatting(flat)
        return LeafNode("p", formatted)

    @staticmethod
    def handle_code(block):
        lines = block.split("\n")[1:-1]  # remove ```
        content = "\n".join(line.lstrip() for line in lines) + "\n"
        code_node = LeafNode("code", content)
        return ParentNode("pre", [code_node])

    @staticmethod
    def handle_heading(block):
        level = len(block) - len(block.lstrip("#"))
        tag = f"h{level}"
        text = block[level:].strip()
        formatted = MarkdownBlock.apply_inline_formatting(text)
        return LeafNode(tag, formatted)

    @staticmethod
    def handle_quote(block):
        lines = [line.lstrip("> ").strip() for line in block.split("\n")]
        text = " ".join(lines)
        formatted = MarkdownBlock.apply_inline_formatting(text)
        return LeafNode("blockquote", formatted)

    @staticmethod
    def handle_ulist(block):
        items = [line.lstrip("-*+ ").strip() for line in block.split("\n")]
        children = [LeafNode("li", MarkdownBlock.apply_inline_formatting(item)) for item in items]
        return ParentNode("ul", children)

    @staticmethod
    def handle_olist(block):
        lines = block.split("\n")
        children = []
        for line in lines:
            match = re.match(r"\d+\.\s+(.*)", line)
            if match:
                item = match.group(1).strip()
                children.append(LeafNode("li", MarkdownBlock.apply_inline_formatting(item)))
        return ParentNode("ol", children)

    @staticmethod
    def apply_inline_formatting(text):
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'_([^_]+)_', r'<i>\1</i>', text)
        return text
