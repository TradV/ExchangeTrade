from datetime import datetime, timedelta

from csv_file import create_csv, write_csv
from http_request import get_coinbase_trade
import json

COINBASE_CSV_FILENAME_SUFFIX = "_coinbase_latest_trade.csv"
FILE_HEADER = ["id", "time", "price", "size", "value"]

SYMBOLS = ["BTC-USD", "XLM-USD", "ZEC-USDC", "DASH-USD", "XRP-USD",
           "ETC-USD", "BCH-USD", "EOS-USD", "ETH-USD", "LTC-USD", "OMG-USD"]


def execute():
    for symbol in SYMBOLS:
        print(f"get symbols {symbol}")
        get_latest_trade(symbol, 12, 0)


def get_latest_trade(symbol, hour_before, minute_before):
    file_name = "{symbol}_last_{hour_before}h{minute_before}m_{suffix}"\
        .format(symbol=symbol, hour_before=hour_before, minute_before=minute_before, suffix=COINBASE_CSV_FILENAME_SUFFIX)
    create_csv(file_name, FILE_HEADER)

    last_time = datetime.utcnow()
    start_time = datetime.utcnow() - timedelta(hours=hour_before, minutes=minute_before)
    last_id = 0

    while last_time > start_time:
        print(f"last_time: {last_time}, start_time: {start_time}")
        trade_list = get_trade(symbol, last_id)
        last_id, last_time = append_csv(file_name, trade_list)
        time.sleep(0.1)


def get_trade(symbol, last_id):
    response = get_coinbase_trade(symbol, last_id)
    response_text = json.loads(response.text)
    trade_list = parse_trade(trade_response=response_text, id="trade_id", time="time", price="price", size="size")
    return trade_list


def parse_trade(trade_response, id, time, price, size):
    trade_list = []
    if (trade_response and len(trade_response)):
        for item in trade_response:
            trade_item = {}
            trade_item["id"] = item.get(id)
            trade_item["time"] = item.get(time)
            trade_item["price"] = item.get(price)
            trade_item["size"] = item.get(size)
            trade_item["value"] = float(item.get(price)) * float(item.get(size))
            trade_list.append(trade_item)

    return trade_list


def append_csv(file_name, trade_list):
    last_id = 0
    last_time = datetime.now()

    for item in trade_list:
        write_csv(file_name, FILE_HEADER, item)
        last_id = item["id"]
        last_time_str = item["time"]

    last_time = datetime.strptime(last_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    return last_id, last_time


execute()
