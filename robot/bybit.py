import broker_abs
from broker_abs import Broker, MTime
import pandas
from pandas import DataFrame
import requests
from datetime import datetime
import pytz
import pdb
from typing import Tuple

class ByBit(Broker):
  CATEGORY = "linear"
  URL = "https://api-testnet.bybit.com"

  def __init__(self, logger, tz):
    super().__init__(logger, tz)
  
  def request_data(self, symbol:str, interval_sec:str, start_loc: MTime, end_loc:MTime) -> Tuple[dict, str]:
    RESP_CODE = "retCode"
    RESP_MSG = "retMsg"
    RESP_SYM = "symbol"
    RESP_RES = "result"

    start_utc = MTime(start_loc.dt)
    end_utc = MTime(end_loc.dt)
    
    self.logger.info(f"{symbol=}, {interval_sec=}")
    self.logger.info(f"start_loc:{start_loc.s} / end_loc:{end_loc.s}") 
    self.logger.info(f"start_utc:{start_utc.s} / end_utc:{end_utc.s}")
    
    url = f"{self.URL}/v5/market/kline?category={self.CATEGORY}&symbol={symbol}&interval={interval_sec}&start={start_utc.si}&end={end_utc.si}"
    response = requests.request("GET", url, headers=self.headers, data=self.payload).json()
    
    if(response[RESP_CODE] != 0 or response[RESP_MSG] != 'OK' or response[RESP_RES][RESP_SYM] != symbol):
      errMsg = f"Resquest error {response[RESP_CODE]}, {response[RESP_MSG]}, {response[RESP_RES][RESP_SYM]}"
      self.logger.error(errMsg)
      raise Exception (errMsg)
    
    self.logger.info(f"ByBit.request_data: {response[RESP_CODE]=}, {response[RESP_MSG]=}")
    return response[RESP_RES]['list'], url
  
    #lf=DataFrame()
    #lf = pandas.DataFrame(resp["result"]["list"], columns=broker_abs.COLS)
    #lf['Date'] = pandas.to_datetime(lf['Date'], unit="ms")
    #lf['Open'] = self.convNum(lf['Open'])
    #lf['High'] = self.convNum(lf['High'])
    #lf['Low'] = self.convNum(lf['Low'])
    #lf['Close'] = self.convNum(lf['Close'])
