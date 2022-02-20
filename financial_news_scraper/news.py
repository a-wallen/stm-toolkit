from itertools import count
import os
import uuid
import sys
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))

from typing import List
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# CONVERT TO ALPACA_NEWS object if article is not from Alpaca

# https://newspaper.readthedocs.io/en/latest/
from newspaper import Article # summarize articles with url 
import requests

# CONVERT TO ALPACA_NEWS object if article is not from Alpaca

from alpaca import Alpaca # internal wrapper for Alpaca API
# https://alpaca.markets/docs/api-references/market-data-api/news-data/historical/
from alpaca_news import AlpacaNews # News as defined by the Alpaca API
# https://alpaca.markets/docs/api-references/market-data-api/stock-pricing-data/historical/

class News():
    def __init__(self):
        self.alpaca = Alpaca()

    def getNewsArticles(self, symbols: List[str]) -> List[AlpacaNews]:
        local_time = datetime.utcnow()
        # local_time = local_time.strftime("%Y-%m-%eT%H:%M:%SZ")
        
        list = []
        for i in range(5):
            td = timedelta(i*3)
            # print((local_time-td).strftime("%Y-%m-%eT%H:%M:%SZ"))
            list += self.alpaca.getNews(
                symbols=symbols,
                end=(local_time-td).strftime("%Y-%m-%dT%H:%M:%SZ")
            )
        # td = timedelta(31)
        # print((local_time-td).strftime("%Y-%m-%dT%H:%M:%SZ"))
        # list+= self.alpaca.getNews(end=(local_time-td).strftime("%Y-%m-%dT%H:%M:%SZ"))
        
        return list

    def getNewsUsingNewspaper(self) -> List[AlpacaNews]:
        url = "https://www.cnbc.com/business/"

        response = requests.get(url, allow_redirects=True, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')

        soupTitle = soup.findAll("div", {"class":"Card-standardBreakerCard Card-threeUpStackRectangleSquareMedia Card-rectangleToLeftSquareMedia Card-card"}, recursive=True)
        
        list = []

        for item in soupTitle:
            m = item.find("a")
            if m :
                list.append(Article(m['href']))

        finalList = []

        for article in list:
            article.download()
            article.parse()
            finalList.append(AlpacaNews(id=uuid.uuid4(), headline=article.title, author=article.authors, created_at=article.publish_date, updated_at=article.publish_date, summary=article.summary, content=article.text, symbols=article.keywords, source=article.source_url))
            
        return finalList

if __name__ == "__main__":
    n = News()
    watchList: List[str] = [
        "TSLA",
        "MSFT",
        "GOOG",
        "AAPL",
        "YHOO",
        "SNE",
        "RIVN",
        "SMG",
    ]
    list = n.getNewsArticles(watchList)

    