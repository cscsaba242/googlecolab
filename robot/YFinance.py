
from robot import IBroker
from typing import List
from MRange import MRange
import YFinance as yf

class YFinance(IBroker):
    def __init__(self):
        pass

    
    def request_data(self, symbol:str, range: MRange) -> List:
        data = yf.download(tickers=symbol, start=range.start.s, end=end, interval=interval)
        df = yf.download("AAPL", start="2023-01-01", end="2023-01-10", interval="1d")
        print(df.index)
        print(df.columns)
        print(df.head())

        return 
