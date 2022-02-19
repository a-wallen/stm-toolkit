import sys, os

# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))

from alpaca_news import AlpacaNews as News

def readAndPrint(article : News) -> None:
    headline = article.headline
    summary = article.summary
    content = article.content
    symbols = article.symbols

    print("HEADLINE:\n\n" + headline)
    print("SUMMARY:\n\n" + summary)
    print("CONTENT:\n\n" + content)
    print("SYMBOLS:\n\n")
    for symbol in symbols:
        print(symbol, end=' ')

def main() -> None:

    article = News(
        24803233,
        "Benzinga's Top 5 Articles For 2021 — Or 'Who Let The Dog Out?'",
        "Sue Strachan",
        "2021-12-29T15:11:03Z",
        "2021-12-30T20:37:41Z",
        "2021 may have been the Year of the Ox in the Chinese calendar, but for Benzinga, it was the Year of the Dog, or should we say, Year of the Dogecoin (CRYPTO: DOGE).",
        "<p>2021 may have been the Year of the Ox in the Chinese calendar, but for Benzinga, it was the Year of the Dog, or should we say, Year of the <strong>Dogecoin</strong> (CRYPTO: <a class=\"ticker\" href=\"https://www.benzinga.com/quote/doge/usd\">DOGE</a>).</p>\r\n\r\n<p>The memecoin created in 2013....",
        [],
        [
            "AMZN",
            "BTCUSD",
            "COIN",
            "DOGEUSD",
            "SPCE",
            "TSLA",
            "TWTR"
        ],
        "benzinga"
    )

    readAndPrint(article)

if __name__ == '__main__':
    main()