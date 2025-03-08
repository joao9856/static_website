import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter

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


class TestTextNodeToHTMLNode(unittest.TestCase):

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


class TestTextNodeSplitter(unittest.TestCase):

    def test_node_spliter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)  
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])     

    def test_node_spliter_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)  
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("bold block", TextType.BOLD), TextNode(" word", TextType.TEXT)]) 

    def test_node_spliter_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)  
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("italic block", TextType.ITALIC), TextNode(" word", TextType.TEXT)])    

    def test_node_spliter_invalid_delimiter(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([TextNode("This is text with a _italic block_ word", TextType.TEXT)], "*", TextType.BOLD)    

    def test_node_spliter_code_no_split(self):
        node = TextNode("This is code block", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)  
        self.assertEqual(new_nodes, [TextNode("This is code block", TextType.CODE)])

    def test_node_spliter_italic_plus_no_split(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        node1 = TextNode("This is italic block", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node, node1], "_", TextType.ITALIC)  
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("italic block", TextType.ITALIC), TextNode(" word", TextType.TEXT), TextNode("This is italic block", TextType.ITALIC)])

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD)
            ],
            new_nodes
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD)
            ],
            new_nodes
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC)
            ],
            new_nodes
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes
        )

if __name__ == "__main__":
    unittest.main()