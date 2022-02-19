from datetime import datetime

class Prediction():
    def __init__(
        self,
        ticker: str,
        starting: datetime,
        ending: datetime,
        delta: float,
        article_url: str=None,
    ):
        self.ticker = ticker
        self.starting = starting
        self.ending = ending
        self.delta = delta
        self.article_url = article_url

if __name__ == "__main__":
    import doctest
    doctest.testmod()