from getprices_abs import GetPrices
import pandas
from pandas import DataFrame
import requests
from datetime import datetime

class ByBit(GetPrices):
  CATEGORY = "linear"
  URL = "https://api-testnet.bybit.com"

  async def do(self, symbol:str, interval:str, start: datetime, end:datetime) -> DataFrame:
    self.logger.info(f"ByBit.do: {symbol=}, {interval=}, {start=}, {end=}")
    
    start_ts = start.timestamp(start)
    end_ts = end.timestamp(end)

    lf=DataFrame()
    url = f"{self.URL}/v5/market/mark-price-kline?category={self.CATEGORY}&symbol={symbol}&interval={interval}&start={start}&end={end}"
    resp=requests.request("GET", url, headers=self.headers, data=self.payload).json()

    lf = pandas.DataFrame(resp["result"]["list"], columns=self.COLS)
    lf['Date'] = pandas.to_datetime(lf['Date'].astype(float))
    lf['Open'] = self.convNum(lf['Open'])
    lf['High'] = self.convNum(lf['High'])
    lf['Low'] = self.convNum(lf['Low'])
    lf['Close'] = self.convNum(lf['Close'])

    self.logger.info(f"ByBit.do: {lf.size=}, {resp['retCode']=}, {resp['retMsg']=}")
    return lf
  
  pass