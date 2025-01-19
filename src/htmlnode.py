class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        return ''.join(f' {key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
       return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag ='{self.tag}', value='{self.value}', props='{self.props})'"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag missing")
        if self.children == None or len(self.children) == 0:
            raise ValueError("No children")
        children_list = []
        for child in self.children:
            children_list.append(child.to_html())
        return f"<{self.tag}{self.props_to_html()}>{''.join(children_list)}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode(tag ='{self.tag}', children='{self.children}', props='{self.props})'"