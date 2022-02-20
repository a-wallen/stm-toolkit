import sys, os
# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

# https://www.nltk.org/howto/sentiment.html
import logging
import azure.functions as func
from cosmos import Cosmos # internal wrapper class for persisting data
from sentiment import Sentiment # internal class for storing sentiment data
from sentiment_analyzer import SentimentAnalyzer

def main(documents: func.DocumentList) -> str:
    if documents:
        logging.info('Document id: %s', documents[0]['id'])
        
        # Convert func.Docs to articles
        for doc in documents:
            
            article = doc.to_json()

            # Create sentiment report
            sa = SentimentAnalyzer()
            sentiment = sa.analyze(article)

            # Write to db