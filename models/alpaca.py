from email.mime import image
import os
from symtable import Symbol
import sys
import json
import base64
from datetime import datetime
import alpaca_trade_api as tradeapi
from typing import Dict, List
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from alpaca_ticker import AlpacaTicker
from alpaca_news import AlpacaNews
from alpaca_image import AlpacaImage

from alpaca_trade_api.rest import TimeFrame, URL
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
        # print(json_dict["api_key_id"])
        # print(json_dict["secret_key"])
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

        # list = self.api.get_news(
        #     symbol=symbols, start=start, end=end, limit=limit, sort=sort, include_content=include_content, exclude_contentless=exclude_contentless)
        symbols = symbols or []  # TODO check if ano or many

        list = self.api._data_get('', symbols, api_version='v1beta1', endpoint_base='news', start=start, end=end, limit=limit, sort=sort,
                                  include_content=include_content,
                                  exclude_contentless=exclude_contentless,
                                  resp_grouped_by_symbol=False,)

        finalList = []

        for i in iter(list):

            a = AlpacaNews(id=i["id"], headline=i["headline"], author=i["author"], created_at=i["created_at"], updated_at=i["updated_at"],
                           summary=i["summary"], content=BeautifulSoup(i["content"], "lxml").text, images=[*map(lambda s: AlpacaImage(
                               size=s["size"], url=s["url"]), i["images"])], symbols=i["symbols"], source=i["source"])
            finalList.append(a)

        return finalList

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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    alpaca = Alpaca()
    ticker = alpaca.getTickerInfo("AAPL")
