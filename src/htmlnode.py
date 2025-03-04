

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
        tmp_str = ""
        for key in self.props:
            tmp_str = f'{tmp_str} {key}="{self.props[key]}"'
        return tmp_str[1:]
    
    def __repr__(self):        
        return f"\nTag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}"