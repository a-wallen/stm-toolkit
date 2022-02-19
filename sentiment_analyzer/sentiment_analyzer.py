import sys, os
# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

# sentiment analysis with nltk: https://www.nltk.org/howto/sentiment.html
# sentiment word networks: https://www.nltk.org/howto/sentiwordnet.html
# parent link: https://www.nltk.org/howto.html
import nltk # for natural language processing

# Stock Ticker info from Alpaca: https://alpaca.markets/docs/api-references/market-data-api/stock-pricing-data/historical/
from alpaca import Alpaca # internal wrapper for getting stock info getting articles
from alpaca_news import news

from cosmos import Cosmos # internal wrapper class for persisting data
from sentiment import Sentiment # internal class for storing sentiment data

class SentimentAnalyzer():
    pass