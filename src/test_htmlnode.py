import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "container", [], {"class": "container"})
        node2 = HTMLNode("div", "container", [], {"class": "container"})
        self.assertEqual(node, node2)

    def test_not_equal(self):
        node = HTMLNode("div", "containeroo", [], {"class": "container"})
        node2 = HTMLNode("div", "container", [], {"class": "container"})
        self.assertNotEqual(node, node2)

    def test_tag_not_equal(self):
        node = HTMLNode("div", "container", [], {"class": "container"})
        node2 = HTMLNode("span", "container", [], {"class": "container"})
        self.assertNotEqual(node, node2)

    def test_attrs_not_equal(self):
        node = HTMLNode("div", "container", [], {"class": "container"})
        node2 = HTMLNode("div", "container", [], {"id": "main"})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("div", "container", [], {"class": "container"})
        self.assertEqual(
            "HTMLNode(tag=div, value=container, children=[], props={'class': 'container'})",
            repr(node)
        )

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html(self):
        node = LeafNode("div", "container", {"class": "container"})
        self.assertEqual(
            '<div class="container">container</div>',
            node.to_html()
        )

    def test_to_html_no_value(self):
        node = LeafNode("div", None, {"class": "container"})
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        child1 = LeafNode("p", "Hello, world!")
        child2 = LeafNode("p", "This is a test.")
        parent = ParentNode("div", [child1, child2], {"class": "container"})
        self.assertEqual(
            '<div class="container"><p>Hello, world!</p><p>This is a test.</p></div>',
            parent.to_html()
        )

    def test_parent_to_html_no_tag(self):
        child1 = LeafNode("p", "Hello, world!")
        parent = ParentNode(None, [child1], {"class": "container"})
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_to_html_no_children(self):
        parent = ParentNode("div", None, {"class": "container"})
        with self.assertRaises(ValueError):
            parent.to_html()

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

if __name__ == "__main__":
    unittest.main()