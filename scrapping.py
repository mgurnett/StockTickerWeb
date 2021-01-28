import sys
import requests
from bs4 import BeautifulSoup as bs

def get_stock_full_name (symbol):
    URL = "https://www.google.com/search?q="+symbol+"&tbm=fin"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    page = requests.get(URL, headers=headers)
    # print (page)
    soup = bs(page.content, "html.parser")
    try:
        name=soup.find ('span', attrs = {'class':"mfMhoc"}).text
    except:
        name = ""
    return name

symbol = "tsla"
name  = get_stock_full_name(symbol)
print (name)
# <span role="heading" aria-level="2" class="mfMhoc">Alphabet Inc Class C</span>



#https://www.google.com/search?q="INDEXTSI: OSPTX"&tbm=fin