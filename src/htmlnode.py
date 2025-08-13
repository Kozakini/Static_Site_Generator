

class HTMLNode:
    def __init__(self, tag = None, value = None, props = None, children = None):
        self.tag = tag
        self.value = value
        self.props = props
        self.children = children

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop = self.props
        if prop is None:
            return ""
        else:
            for key, value in prop.items():
                return "".join([key.strip('"'),"=",f'"{value}"'])

    def __repr__(self):
        return f"HTMLNode( {self.tag}, {self.value}, {self.props}, {self.children})"

class LeafNode(HTMLNode):
    def __init__(self, tag , value,props = None):
        super().__init__(tag, value, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return f"{self.value}"
        else:
            match self.tag:
                case "a":
                    key , value = self.props.popitem()
                    return f"<a href={value}>{self.value}</a>"
                case "p":
                    return f"<p>{self.value}</p>"
                case _:
                    return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, props, children)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")

        else:
            children = ""
            for child in self.children:
                children += child.to_html()

            return f"<{self.tag}>{children}</{self.tag}>"
    def __repr__(self):
        return f"ParentNode( {self.tag}, {self.children}, {self.props})"

