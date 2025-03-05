import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("h1", "banana bros", props={"href": "https://www.youtube.com", "target": "_blank"})
        self.assertEqual(node.__repr__(), "\nTag: h1\nValue: banana bros\nChildren: None\nProps: {'href': 'https://www.youtube.com', 'target': '_blank'}")
        self.assertEqual(node.props_to_html(), 'href="https://www.youtube.com" target="_blank"')

    def test_props_to_html2(self):
        node = HTMLNode(props={})
        self.assertEqual(node.__repr__(), "\nTag: None\nValue: None\nChildren: None\nProps: {}")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html3(self):    
        node = HTMLNode()
        self.assertEqual(node.__repr__(), "\nTag: None\nValue: None\nChildren: None\nProps: None")
        self.assertEqual(node.props_to_html(), None)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", props={"href": "https://www.youtube.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.youtube.com">Hello, world!</a>')
    
    def test_leaf_to_html_None(self):
        node = LeafNode(value="Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

if __name__ == "__main__":
    unittest.main()