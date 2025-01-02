import broker_abs
from broker_abs import Broker
import pandas
from pandas import DataFrame
import requests
from datetime import datetime
import pytz
import pdb

class ByBit(Broker):
  CATEGORY = "linear"
  URL = "https://api-testnet.bybit.com"

  def __init__(self, logger, tz):
    super().__init__(logger, tz)
  
  def request_data(self, symbol:str, interval_sec:str, start_loc: datetime, end_loc:datetime) -> DataFrame:
    start_utc = start_loc.astimezone(pytz.utc)
    end_utc = end_loc.astimezone(pytz.utc)
    
    self.logger.info(f"{symbol=}, {interval_sec=}")
    self.logger.info(f"start_loc:{self.dtime_str(start_loc)} / end_loc:{self.dtime_str(end_loc)}") 
    self.logger.info(f"start_utc:{self.dtime_str(start_utc)} / end_utc:{self.dtime_str(end_utc)}")
    
    lf=DataFrame()
    start_utc_ts = str(int(start_utc.timestamp())) + "000"
    end_utc_ts = str(int(end_utc.timestamp())) + "000"
    url = f"{self.URL}/v5/market/kline?category={self.CATEGORY}&symbol={symbol}&interval={interval_sec}&start={start_utc_ts}&end={end_utc_ts}&limit=5"
    resp=requests.request("GET", url, headers=self.headers, data=self.payload).json()
    breakpoint()

    lf = pandas.DataFrame(resp["result"]["list"], columns=broker_abs.COLS)
    lf['Date'] = pandas.to_datetime(lf['Date'], unit="ms")
    lf['Open'] = self.convNum(lf['Open'])
    lf['High'] = self.convNum(lf['High'])
    lf['Low'] = self.convNum(lf['Low'])
    lf['Close'] = self.convNum(lf['Close'])

    self.logger.info(f"ByBit.request_data: {lf.size=}, {resp['retCode']=}, {resp['retMsg']=}")
    return lf
