
from IBroker import IBroker
from typing import List
from MRange import MRange
import yfinance as yf

symbols = {"AAPL"}

class YahooFinance(IBroker):
    def __init__(self):
        self.name = "yahoofinance"

    def request_data(self, range: MRange) -> List:
        for symbol in symbols:
            symbol = symbol
            df = yf.download(tickers=symbol, start=range.start.sYmdHMS, end=range.end.sYmdHMS)
            print(df.index)
            print(df.columns)
            print(df.head())
        return 
