class Sentiment():
    def __init__(
        self,
        article_url: str,
        positive: float,
        neutral: float,
        negative: float,
    ):
        self.article_url = article_url
        self.positive = positive
        self.neutral = neutral
        self.negative = negative
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()