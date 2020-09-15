import os
import re
import pathlib
import json
import requests
from datetime import date

# setup
root = pathlib.Path(__file__).parent.parent.resolve()
city = "Cheltenham"
country_code = "UK"
location = city+','+country_code
APIKEY = os.getenv('open_weather_key')
url = "http://api.openweathermap.org/data/2.5/find?q=%s&units=metric&APPID=%s" %(location,APIKEY)
# headers = {"Authorization":"Bearer %s"%key}

response = requests.get(url)
response_dict = json.loads(response.text)

my_loc = response_dict['list'][0]
string_today = "Today's date is "+ date.today()
string_weather = "The average temperature today is", str(my_loc['main']['temp'])+"˚C."\
      , "You should expect", str(my_loc['weather'][0]['description'])+".")

# Replacer function
def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

# processing
if __name__ == "__main__":
    index_page = root / "index.html"
    index_contents = index_page.open().read()
    final_output = replace_chunk(index_contents, "day_marker", string_today)
    final_output = replace_chunk(final_output, "weather_marker", string_weather)
    index_page.open("w").write(final_output)
