

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def __repr__(self):
        attrs = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return f"HTMLNode({self.tag}, {self.value}, {{{attrs}}})"

    def to_html(self):
        raise NotImplementedError("TBD")
    
    def props_to_html(self):
        prop_string = ""
        for prop in self.props or {}:
            prop_string += f'{prop}="{self.props[prop]}" '
        return prop_string.strip()
