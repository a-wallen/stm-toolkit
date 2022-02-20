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

def print_sentiment(sentiment: Sentiment) -> None:
    """Prints article sentiment analysis report"""

    print(
        f'Pos: {sentiment.positive} ',
        f'Neu: {sentiment.neutral} ',
        f'Neg: {sentiment.negative} ',
        f'Comp: {sentiment.compound} '
    )

def main() -> str: #documents: func.DocumentList

    # if documents:
    #     logging.info('Document id: %s', documents[0]['id'])

    # Access database
    instance = Cosmos()

    # Read articles from database
    articles = instance.read(AlpacaNews)

    # Write article sentiment analysis reports to database
    sa = SentimentAnalyzer()
    for article in articles:
        sentiment = sa.analyze(article)
        instance.write([sentiment])
        print_sentiment(sentiment)


if __name__ == "__main__":
    main()