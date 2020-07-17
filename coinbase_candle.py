import time
from datetime import datetime, timedelta

from coinbase.public_client import PublicClient
from csv_file import create_csv, write_csv

file_name = "coinbase_last8day_candle.csv"
FILE_HEADER = ["symbol", "time", "low", "high", "open", "close", "volume"]
currency_usd_price = {}


def execute():
    symbol_list, currency_usd_list = get_symbol_currency_list()
    create_csv(file_name, FILE_HEADER)

    for symbol in symbol_list:
        write_candle(symbol)
        time.sleep(1)
    return


def get_symbol_currency_list():
    products = client.get_products()
    print(products)
    symbol_list, currency_usd_list = parse_product(products, symbol_field="id", currency_field="base_currency")
    return symbol_list, currency_usd_list


def write_candle(symbol):
    candles = get_candles(symbol)
    append_csv(file_name, candles)
    return


def get_candles(symbol):
    candle_list = []
    candles = client.get_product_historic_rates(symbol, start=start_day, end=end_day, granularity=86400)
    for candle in candles:
        row = {}
        row["symbol"] = symbol
        row["time"] = datetime.utcfromtimestamp(candle[0]).isoformat()
        row["low"] = candle[1]
        row["high"] = candle[2]
        row["open"] = candle[3]
        row["close"] = candle[4]
        row["volume"] = candle[5]
        candle_list.append(row)
        currency_usd = get_currency_usd(symbol)
    return candle_list


def parse_product(products, symbol_field, currency_field):
    symbol_list = []
    currency_usd_list = []
    if products and len(products):
        for item in products:
            symbol = item.get(symbol_field)
            currency = item.get(currency_field)
            symbol_list.append(symbol)
            currency_usd = "{currency}-USD".format(currency=currency)
            currency_usd_list.append(currency_usd)

    return symbol_list, currency_usd_list


def get_currency_usd(symbol):
    position = symbol.find('-')
    return symbol[:position] + "-USD"


def append_csv(file_name, candle_list):
    for candle in candle_list:
        # print(candle)
        write_csv(file_name, FILE_HEADER, candle)

    return


client = PublicClient()
end_day = datetime.now().isoformat()
start_day = (datetime.now() - timedelta(hours=192)).isoformat()

execute()


