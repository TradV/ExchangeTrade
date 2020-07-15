import requests

from key import BINANCE_API_KEY

session = requests.Session()

def get_coinbase_trade(symbol, after_id):
    if after_id == 0:
        url = "https://api.pro.coinbase.com/products/{symbol}/trades".format(symbol=symbol)
    else:
        url = "https://api.pro.coinbase.com/products/{symbol}/trades?after={after_id}".format(symbol=symbol, after_id=after_id)

    return session.get(url)

def get_okex_trade(symbol, after_id):
    if after_id == 0:
        url = "https://www.okex.com/api/spot/v3/instruments/{symbol}/trades".format(symbol=symbol)
    else:
        url = "https://www.okex.com/api/spot/v3/instruments/{symbol}/trades?after={after_id}".format(symbol=symbol, after_id=after_id)

    return session.get(url)

def get_binance_trade(symbol, from_id, size=100):
    if from_id == 0:
        url = "https://api.binance.com/api/v3/historicalTrades?symbol={symbol}&limit={size}".format(symbol=symbol, size=size)
    else:
        url = "https://api.binance.com/api/v3/historicalTrades?symbol={symbol}&fromId={from_id}&limit={size}"\
            .format(symbol=symbol, from_id=from_id, size=size)

    session.headers.update({"X-MBX-APIKEY" : BINANCE_API_KEY})
    return session.get(url)
