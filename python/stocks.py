# import
import os
import re
import random
import pathlib
from yahoo_fin import stock_info as si

root = pathlib.Path(__file__).parent.parent.resolve()

# Methods
def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

def get_stocks(set_of_tickers):
    string_builder = "<h2>Stocks</h2>\n<ul>\n"
    for ticker in list(set_of_tickers):
        string_builder += f"<li>{ticker} : {si.get_live_price(ticker)}</li>\n"
    return string_builder

# Processing
set_of_tickers = ['AAPL','AMZN','MSFT','IUSA.L','IWDG.L','VWRL.L','UKDV.L','UDVD.L']
string_output = get_stocks(set_of_tickers)
print(string_output)

# output
if __name__ == "__main__":
    index_page = root / "index.html"
    index_contents = index_page.open().read()
    final_output = replace_chunk(index_contents, "stocks_marker", string_output + "</ul>")
    index_page.open("w").write(final_output)