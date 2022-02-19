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

        # Retrieve subjective and objective documents, tokenize list
        n_instances = 100
        subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
        obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
        print(len(subj_docs), len(obj_docs))
        print(obj_docs[0])

        # Split subjective and objective instances to training and testing docs
        train_subj_docs = subj_docs[:80]
        test_subj_docs = subj_docs[80:100]
        train_obj_docs = obj_docs[:80]
        test_obj_docs = obj_docs[80:100]
        training_docs = train_subj_docs + train_obj_docs
        testing_docs = test_subj_docs + test_obj_docs

        # Handle negations with unigram word features
        sentilyzer = Sentilyzer()
        all_words_neg = sentilyzer.all_words([mark_negation(doc) for doc in training_docs]) 
        unigram_feats = sentilyzer.unigram_word_feats(all_words_neg, min_freq=4)
        print(len(unigram_feats))
        sentilyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

        # Apply features to obtain a feature-value representation of datasets
        training_set = sentilyzer.apply_features(training_docs)
        test_set = sentilyzer.apply_features(testing_docs)

        # Train classifyer on training set
        trainer = NaiveBayesClassifier.train
        classifier = sentilyzer.train(trainer, training_set)
        for key,value in sorted(sentilyzer.evaluate(test_set).items()):
            print('{0}: {1}'.format(key, value))

    def __del__(self) -> None:
        pass

def test() -> None:
    sa = SentimentAnalyzer()
    sa.analyze()

if __name__ == "__main__":
    test()