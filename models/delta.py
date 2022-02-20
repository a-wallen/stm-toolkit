class Delta():
    def __init__(
        self,
        symbol: str,
        delta: str,
        open: str,
        close: str,
        date: str,
    ):
        self.symbol = symbol
        self.delta = delta
        self.open = open
        self.close = close
        self.date = date

if __name__ == "__main__":
    import doctest
    doctest.testmod()