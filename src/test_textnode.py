import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK, "")
        self.assertNotEqual(node, node2)

    def test_eq_3(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.bold.com")
        self.assertNotEqual(node, node2)

    def test_eq_4(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_5(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_6(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.bold.com")
        self.assertNotEqual(node, node2)

    def test_eq_7(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.bold.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.bold.com")
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.youtube.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.youtube.com", "alt": "This is a text node"}) 

    def test_invalid_text_type(self):
        with self.assertRaises(Exception):
            text_node_to_html_node(TextNode("This is a text node", TextType.BANANA, "https://www.youtube.com"))  

    def test_no_url_on_link_type(self):
        with self.assertRaises(ValueError):
            text_node_to_html_node(TextNode("This is a text node", TextType.LINK))  

if __name__ == "__main__":
    unittest.main()