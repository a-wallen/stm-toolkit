from tokenize import Double
from typing import List, Dict

# https://alpaca.markets/docs/api-references/market-data-api/stock-pricing-data/historical/
class AlpacaQuote():
    """
    # timestamp (t),
    # ask exchange (ax), 
    # ask price (ap), 
    # ask size (as), 
    # bid exchange (bx), 
    # bid price (bp), 
    # bid size(bs), 
    # and quote conditions (c) for 10 quotes(as this was our limit).
    # (z)	string	Tape

    JSON Example:
    {
        "symbol": "SPY",
        "quote": {
            "t": "2021-05-13T14:27:51.742904322Z",
            "ax": "V",
            "ap": 411.02,
            "as": 2,
            "bx": "V",
            "bp": 411,
            "bs": 1,
            "c": [
                "R"
            ],
            "z": 'C'
        }
    }
    """
    def __init__(
        self,
        symbol: str,
        t: str,
        ax: str,
        ap: float,
        asize: int,
        bx: str,
        bp: int,
        bs: int,
        c: List[str],
        z: str
    ):
        self.symbol = symbol
        self.t = t
        self.ax = ax
        self.ap = ap
        self.asize = asize
        self.bx = bx
        self.bp = bp
        self.bs = bs
        self.c = c
        self.z = z

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    quote = AlpacaQuote("a", "a", "a", 3.2, 4, "str", 4, 3, ["str"], "C")
    print(quote.__dict__)
    print(str(quote))