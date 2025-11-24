
from IRequestData import IRequestData
from typing import List
from MRange import MRange
import yfinance as yf


class YahooFinance(IRequestData):
    def __init__(self):
        self.name = "yahoofinance"
        
    def request_data(self, range: MRange) -> List:
        for data in self.data:
            symbol = data["SYM"]
            df = yf.download(tickers=symbol, start=range.start.sYmdHMS, end=range.end.sYmdHMS)
            print(df.index)
            print(df.columns)
            print(df.head())
        return 
