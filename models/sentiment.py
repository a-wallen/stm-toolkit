class Sentiment():
    def __init__(
        self,
        positive: float,
        neutral: float,
        negative: float,
        article_url: str = None,
    ):
        self.article_url = article_url
        self.positive = positive
        self.neutral = neutral
        self.negative = negative
        pass

    def __del__(self):
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()