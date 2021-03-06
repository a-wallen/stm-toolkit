import json
from typing import List, Dict

# https://alpaca.markets/docs/api-references/market-data-api/news-data/historical/


class AlpacaImage():
    """Alpaca APIs definition of an image

    JSON Example
    {
    "size": "large",
    "url": "https://cdn.benzinga.com/files/imagecache/2048x1536xUP/images/story/2012/doge_12.jpg"
    }
    """

    def __init__(self,
                 size: str,
                 url: str,
                 ):
        self.size = size
        self.url = url

    def __str__(self) -> str:
        return "[ " + str(self.size) + " | " + str(self.url) + " ]"


    def __dict__(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __repr__(self) -> str:
        return self.__dict__



if __name__ == "__main__":
    import doctest
    doctest.testmod()
