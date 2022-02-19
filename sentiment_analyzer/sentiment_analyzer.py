import sys, os, re
# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))

# sentiment analysis with nltk: https://www.nltk.org/howto/sentiment.html
# sentiment word networks: https://www.nltk.org/howto/sentiwordnet.html
# parent link: https://www.nltk.org/howto.html
import nltk # for natural language processing
from nltk import tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity, stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentAnalyzer as Sentilyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *


# Stock Ticker info from Alpaca: https://alpaca.markets/docs/api-references/market-data-api/stock-pricing-data/historical/
from alpaca import Alpaca # internal wrapper for getting stock info getting articles
from alpaca_news import AlpacaNews as News

from cosmos import Cosmos # internal wrapper class for persisting data
from sentiment import Sentiment # internal class for storing sentiment data

class SentimentAnalyzer():

    def __init__(self) -> None:
        pass

    # def _train(self) -> None:
    #     # Retrieve subjective and objective documents, tokenize list
    #     n_instances = 100
    #     subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
    #     obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
    #     print(len(subj_docs), len(obj_docs))
    #     print(obj_docs[0])

    #     # Split subjective and objective instances to training and testing docs
    #     train_subj_docs = subj_docs[:80]
    #     test_subj_docs = subj_docs[80:100]
    #     train_obj_docs = obj_docs[:80]
    #     test_obj_docs = obj_docs[80:100]
    #     training_docs = train_subj_docs + train_obj_docs
    #     testing_docs = test_subj_docs + test_obj_docs

    #     # Handle negations with unigram word features
    #     sentilyzer = Sentilyzer()
    #     all_words_neg = sentilyzer.all_words([mark_negation(doc) for doc in training_docs]) 
    #     unigram_feats = sentilyzer.unigram_word_feats(all_words_neg, min_freq=4)
    #     print(len(unigram_feats))
    #     sentilyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

    #     # Apply features to obtain a feature-value representation of datasets
    #     training_set = sentilyzer.apply_features(training_docs)
    #     test_set = sentilyzer.apply_features(testing_docs)

    #     # Train classifyer on training set
    #     trainer = NaiveBayesClassifier.train
    #     classifier = sentilyzer.train(trainer, training_set)
    #     for key,value in sorted(sentilyzer.evaluate(test_set).items()):
    #         print('{0}: {1}'.format(key, value))

    def _filter_gen(self, article_text: str) -> str:
        stop_words = set(stopwords.words('english'))
        article_text = re.sub(r'[^\w\s]', '', article_text)
        words = word_tokenize(article_text)
        for word in words:
            if word not in stop_words:
                yield word

    def analyze(self, article : News) -> Sentiment:

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
            #article.source
        ]

        # Filter string of all concatenated data
        article_text = ''.join('%s ' % ''.join(map(str, attribute)) for attribute in article_data).lower()
        article_text_filtered = ''.join('%s ' % ' '.join(word for word in self._filter_gen(article_text)))
        
        # Create polarity scores as a dictionary
        # EX: {compound: -0.5859, neg: 0.23, neu: 0.697, pos: 0.074}
        sia = SentimentIntensityAnalyzer()
        sentiment_score = sia.polarity_scores(article_text_filtered)

        # Create sentiment sentiment
        return Sentiment(
            article,    
            sentiment_score['pos'], 
            sentiment_score['neu'], 
            sentiment_score['neg'],
            sentiment_score['compound']
        )

    def __del__(self) -> None:
        pass

def test() -> None:
    article = News(
        24803233,
        "Benzinga's Top 5 Articles For 2021 — Or 'Who Let The Dog Out?'",
        "Sue Strachan",
        "2021-12-29T15:11:03Z",
        "2021-12-30T20:37:41Z",
        "2021 may have been the Year of the Ox in the Chinese calendar, but for Benzinga, it was the Year of the Dog, or should we say, Year of the Dogecoin (CRYPTO: DOGE).",
        "<p>2021 may have been the Year of the Ox in the Chinese calendar, but for Benzinga, it was the Year of the Dog, or should we say, Year of the <strong>Dogecoin</strong> (CRYPTO: <a class=\"ticker\" href=\"https://www.benzinga.com/quote/doge/usd\">DOGE</a>).</p>\r\n\r\n<p>The memecoin created in 2013....",
        [
            {
                "size": "large",
                "url": "https://cdn.benzinga.com/files/imagecache/2048x1536xUP/images/story/2012/doge_12.jpg"
            },
            {
                "size": "small",
                "url": "https://cdn.benzinga.com/files/imagecache/1024x768xUP/images/story/2012/doge_12.jpg"
            },
            {
                "size": "thumb",
                "url": "https://cdn.benzinga.com/files/imagecache/250x187xUP/images/story/2012/doge_12.jpg"
            }
        ],
        [
            "AMZN",
            "BTCUSD",
            "COIN",
            "DOGEUSD",
            "SPCE",
            "TSLA",
            "TWTR"
        ],
        "benzinga"
    )

    sa = SentimentAnalyzer()
    sentiment = sa.analyze(article)
    print(
        f'Pos: {sentiment.positive}, ' +
        f'Neut: {sentiment.neutral}, ' +
        f'Neg: {sentiment.negative}, ' +
        f'Compound: {sentiment.compound}'
    )

if __name__ == "__main__":
    test()