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
from alpaca import Alpaca
from delta import Delta

def print_sentiment(sentiment: Sentiment) -> None:
    """Prints article sentiment analysis report"""

    print(
        f'Pos: {sentiment.positive} ',
        f'Neu: {sentiment.neutral} ',
        f'Neg: {sentiment.negative} ',
        f'Comp: {sentiment.compound} '
    )

def main(documents: func.DocumentList) -> str:

    if documents:
        logging.info('Document id: %s', documents[0]['id'])

    # Access database
    cosmos = Cosmos()
    alpaca = Alpaca()

    # Read articles from database
    articles = cosmos.read(AlpacaNews)

    # Write article sentiment analysis reports to database
    sa = SentimentAnalyzer()
    for article in articles:
        sentiment = sa.analyze(article)
        cosmos.write([sentiment])
        print_sentiment(sentiment)

    for article in articles:
        delta: Delta = alpaca.getDelta(article.tickers, article.created_at)
        print(delta.__dict__)
        cosmos.write([delta])


if __name__ == "__main__":
    cosmos = Cosmos()
    alpaca = Alpaca()

    articles = cosmos.read(AlpacaNews)

    sa = SentimentAnalyzer()
    for article in articles:
        sentiment = sa.analyze(article)
        cosmos.write([sentiment])
        print_sentiment(sentiment)

    for article in articles:
        delta = alpaca.getDelta(article.tickers, article.created_at)
        print(delta.__dict__)
        cosmos.write([delta])