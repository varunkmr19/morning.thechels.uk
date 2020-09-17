
 # importing modules
import os
import re
import pathlib
import requests
import json
from datetime import date

# Methods
def ord(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

def dtStylish(dt,f):
    return dt.strftime(f).replace("{th}", ord(dt.day))

def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

def pprint(string):
    json_formatted_str = json.dumps(string, indent=2)
    print(json_formatted_str)

# setup
date = date.today()
root = pathlib.Path(__file__).parent.parent.resolve()
url = f"https://push.api.bbci.co.uk/b?t=%2Fdata%2Fbbc-morph-football-scores-match-list-data%2FendDate%2F{date}%2FstartDate%2F{date}%2FtodayDate%2F{date}%2Ftournament%2Ffull-priority-order%2Fversion%2F2.4.1?timeout=5"
response_dict = json.loads(requests.get(url).text)
tournament_slug = [ 'league-cup','champions-league','premier-league','fa-cup']
pre_content = "<ul>\n\n"

today_date_string = dtStylish(date.today(), '%A-{th}-%B')

for md_events in list(response_dict['payload'][0]['body']['matchData']):
    for tournaments in (t_item for t_item in md_events if md_events['tournamentMeta']['tournamentSlug'] in tournament_slug):
        for events in md_events['tournamentDatesWithEvents'][today_date_string]:
            for games in events['events']:
                pprint(games)
                home_name = games['homeTeam']['name']['first']
                away_name = games['awayTeam']['name']['first']
                kick_off = games['startTimeInUKHHMM']
                pre_content += f"<li>{home_name} - {away_name} ({kick_off})</li>\n\n"

print(pre_content)

# processing
if __name__ == "__main__":
    all_news = "<h2>Fixtures</h2>\n"
    index_page = root / "index.html"
    index_contents = index_page.open().read()
    final_output = replace_chunk(index_contents, "fixtures_marker", pre_content + "</ul>")
    index_page.open("w").write(final_output)
