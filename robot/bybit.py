import broker_abs
from broker_abs import Broker
import pandas
from pandas import DataFrame
import requests
from datetime import datetime
import pytz

class ByBit(Broker):
  CATEGORY = "linear"
  URL = "https://api-testnet.bybit.com"

  def __init__(self, logger, tz):
    super().__init__(logger, tz)
  
  def request_data(self, symbol:str, interval_sec:str, start_loc: datetime, end_loc:datetime) -> DataFrame:
    start_utc = start_loc.astimezone(pytz.utc)  
    end_utc = end_loc.astimezone(pytz.utc)
    
    self.logger.info(f"{symbol=}, {interval_sec=}, {start_loc=} / {start_utc}, {end_loc=} / {end_utc}")
    
    lf=DataFrame()
    url = f"{self.URL}/v5/market/mark-price-kline?category={self.CATEGORY}&symbol={symbol}&interval={interval_sec}&start={start_utc}&end={end_utc}"
    resp=requests.request("GET", url, headers=self.headers, data=self.payload).json()

    lf = pandas.DataFrame(resp["result"]["list"], columns=broker_abs.COLS)
    lf['Date'] = pandas.to_datetime(lf['Date'].astype(float))
    lf['Open'] = self.convNum(lf['Open'])
    lf['High'] = self.convNum(lf['High'])
    lf['Low'] = self.convNum(lf['Low'])
    lf['Close'] = self.convNum(lf['Close'])

    self.logger.info(f"ByBit.request_data: {lf.size=}, {resp['retCode']=}, {resp['retMsg']=}")
    return lf
