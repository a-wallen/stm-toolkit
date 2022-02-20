import json
import os
from random import randint
import sys
from time import sleep

from aiohttp import request
from bs4 import BeautifulSoup
# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))


from typing import Dict, List
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import bs4 # any scraping outside of bs4 and newspaper3k
# CONVERT TO ALPACA_NEWS object if article is not from Alpaca

# https://newspaper.readthedocs.io/en/latest/
from newspaper import Article # summarize articles with url 
import newspaper
from newspaper import Source
import requests

# CONVERT TO ALPACA_NEWS object if article is not from Alpaca

from alpaca import Alpaca # internal wrapper for Alpaca API
# https://alpaca.markets/docs/api-references/market-data-api/news-data/historical/
from alpaca_news import AlpacaNews # News as defined by the Alpaca API
from alpaca_image import AlpacaImage # Images as defined by the Alpaca API
# https://alpaca.markets/docs/api-references/market-data-api/stock-pricing-data/historical/
from alpaca_ticker import AlpacaTicker # ticker information from Alpaca API

class News():
    def __init__(self):
        self.alpaca = Alpaca()

    def getNewsArticles(self) -> List[AlpacaNews]:
        list = self.alpaca.getNews()
        return list

    def getNewsUsingNewspaper(self) -> List[AlpacaNews]:
        url = "https://finance.yahoo.com"

       
    

        yahooPaper= Source(url = url)
        yahooPaper.build()
        for i in yahooPaper.articles:
            i.download()
            i.parse()
            print(i.title)
            sleep(randint(1, 5))


        

        

        

        
        



if __name__ == "__main__":
    n = News()
    # list = n.getNewsArticles()
    # print([str(i) for i in list])
    n.getNewsUsingNewspaper()
    