import time
from datetime import datetime, timedelta

from csv_file import create_csv, write_csv
from http_request import get_binance_trade
import json

BINANCE_CSV_FILENAME_SUFFIX = "_binance_latest_trade.csv"
FILE_HEADER = ["id", "time", "price", "size", "value"]
BATCH_COUNT = 100

SYMBOLS = ["BTCUSDT", "ADAUSDT", "IOTAUSDT", "XLMUSDT", "XMRUSDT", "ZECUSDT", "DASHUSDT",
           "XRPUSDT", "ETCUSDT", "BCHUSDT", "EOSUSDT", "ETHUSDT", "LTCUSDT", "OMGUSDT"]

def execute():
    for symbol in SYMBOLS:
        print(f"get symbols {symbol}")
        get_latest_trade(symbol, 12, 0)
        time.sleep(10)

def get_latest_trade(symbol, hour_before, minute_before):
    file_name = "{symbol}_last_{hour_before}h{minute_before}m_{suffix}" \
        .format(symbol=symbol, hour_before=hour_before, minute_before=minute_before,
                suffix=BINANCE_CSV_FILENAME_SUFFIX)
    create_csv(file_name, FILE_HEADER)

    last_time = datetime.utcnow()
    start_time = datetime.utcnow() - timedelta(hours=hour_before, minutes=minute_before)
    last_id = 0

    while last_time > start_time:
        print(f"last_time: {last_time}, start_time: {start_time}, last_id: {last_id}")
        trade_list = get_trade(symbol, last_id, BATCH_COUNT)
        last_id, last_time = append_csv(file_name, trade_list)
        last_id = last_id - BATCH_COUNT
        time.sleep(0.2)

def get_trade(symbol, last_id, size):
    response = get_binance_trade(symbol, last_id, size)
    response_text = json.loads(response.text)
    trade_list = parse_trade(trade_response=response_text, id="id", time="time", price="price", size="qty")
    return trade_list

def parse_trade(trade_response, id, time, price, size):
    trade_list = []
    if trade_response and len(trade_response):
        for item in trade_response:
            trade_item = {}
            trade_item["id"] = int(item.get(id))
            trade_item["time"] = datetime.utcfromtimestamp(item.get(time)/1000).isoformat()
            trade_item["price"] = item.get(price)
            trade_item["size"] = item.get(size)
            trade_item["value"] = float(item.get(price)) * float(item.get(size))
            trade_list.append(trade_item)

    trade_list.sort(key=get_id, reverse=True)
    return trade_list

def get_id(element):
    return element.get("id")

def append_csv(file_name, trade_list):
    last_id = 0
    last_time = datetime.now()

    for item in trade_list:
        write_csv(file_name, FILE_HEADER, item)
        last_id = item["id"]
        last_time = datetime.fromisoformat(item["time"])

    return last_id, last_time


execute()
