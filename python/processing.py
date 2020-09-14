 # importing modules
"""
Build and Process
"""
import os
import re
import random
import pathlib
import json
import requests
import feedparser

# setup
root = pathlib.Path(__file__).parent.parent.resolve()
url_list = [
    "http://daringfireball.net/index.xml",
    "http://feeds.feedburner.com/macstoriesnet",
    "http://thechels.uk/feed/",
    "http://xkcd.com/rss.xml",
    "https://www.cloudflarestatus.com/history.rss",
    "http://blog.agilebits.com/feed/",
    "https://status.dropbox.com/history.rss",
    "http://feeds.feedburner.com/Garmin",
    "http://status.ifttt.com/history.rss",
    "http://blog.mailgun.net/rss",
    "http://blog.strava.com/feed/atom/",
    "http://blog.supertop.co/rss",
    "https://blog.dropbox.com/feed/",
    "https://medium.com/feed/strava-engineering",
    "http://www.politics.co.uk/rss.xml",
    "https://sixcolors.com/feed.json",
    "http://feeds.feedburner.com/ReflectivePerspective",
    "http://the5krunner.com/feed/",
    "https://www.troyhunt.com/rss/",
    "http://usesthis.com/feed/",
    "http://www.wonkhe.com/feed/"

]

# Replacer function
def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

# Get Entries Function
def fetch_blog_entries(working_url):
    entries = feedparser.parse(working_url)["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]

# processing
if __name__ == "__main__":
    index_page = root / "index.html"
    index_contents = index_page.open().read()
    for url in url_list:
        print(url)
        entries = fetch_blog_entries(url)[:1]
        data_item_text = "\n".join(["<p>{title}</p><p><small><a href='{url}'>Published: {published}</a></small></p>".format(**entry) for entry in entries])
        index_contents = replace_chunk(index_contents, "content_marker", data_item_text)
        keep += index_contents
    index_page.open("w").write(keep)

# get array from Json
# foreach url in Json get feed
# get last item from eat feed and add them into the html

# get weather
# provide some links