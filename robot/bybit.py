import broker_abs
from broker_abs import Broker, MTime, MRange
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
  max_data_per_request = 1000


  def __init__(self, logger, tz, max):
    super().__init__(logger, tz, max)
  
  def request_data(self, symbol:str, mrange_loc: MRange) -> Tuple[dict, str]:
    RESP_CODE = "retCode"
    RESP_MSG = "retMsg"
    RESP_SYM = "symbol"
    RESP_RES = "result"

    mrange_utc = MRange(MTime(mrange_loc.start.dt), MTime(mrange_loc.end.dt), mrange_utc.interval_ms)
    
    self.logger.info(f"{symbol=}, {interval=}")
    self.logger.info(f"start_loc:{mrange_loc.start.s} / end_loc:{mrange_loc.end.s}") 
    self.logger.info(f"start_utc:{mrange_utc.start.s} / end_utc:{mrange_utc.end.s}")
    
    url = f"{self.URL}/v5/market/kline?category={self.CATEGORY}&symbol={symbol}&interval={interval}&start={mrange_utc.start.si}&end={mrange_utc.end.si}"
    response = requests.request("GET", url, headers=self.headers, data=self.payload).json()
    
    if(response[RESP_CODE] != 0 or response[RESP_MSG] != 'OK' or response[RESP_RES][RESP_SYM] != symbol):
      errMsg = f"Resquest error {response[RESP_CODE]}, {response[RESP_MSG]}, {response[RESP_RES][RESP_SYM]}"
      self.logger.error(errMsg)
      raise Exception (errMsg)
    
    self.logger.info(f"ByBit.request_data: {response[RESP_CODE]=}, {response[RESP_MSG]=}")
    return response[RESP_RES]['list'], url