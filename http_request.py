import requests

session = requests.Session()

class CoinbaseTrade:
    trade_id = 0
    time = ""
    price = ""
    size = ""

def get_coinbase_trade(symbol, afterId):
    if afterId == 0:
        url = "https://api.pro.coinbase.com/products/{symbol}/trades".format(symbol=symbol)
    else:
        url = "https://api.pro.coinbase.com/products/{symbol}/trades?after={afterId}".format(symbol=symbol, afterId=afterId)

    return session.get(url)

