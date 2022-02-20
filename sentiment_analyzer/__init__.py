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

def main() -> None: # documents: func.DocumentList
    _database = Cosmos()
    _database._cosmosCreateInstance()
    articles = _database.read(AlpacaNews)

    sa = SentimentAnalyzer()
    for article in articles:
        sentiment = sa.analyze(article)
        _database.write([sentiment])

        print(
            f'Pos: {sentiment.positive}, ' +
            f'Neut: {sentiment.neutral}, ' +
            f'Neg: {sentiment.negative}, ' +
            f'Compound: {sentiment.compound}'
        )

if __name__ == '__main__':
    main()