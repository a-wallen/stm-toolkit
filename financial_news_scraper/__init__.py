import sys
import os
import datetime
import logging
import azure.functions as func


# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'models'))
from typing import List
from news import News
from alpaca import Alpaca
from alpaca_ticker import AlpacaTicker
from cosmos import Cosmos

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    alpaca = Alpaca()
    cosmos = Cosmos()

    ticker: AlpacaTicker = alpaca.getTickerInfo("TSLA")
    cosmos.write([ticker])

    news = news.News()
    newsList = news.getNewsArticles()
    cosmos.write(newsList)

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)


if __name__ == "__main__":
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    alpaca = Alpaca()
    news = News()
    cosmos = Cosmos()

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
    
    newsList = news.getNewsArticles(watchList)
    cosmos.write(newsList)

    for symbol in watchList:
        try:
            ticker: AlpacaTicker = alpaca.getTickerInfo(symbol=symbol)
            cosmos.write([ticker])
        except:
            pass

