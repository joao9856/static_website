

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return None
        html_props = ""
        for key in self.props:
            html_props += f' {key}="{self.props[key]}"'
        return html_props[1:]
    
    def __repr__(self):        
        return f"\nTag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props)
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        if self.props != None:
            html_props = ""
            for key in self.props:
                html_props += f' {key}="{self.props[key]}"'
            return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
        