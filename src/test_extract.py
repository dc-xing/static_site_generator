import unittest

from extract import extract_markdown_images, extract_markdown_links, extract_title


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        markdown_text = "Here is an image: ![alt text](http://example.com/image.jpg)"
        expected_images = [("alt text", "http://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(markdown_text), expected_images)

    def test_extract_markdown_images_multiple(self):
        markdown_text = "Image 1: ![alt text](http://example.com/image1.jpg) Image 2: ![alt text](http://example.com/image2.jpg)"
        expected_images = [("alt text", "http://example.com/image1.jpg"), ("alt text", "http://example.com/image2.jpg")]
        self.assertEqual(extract_markdown_images(markdown_text), expected_images)

    def test_extract_markdown_images_none(self):
        markdown_text = "This text has no images."
        expected_images = []
        self.assertEqual(extract_markdown_images(markdown_text), expected_images)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        markdown_text = "Here is a link: [link text](http://example.com)"
        expected_links = [("link text", "http://example.com")]
        self.assertEqual(extract_markdown_links(markdown_text), expected_links)

    def test_extract_markdown_links_multiple(self):
        markdown_text = "Link 1: [link text 1](http://example.com/link1) Link 2: [link text 2](http://example.com/link2)"
        expected_links = [("link text 1", "http://example.com/link1"), ("link text 2", "http://example.com/link2")]
        self.assertEqual(extract_markdown_links(markdown_text), expected_links)

    def test_extract_markdown_links_none(self):
        markdown_text = "This text has no links."
        expected_links = []
        self.assertEqual(extract_markdown_links(markdown_text), expected_links)

    def test_extract_markdown_links_excludes_images(self):
        markdown_text = "![image](http://example.com/image.jpg) and [link](http://example.dev)"
        expected_links = [("link", "http://example.dev")]
        self.assertEqual(extract_markdown_links(markdown_text), expected_links)

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown_text = "# This is a title\n\nThis is some content."
        expected_title = "This is a title"
        self.assertEqual(extract_title(markdown_text), expected_title)

    def test_extract_title_no_title(self):
        markdown_text = "This is some content without a title."
        with self.assertRaises(ValueError):
            extract_title(markdown_text)

    def test_extract_title_multiple_titles(self):
        markdown_text = "# Title 1\n\n# Title 2\n\nThis is some content."
        expected_title = "Title 1"
        self.assertEqual(extract_title(markdown_text), expected_title)