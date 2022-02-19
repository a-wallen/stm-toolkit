import sys, os

# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))

from alpaca_news import AlpacaNews as News

def extractRelevantData(article : News) -> None:
    headline = article.headline
    author = article.author
    created_at = article.created_at
    updated_at = article.updated_at
    summary = article.summary
    content = article.content
    images = article.images
    symbols = article.symbols
    source = article.source

    print(f"HEADLINE:\n {headline} \n")
    print(f"AUTHOR\n {author} \n")
    print(f"CREATED\n {created_at} \n")
    print(f"UPDATED\n {updated_at} \n")
    print(f"SUMMARY:\n {summary} \n")
    print(f"CONTENT:\n {content} \n")
    print("IMAGES:\n")
    for image in images:
        print('Size: {0}, URL: {1}'.format(image['size'], image['url']))
    print("\n")
    print("SYMBOLS:\n")
    for symbol in symbols:
        print(symbol, end=' ')
    print("\n")

def main() -> None:

    article = News(
        24803233,
        "Benzinga's Top 5 Articles For 2021 — Or 'Who Let The Dog Out?'",
        "Sue Strachan",
        "2021-12-29T15:11:03Z",
        "2021-12-30T20:37:41Z",
        "2021 may have been the Year of the Ox in the Chinese calendar, but for Benzinga, it was the Year of the Dog, or should we say, Year of the Dogecoin (CRYPTO: DOGE).",
        "<p>2021 may have been the Year of the Ox in the Chinese calendar, but for Benzinga, it was the Year of the Dog, or should we say, Year of the <strong>Dogecoin</strong> (CRYPTO: <a class=\"ticker\" href=\"https://www.benzinga.com/quote/doge/usd\">DOGE</a>).</p>\r\n\r\n<p>The memecoin created in 2013....",
        [
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

    extractRelevantData(article)

if __name__ == '__main__':
    main()