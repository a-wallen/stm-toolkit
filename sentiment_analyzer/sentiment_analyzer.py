import sys, os
# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))

# sentiment analysis with nltk: https://www.nltk.org/howto/sentiment.html
# sentiment word networks: https://www.nltk.org/howto/sentiwordnet.html
# parent link: https://www.nltk.org/howto.html
import nltk # for natural language processing
from nltk import tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
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

        # 
        sentences = [   "VADER is smart, handsome, and funny.", # positive sentence example
           "VADER is smart, handsome, and funny!", # punctuation emphasis handled correctly (sentiment intensity adjusted)
           "VADER is very smart, handsome, and funny.",  # booster words handled correctly (sentiment intensity adjusted)
           "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
           "VADER is VERY SMART, handsome, and FUNNY!!!",# combination of signals - VADER appropriately adjusts intensity
           "VADER is VERY SMART, really handsome, and INCREDIBLY FUNNY!!!",# booster words & punctuation make this close to ceiling for score
           "The book was good.",         # positive sentence
           "The book was kind of good.", # qualified positive sentence is handled correctly (intensity adjusted)
           "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
           "A really bad, horrible book.",       # negative sentence with booster words
           "At least it isn't a horrible book.", # negated negative sentence with contraction
           ":) and :D",     # emoticons handled
           "",              # an empty string is correctly handled
           "Today sux",     #  negative slang handled
           "Today sux!",    #  negative slang with punctuation emphasis handled
           "Today SUX!",    #  negative slang with capitalization emphasis
           "Today kinda sux! But I'll get by, lol" # mixed sentiment example with slang and constrastive conjunction "but"
        ]

        paragraph = "It was one of the worst movies I've seen, despite good reviews. \
            Unbelievably bad acting!! Poor direction. VERY poor production. \
            The movie was bad. Very bad movie. VERY bad movie. VERY BAD movie. VERY BAD movie!"

        lines_list = tokenize.sent_tokenize(paragraph)
        sentences.extend(lines_list)

        tricky_sentences = [
            "Most automated sentiment analysis tools are shit.",
            "VADER sentiment analysis is the shit.",
            "Sentiment analysis has never been good.",
            "Sentiment analysis with VADER has never been this good.",
            "Warren Beatty has never been so entertaining.",
            "I won't say that the movie is astounding and I wouldn't claim that \
            the movie is too banal either.",
            "I like to hate Michael Bay films, but I couldn't fault this one",
            "I like to hate Michael Bay films, BUT I couldn't help but fault this one",
            "It's one thing to watch an Uwe Boll film, but another thing entirely \
            to pay for it",
            "The movie was too good",
            "This movie was actually neither that funny, nor super witty.",
            "This movie doesn't care about cleverness, wit or any other kind of \
            intelligent humor.",
            "Those who find ugly meanings in beautiful things are corrupt without \
            being charming.",
            "There are slow and repetitive parts, BUT it has just enough spice to \
            keep it interesting.",
            "The script is not fantastic, but the acting is decent and the cinematography \
            is EXCELLENT!",
            "Roger Dodger is one of the most compelling variations on this theme.",
            "Roger Dodger is one of the least compelling variations on this theme.",
            "Roger Dodger is at least compelling as a variation on the theme.",
            "they fall in love with the product",
            "but then it breaks",
            "usually around the time the 90 day warranty expires",
            "the twin towers collapsed today",
            "However, Mr. Carter solemnly argues, his client carried out the kidnapping \
            under orders and in the ''least offensive way possible.''"
        ]

        # 
        sentences.extend(tricky_sentences)
        for sentence in sentences:
            sid = SentimentIntensityAnalyzer()
            print(sentence)
        
            # Create polarity scores as a dictionary
            # EX: {compound: -0.5859, neg: 0.23, neu: 0.697, pos: 0.074}
            ss = sid.polarity_scores(sentence)

            # Print polatiry score
            print(sorted(ss.values()))
            for k in sorted(ss):
                print('{0}: {1}'.format(k, ss[k]), end='')
            print()

        # Return sentiment
        #sentiment = Sentiment(positive=ss['pos'], neutral=ss['neu'], negative=ss['neg'])
        #return sentiment

    def __del__(self) -> None:
        pass

def test() -> None:
    sa = SentimentAnalyzer()
    sentim = sa.analyze()
    # print(f'Pos: {sentim.positive}, Neut: {sentim.neutral}, Neg: {sentim.negative}')

if __name__ == "__main__":
    test()