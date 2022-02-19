from typing import List, Dict

# https://alpaca.markets/docs/api-references/market-data-api/stock-pricing-data/historical/
class AlpacaTicker():
    """Alpaca's definiton of a stock market ticker

    # t	string/timestamp	Timestamp in RFC-3339 format with nanosecond precision
    # x	string	Exchange where the trade happened
    # p	number	Trade price
    # s	int	Trade size
    # c	array	Trade conditions
    # i	int	Trade ID
    # z	string	Tape

    JSON Example:
    {
        "t": "2021-02-06T13:04:56.334320128Z",
        "x": "C",
        "p": 387.62,
        "s": 100,
        "c": [" ", "T"],
        "i": 52983525029461,
        "z": "B"
    }
    """
    def __init__(
        self,
        t: str,
        x: str,
        p: str,
        s: str,
        c: List[str],
        i: str,
        z: str,
    ):
        self.t = t
        self.x = x
        self.p = p
        self.s = s
        self.c = c
        self.i = i
        self.z = z
    
    def __iter__():
        for key in self.__dict__:
            print(key)
            if key == "t":
                yield key, str(self.__dict__[key])
            else:
                yield key, getattr(self, key)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    ticker = AlpacaTicker("a", "a","a","a",["a"],"a","a")
    print(ticker.__dict__)
    print(ticker.__iter__)