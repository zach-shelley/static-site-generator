from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
import unittest

class TestHTMLNode(unittest.TestCase):
    # first tests

    # def test_eq(self):
    #     node1 = HTMLNode(tag="p", value="this is a test", props={"class" : "test"})
    #     node2 = HTMLNode(tag="p", value="this is a test", props={"class" : "test"})
    #     return self.assertEqual(node1, node2)
    
    # def test_func(self):
    #     node1 = HTMLNode(tag="p", value="this is a test", props={"class" : "test"})
    #     return self.assertEqual(node1.props_to_html(), ' class="test"')
        
    # def test_multiple_props(self):
    #     node = HTMLNode(tag="a", value="click", props={"href": "https://example.com", "target": "_blank"})
    #     self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

    # second tests

    # def test_leaf_to_html_p(self):
    #     node = LeafNode("p", "Hello, world!")
    #     self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # def test_leaf_to_html_h1_unequal(self):
    #     node = LeafNode("h1", "Greetings, king")
    #     self.assertNotEqual(node.to_html(), "<h1>Greeting, king</h1>")

    # third tests

    # def test_to_html_with_children(self):
    #     child_node = LeafNode("span", "child")
    #     parent_node = ParentNode("div", [child_node])
    #     self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    # def test_to_html_with_grandchildren(self):
    #     grandchild_node = LeafNode("b", "grandchild")
    #     child_node = ParentNode("span", [grandchild_node])
    #     parent_node = ParentNode("div", [child_node])
    #     self.assertEqual(
    #         parent_node.to_html(),
    #         "<div><span><b>grandchild</b></span></div>",
    #     )

    # def test_to_html_with_multiple_children(self):
    #     parent_node = ParentNode("ul", [
    #         LeafNode("li", "first"),
    #         LeafNode("li", "second"),
    #         LeafNode("li", "third"),
    #     ])
    #     self.assertEqual(parent_node.to_html(), "<ul><li>first</li><li>second</li><li>third</li></ul>")

    # 4th Tests

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()

