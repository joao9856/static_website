import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("h1", "banana bros", props={"href": "https://www.youtube.com", "target": "_blank"})
        print(node)
        print(node.props_to_html())

    def test_props_to_html2(self):
        node = HTMLNode(props={})
        print(node)
        print(node.props_to_html())

    def test_props_to_html3(self):    
        node = HTMLNode()
        print(node)
        print(node.props_to_html())