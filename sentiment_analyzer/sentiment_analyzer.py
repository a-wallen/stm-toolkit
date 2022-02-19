import sys, os

# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))

# sentiment analysis with nltk: https://www.nltk.org/howto/sentiment.html
# sentiment word networks: https://www.nltk.org/howto/sentiwordnet.html
# parent link: https://www.nltk.org/howto.html
import nltk # for natural language processing
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer as Sentilyzer
from nltk.sentiment.util import *

# Stock Ticker info from Alpaca: https://alpaca.markets/docs/api-references/market-data-api/stock-pricing-data/historical/
from alpaca import Alpaca # internal wrapper for getting stock info getting articles
from alpaca_news import AlpacaNews as News

from cosmos import Cosmos # internal wrapper class for persisting data
from sentiment import Sentiment # internal class for storing sentiment data

class SentimentAnalyzer():

    def __init__(self) -> None:
        pass

    def analyze(self) -> None:

        # Sentiment data to analyze
        # headline = article.headline
        # summary = article.summary
        # content = article.content
        # symbols = article.symbols

        pass

    def __del__(self) -> None:
        pass

def test() -> None:
    sa = SentimentAnalyzer()
    sa.analyze()

if __name__ == "__main__":
    test()