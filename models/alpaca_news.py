from alpaca_image import AlpacaImage
from typing import List, Dict

# https://alpaca.markets/docs/api-references/market-data-api/news-data/historical/


class AlpacaNews():
    """Alpaca's definition of a news article

    JSON Example:
    {
        "id": 24803233,
        "headline": "Benzinga's Top 5 Articles For 2021 — Or 'Who Let The Dog Out?'",
        "author": "Sue Strachan",
        "created_at": "2021-12-29T15:11:03Z",
        "updated_at": "2021-12-30T20:37:41Z",
        "summary": "2021 may have been the Year of the Ox in the Chinese calendar, but for Benzinga, it was the Year of the Dog, or should we say, Year of the Dogecoin (CRYPTO: DOGE).",
        "content": "<p>2021 may have been the Year of the Ox in the Chinese calendar, but for Benzinga, it was the Year of the Dog, or should we say, Year of the <strong>Dogecoin</strong> (CRYPTO: <a class=\"ticker\" href=\"https://www.benzinga.com/quote/doge/usd\">DOGE</a>).</p>\r\n\r\n<p>The memecoin created in 2013....",
        "images": [
            {
                "size": "large",
                "url": "https://cdn.benzinga.com/files/imagecache/2048x1536xUP/images/story/2012/doge_12.jpg"
            },
            {
                "size": "small",
                "url": "https://cdn.benzinga.com/files/imagecache/1024x768xUP/images/story/2012/doge_12.jpg"
            },
            {
                "size": "thumb",
                "url": "https://cdn.benzinga.com/files/imagecache/250x187xUP/images/story/2012/doge_12.jpg"
            }
        ],
        "symbols": [
            "AMZN",
            "BTCUSD",
            "COIN",
            "DOGEUSD",
            "SPCE",
            "TSLA",
            "TWTR"
        ],
        "source": "benzinga"
    }
    """

    def __init__(
        self,
        id: str,
        headline: str,
        author: str,
        created_at: str,
        updated_at: str,
        summary: str,
        content: str,
        # images: List[AlpacaImage],
        symbols: List[str],
        source: str,
    ):
        self.id = id
        self.headline = headline
        self.author = author
        self.created_at = created_at
        self.updated_at = updated_at
        self.summary = summary
        self.content = content
        # self.images = images
        self.tickers = symbols
        self.source = source

    def __str__(self) -> str:
        return "[ " + str(self.id) + " | " + str(self.headline) + " | " + str(self.author) + " | " + str(self.summary) + " | " + str(self.content) + " | " + str(self.tickers) + " | " + str(self.source) + " ]"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
