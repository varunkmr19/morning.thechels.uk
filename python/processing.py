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
import datefinder
from datetime import datetime
from urllib.parse import urlparse

# setup
root = pathlib.Path(__file__).parent.parent.resolve()
url_list = [
      "http://daringfireball.net/index.xml",
      "http://feeds.feedburner.com/macstoriesnet",
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
     # "http://usesthis.com/feed/",
     # "https://wonkhe.com/blogs/feed/"
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

    entries_data = []
    for entry in entries:
        published_dt = list(datefinder.find_dates(entry['published']))

        if len(published_dt) == 0:
            published_str_dt = ""
        else:
            # E.g. Mon, 14 Sep 2020 21:38:24 
            published_str_dt = published_dt.strftime("%a, %d %b %Y %H:%M:%S")
            
        entries_data.append({
            "domain": get_hostname(entry["link"].split("#")[0]),
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published_str_dt": published_str_dt,
        })

    return entries_data

# Get url parse
def get_hostname(url):
    domain = urlparse(url).hostname
    return domain


# processing
if __name__ == "__main__":
    all_news = "<h2>News</h2>\n"
    index_page = root / "index.html"
    index_contents = index_page.open().read()

    for url in url_list:
        entries = fetch_blog_entries(url)[:1]
        domain = get_hostname(url)
        data_item_text = "\n\n".join(["<p><a href='{url}' target='new'>{title}</a><br/><small>{domain} | Published: {published}</small></p>\n"
                                    .format(**entry) for entry in entries])
        all_news += data_item_text
    final_output = replace_chunk(index_contents, "content_marker", all_news)
    index_page.open("w").write(final_output)

# get array from Json
# foreach url in Json get feed
# get last item from eat feed and add them into the html
# get weather
# provide some links