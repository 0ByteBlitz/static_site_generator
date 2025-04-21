from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None and tag not in ['img', 'br', 'hr']:
            raise ValueError("LeafNode must have a value.")
        super().__init__(tag=tag, value=value, props=props, children=None)

    def to_html(self):
        if self.value is None and self.tag not in ['img', 'br', 'hr']:
            raise ValueError("LeafNode must have a value to render HTML.")
        
        if self.tag is None:
            return self.value
        
        if self.tag == 'img':
            # For img, handle it as a self-closing tag
            if not self.props:
                raise ValueError("Image must have 'src' and 'alt' properties.")
            attributes = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
            return f'<{self.tag} {attributes} />'
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def props_to_html(self):
        if self.props:
            return ' ' + ' '.join(f'{key}="{value}"' for key, value in self.props.items())
        return ''