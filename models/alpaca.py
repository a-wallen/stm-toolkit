from ast import Del
from email.mime import image
import os
from symtable import Symbol
import sys
import json
import base64
from datetime import datetime, timedelta
import alpaca_trade_api as tradeapi
from typing import Dict, List
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from alpaca_quote import AlpacaQuote
from alpaca_ticker import AlpacaTicker
from alpaca_news import AlpacaNews
from alpaca_image import AlpacaImage
from delta import Delta
from dateutil import parser

from alpaca_trade_api.rest import TimeFrame, URL, TimeFrameUnit
from alpaca_trade_api.rest_async import gather_with_concurrency, AsyncRest
import alpaca_trade_api as tradeapi
from alpaca_trade_api.common import URL, get_credentials, get_data_url


class Alpaca():
    def __init__(self):
        self.api = self._createTradeApi()

    # https://alpaca.markets/docs/api-references/market-data-api/stock-pricing-data/historical/
    def _createTradeApi(self) -> tradeapi.REST:
        """[PRIVATE] Create instance of trade api from os.environment variables

        Returns:
            tradeapi.REST: Instance of Alpaca RESTful API 
        """
        load_dotenv()
        encrypted_creds: str = os.environ["ALPACA_CREDS"]
        decoded: bytes = base64.b64decode(encrypted_creds)
        json_dict = json.loads(decoded)
        return tradeapi.REST(
            key_id=json_dict["api_key_id"],
            secret_key=json_dict["secret_key"],
        )

    # https://alpaca.markets/docs/api-references/market-data-api/stock-pricing-data/historical/
    def getTickerInfo(
        self,
        symbol: str,
        start: datetime = None,
        end: datetime = None,
        limit: int = None,
    ) -> AlpacaTicker:
        """Get the ticker information for a given stock.

        Args:
            symbol (str): The symbol to query for
            start (datetime): Filter data equal to or after this time in RFC-3339 format. Fractions of a second are not accepted
            end (datetime): Filter data equal to or before this time in RFC-3339 format. Fractions of a second are not accepted
            limit (int): Number of data points to return. Must be in range 1-10000, defaults to 1000

        Returns:
            List[AlpacaTicker]: _description_
        """
        trade = self.api.get_latest_trade(symbol)
        return AlpacaTicker(
            t=str(trade.t),
            x=trade.x,
            p=trade.p,
            s=trade.s,
            c=trade.c,
            i=trade.i,
            z=trade.z,
        )

    def getDelta(self, symbol: str, day: str) -> Delta:
        """Get the latest quote for a given stock

        Args:
            symbol (str): The symbol of the stock to query for

        Returns:
            List[AlpacaQuote]: _description_
        """
        now: datetime = datetime.now()
        date: datetime = parser.parse(day)
        if date.day == now.day and date.month == now.month and date.year == now.year:
            date -= timedelta(minutes=15)

        bars = self.api.get_bars(symbol, TimeFrame.Day, str(date), str(date), adjustment='raw')
        opening: float = float(bars[0].o)
        closing: float = float(bars[-1].c)
        delta: float = closing / opening
        return Delta(
            symbol=symbol,
            open=str(opening),
            close=str(closing),
            delta=str(delta),
            date=day,
        )

    # https://alpaca.markets/docs/api-references/market-data-api/news-data/historical/
    def getNews(
        self,
        symbols: str = None,
        start: datetime = None,
        end: datetime = None,
        limit: int = 10,
        sort: str = None,
        include_content: bool = True,
        exclude_contentless: bool = False,
        page_token: str = None
    ) -> List[AlpacaNews]:
        """Returns latest news articles across stocks and crypto. By default returns latest 10 news articles.

        Args:
            symbols (str, optional): List of symbols to obtain news. Defaults to None.
            start (datetime, optional): (Default: 01-01-2015) Start date to obtain news. Defaults to None.
            end (datetime, optional): (Default: now) End date to obtain news. Defaults to None.
            limit (int, optional): (Default: 10, Max: 50) Limit of news items to be returned for given page. Defaults to None.
            sort (str, optional): (Default: DESC) Sort articles by updated date. Options: DESC, ASC. Defaults to None.
            include_content (bool, optional): (Default: false) Boolean whether to include content for news articles. Defaults to None.
            exclude_contentless (bool, optional): (Default: false) Exclude news articles that do not contain content (just headline and summary). Defaults to None.
            page_token (str, optional): Pagination token to continue to next page. Defaults to None.

        Returns:
            List[AlpacaNews]: Returns latest news articles across stocks and crypto. By default returns latest 10 news articles.
        """
        
        symbols = ['TSLA']  

        list = self.api._data_get('', symbols, api_version='v1beta1', endpoint_base='news', start=start, end=end, limit=50, sort="DESC",
                                  include_content=True,
                                  exclude_contentless=exclude_contentless,
                                  resp_grouped_by_symbol=False,)

        finalList = []

        for i in iter(list):
            if "content" in i:
                a = AlpacaNews(id=str(i["id"]), headline=i["headline"], author=i["author"], created_at=i["created_at"], updated_at=i["updated_at"],
                           summary=i["summary"], content=BeautifulSoup(i["content"], "lxml").text,
                                symbols=i["symbols"], source=i["source"])
            finalList.append(a)

        return finalList



if __name__ == "__main__":
    import doctest
    doctest.testmod()
    