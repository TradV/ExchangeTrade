import requests

from key import BINANCE_API_KEY

session = requests.Session()

def get_coinbase_trade(symbol, afterId):
    if afterId == 0:
        url = "https://api.pro.coinbase.com/products/{symbol}/trades".format(symbol=symbol)
    else:
        url = "https://api.pro.coinbase.com/products/{symbol}/trades?after={afterId}".format(symbol=symbol, afterId=afterId)

    return session.get(url)

def get_okex_trade(symbol, afterId):
    if afterId == 0:
        url = "https://www.okex.com/api/spot/v3/instruments/{symbol}/trades".format(symbol=symbol)
    else:
        url = "https://www.okex.com/api/spot/v3/instruments/{symbol}/trades?after={afterId}".format(symbol=symbol, afterId=afterId)

    return session.get(url)

def get_binance_trade(symbol, fromId):
    if fromId == 0:
        url = "https://api.binance.com/api/v3/historicalTrades?symbol={symbol}".format(symbol=symbol)
    else:
        url = "https://api.binance.com/api/v3/historicalTrades?symbol={symbol}&fromId={fromId}".format(symbol=symbol, fromId=fromId)

    session.headers.update({"X-MBX-APIKEY" : BINANCE_API_KEY})
    return session.get(url)
