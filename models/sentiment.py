from alpaca_news import AlpacaNews

class Sentiment():
    def __init__(
        self,
        positive: float,
        neutral: float,
        negative: float,
        article: AlpacaNews,
    ):
        self.article_url = article
        self.positive = positive
        self.neutral = neutral
        self.negative = negative
        pass

    def __del__(self):
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()