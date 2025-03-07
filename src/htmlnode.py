

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        if tag is not None and not isinstance(tag, str):
            raise ValueError("tag must be a string or None")
        if value is not None and not isinstance(value, str):
            raise ValueError("value must be a string or None")
        if children is not None and not isinstance(children, list):
            raise ValueError("children must be a list or None")
        if props is not None and not isinstance(props, dict):
            raise ValueError("props must be a dictionary or None")
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
        if value == None:
            raise ValueError("Value can't be None for LeafNode!")
        super().__init__( tag, value, None, props)

    def to_html(self):
        if self.tag == None:
            return self.value
        if self.props != None:
            html_props = ""
            for key in self.props:
                html_props += f' {key}="{self.props[key]}"'
            return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag == None:
            raise ValueError("Tag can't be None for ParentNode!")
        if children == None:
            raise ValueError("Children can't be None for ParentNode!")
        super().__init__(tag, None, children, props)

    def to_html(self):
        parent_html = ""
        
        for node in self.children:
            parent_html += node.to_html()
        if self.props != None:
            html_props = ""
            for key in self.props:
                html_props += f' {key}="{self.props[key]}"'    
            return f"<{self.tag}{html_props}>{parent_html}</{self.tag}>"
        return f"<{self.tag}>{parent_html}</{self.tag}>"
    

        