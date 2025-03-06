import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_grandchildren_and_props(self):
        grandchild_node = LeafNode("a", "grandchild", props={"href": "https://youtube.com"})
        child_node = ParentNode("span", [grandchild_node], props={"style": "color:blue"})
        parent_node = ParentNode("div", [child_node], props={"class": "myDiv"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="myDiv"><span style="color:blue"><a href="https://youtube.com">grandchild</a></span></div>',
        )
    
    def test_to_html_children_none(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

    def test_to_html_tag_none(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("a", "child")])     

    def test_to_html_no_children(self):
        with self.assertRaises(TypeError):
            ParentNode("div")

    def test_to_html_no_tag(self):
        with self.assertRaises(TypeError):
            ParentNode(children=[LeafNode("a", "child")])

    def test_to_html_with_multiple_children_and_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("b", "grandchild2")
        grandchild_node3 = LeafNode("b", "grandchild3")
        grandchild_node4 = LeafNode("b", "grandchild4")
        grandchild_node5 = LeafNode("b", "grandchild5")
        grandchild_node6 = LeafNode("b", "grandchild6")
        child_node = ParentNode("span", [grandchild_node, grandchild_node2])
        child_node2 = ParentNode("span", [grandchild_node3, grandchild_node4])
        child_node3 = ParentNode("span", [grandchild_node5, grandchild_node6])
        parent_node = ParentNode("div", [child_node, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><b>grandchild2</b></span><span><b>grandchild3</b><b>grandchild4</b></span><span><b>grandchild5</b><b>grandchild6</b></span></div>",
        )
if __name__ == "__main__":
    unittest.main()