from alpaca_news import AlpacaNews

class Sentiment():
    def __init__(
        self,
        article: AlpacaNews,
        positive: float,
        neutral: float,
        negative: float,
        compound: float,
    ):
        self.article_url = article
        self.positive = positive
        self.neutral = neutral
        self.negative = negative
        self.compound = compound
        pass

    def __del__(self):
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()