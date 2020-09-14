"""
Processor
"""
import re
import pathlib
import feedparser

root = pathlib.Path(__file__).parent.parent.resolve()

def replace_chunk(content, marker, chunk):
    """ Swap out placeholders """
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

def fetch_blog_entries():
    """Get blog posts from RSS"""
    entries = feedparser.parse("https://thechels.uk/feed.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]

if __name__ == "__main__":
    index_file = root / "index.html"
    index_file_contents = index_file.open().read()
    entries = fetch_blog_entries()[:5]
    INDEX_CONTENT = "\n".join(
        ["<h2 class='element'>{title}</h2><p><a href='{url}'>Published: {published}</a></p>".format(**entry) for entry in entries]
    )

    rewritten = replace_chunk(index_file_contents, "posts", INDEX_CONTENT)
    index_file.open("w").write(rewritten)