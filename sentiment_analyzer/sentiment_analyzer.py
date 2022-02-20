import re
import sys, os

# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))

# sentiment analysis with nltk: https://www.nltk.org/howto/sentiment.html
# sentiment word networks: https://www.nltk.org/howto/sentiwordnet.html
# parent link: https://www.nltk.org/howto.html
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentAnalyzer as Sentilyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *

# Stock Ticker info from Alpaca: https://alpaca.markets/docs/api-references/market-data-api/stock-pricing-data/historical/
from alpaca_news import AlpacaNews as News
from sentiment import Sentiment # internal class for storing sentiment data
from datetime import datetime

class SentimentAnalyzer():
    """Sentiment Analyzer for Alpaca News articles"""

    def __init__(self) -> None:
        pass

    def _filter_gen(self, article_text: str) -> str:
        """Filters article text to contain relevant words
        
        Eliminates unnecessary symbols and NLTK stopwords.

        :param article_text: Article text
        :return: Yields relevant filtered words 
        """

        stop_words = set(stopwords.words('english'))
        article_text = re.sub(r'[^\w\s]', ' ', article_text)
        words = word_tokenize(article_text)
        for word in words:
            if word not in stop_words:
                yield word

    def analyze(self, article : News) -> Sentiment:
        """Generates a sentiment analysis report  for an article
        
        :param article: Alpaca News article
        :return: Sentiment analysis score
        """

        # Article data to analyze
        article_data = [  
            article.headline,
            article.author,
            #article.created_at,
            #article.updated_at,
            article.summary,
            article.content,
            #article.images,
            article.symbols,
            article.source
        ]

        # Filter string of all concatenated data
        article_text = ''.join('%s ' % ''.join(map(str, attribute)) for attribute in article_data).lower()
        article_text_filtered = ''.join('%s ' % ' '.join(word for word in self._filter_gen(article_text)))
        
        # Create polarity scores as a dictionary
        # EX: {compound: -0.5859, neg: 0.23, neu: 0.697, pos: 0.074}
        sentimental_intense_anal = SentimentIntensityAnalyzer()
        sentiment_score = sentimental_intense_anal.polarity_scores(article_text_filtered)

        # Create sentiment sentiment
        return Sentiment(
            symbols=article.symbols,
            source=article.source,
            date=str(datetime.now()),
            positive=sentiment_score['pos'], 
            neutral=sentiment_score['neu'], 
            negative=sentiment_score['neg'],
            compound=sentiment_score['compound']
        )

    def __del__(self) -> None:
        pass
