from datetime import datetime, timedelta

from csv_file import create_csv, write_csv
from http_request import get_coinbase_trade
import json

COINBASE_CSV_FILEPATH = "coinbase_latest_trade.csv"
FILE_HEADER = ["id", "time", "price", "size"]

def get_latest_trade(symbol, latest_hour):
    write_file_header()

    last_time = datetime.utcnow()
    start_time = datetime.utcnow() - timedelta(hours=latest_hour)
    last_id = 0

    while last_time > start_time:
        trade_list = get_trade(symbol, last_id)
        last_id, last_time = append_file(trade_list)

def get_trade(symbol, lastId):
    response = get_coinbase_trade(symbol, lastId)
    response_text = json.loads(response.text)
    trade_list = parse_trade(trade_response=response_text, id="trade_id", time="time", price="price", size="size")
    return trade_list

def parse_trade(trade_response, id, time, price, size):
    trade_list = []
    if (trade_response and len(trade_response)):
        for item in trade_response:
            trade_item = {}
            trade_item["id"] = item.get(id)
            trade_item[time] = item.get(time)
            trade_item[price] = item.get(price)
            trade_item[size] = item.get(size)
            trade_list.append(trade_item)

    return trade_list

def write_file_header():
    create_csv(COINBASE_CSV_FILEPATH, FILE_HEADER)

def append_file(trade_list):
    last_id = 0;
    last_time = datetime.now()

    for item in trade_list:
        write_csv(COINBASE_CSV_FILEPATH, FILE_HEADER, item)
        last_id = item["id"]
        last_time_str = item["time"]

    last_time = datetime.strptime(last_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    return last_id, last_time


get_latest_trade("BTC-USD", 2)
