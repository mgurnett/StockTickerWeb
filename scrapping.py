import sys
import requests
from bs4 import BeautifulSoup as bs

def get_stock_full_name (symbol):
#     URL = "https://www.google.com/search?q="+symbol+"&tbm=fin"
#     URL = "https://www.google.com/search?q={}&tbm=fin".format(symbol,38)
    URL = "https://ca.finance.yahoo.com/quote/{}?p=".format(symbol)
#     print (URL)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    page = requests.get(URL, headers=headers)
#     print (page)
    soup = bs(page.content, "html.parser")
#     print (soup.prettify())
    try:
#         name=soup.find ('span', attrs = {'class':"mfMhoc"})
        name=soup.find ('h1', attrs = {'class':"D(ib) Fz(18px)"}).text
        large_name = name[:name.index(" (")]

#         print (name)
    except Exception as e:
        print (' the exception from Sprapping is: {}'.format(e))
        large_name = ""
    return large_name

# symbol = "aapl"
# name  = get_stock_full_name(symbol)

COMMON = [("aapl", "Apple Inc"),
          ("ac", "Air Canada"),
          ("amzn", "Amazon.com, Inc."),
          ("ba", "Boeing Co"),
          ("ccl", "Carnival Corp"),
          ("coke", "Coca-Cola Consolidated Inc"),
          ("f", "Ford"),
          ("fb", "Facebook, Inc. Common Stock"),
          ("goog", "Alphabet Inc Class C"),
          ("gme", "Gamestop"),
          ("mar", "Marriott International"),
          ("msft", "Microsoft"),
          ("nflx", "Netflix Inc"),
          ("su", "Suncor Energy Inc."),
          ("tsla", "Tesla Inc"),
          ("zm", "Zoom Video Com")]

for c in COMMON:
    symbol = c[0]
    name  = get_stock_full_name(symbol)
    print (name)
