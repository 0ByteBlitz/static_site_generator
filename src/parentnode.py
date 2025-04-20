from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not tag:
            raise ValueError("Parentnode tag cannot be empty")
        if not children:
            raise ValueError("Parentnode children cannot be empty")

        super().__init__(tag=tag, value=None, props=props, children=children)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag.")
        if self.children is None:
            raise ValueError("ParentNode must have children.")

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    