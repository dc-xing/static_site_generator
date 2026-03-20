import re


def extract_markdown_images(text):

    # Regular expression to match markdown image syntax ![alt text](image_url)
    image_pattern = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    return re.findall(image_pattern, text)

def extract_markdown_links(text):

    # Regular expression to match markdown link syntax [link text](url)
    link_pattern = r'(?<!!)\[([^\[\]]*)]\(([^\(\)]*)\)'
    return re.findall(link_pattern, text)

def extract_title(markdown):
    lines = markdown.split("\n")   
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found in markdown")