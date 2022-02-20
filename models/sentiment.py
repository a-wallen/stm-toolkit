from typing import List

class Sentiment():
    """Contains data for sentiment analysis report"""

    def __init__(
        self,
        # id: str,
        symbols: List[str],
        source: str,
        date: str,
        positive: float,
        neutral: float,
        negative: float,
        compound: float,
    ):
        # self.id = id
        self.symbols = symbols
        self.source = source
        self.date = date
        self.positive = positive
        self.neutral = neutral
        self.negative = negative
        self.compound = compound

    def __del__(self):
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()