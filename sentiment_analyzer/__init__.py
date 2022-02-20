import sys, os
# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))

# https://www.nltk.org/howto/sentiment.html
import logging
import azure.functions as func
from cosmos import Cosmos # internal wrapper class for persisting data
from sentiment import Sentiment # internal class for storing sentiment data
from sentiment_analyzer import SentimentAnalyzer
from alpaca_news import AlpacaNews

def main(documents: func.DocumentList) -> None:

    # Access database
    _database = Cosmos()
    _database._cosmosCreateInstance()

    # Read articles from database
    articles = _database.read(AlpacaNews)

    # Write article sentiment analysis reports to database
    sa = SentimentAnalyzer()
    for article in articles:
        sentiment = sa.analyze(article)
        _database.write([sentiment])
