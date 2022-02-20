from alpaca_news import AlpacaNews
from typing import List, Dict

class Sentiment():
    def __init__(
        self,
        ticker: List[str],
        source: str,
        date: str,
        positive: float,
        neutral: float,
        negative: float,
        compound: float,
    ):
        self.ticker = ticker
        self.source = source
        self.date = date,
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