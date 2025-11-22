
from IBroker import IBroker
from typing import List
from MRange import MRange
import yfinance as yf

symbols_interval_map = {"AAPL": ["1d"]}

class YahooFinance(IBroker):
    def __init__(self):
        pass

    def request_data(self, range: MRange) -> List:
        for key in symbols_interval_map:
            symbol = key
            interval = symbols_interval_map[key][0]
            df = yf.download(tickers=symbol, start=range.start.sYmdHMS, end=range.end.sYmdHMS, interval=interval)
            print(df.index)
            print(df.columns)
            print(df.head())
        return 
