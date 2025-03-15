from broker_abs import Broker
from MTime import MTime
from MRange import MRange
import requests
from typing import Tuple, List
from datetime import datetime


class ByBit(Broker):
  CATEGORY = "linear"
  URL = "https://api-testnet.bybit.com"
  max_data_per_request = 1000
  LOG_CONFIG = "./robot/broker_logging.yaml"
  
  def __init__(self, tz, max):
    self.name = "bybit"
    super().__init__(tz, max)
  
  def request_data(self, symbol:str, mrange: MRange) -> Tuple[List, str]:
    if len(mrange.pages):
        return None, None
    RESP_CODE = "retCode"
    RESP_MSG = "retMsg"
    RESP_SYM = "symbol"
    RESP_RES = "result"
    RESP_DATA_LIST = "list"

    result = []
    for page in mrange.pages:
      self.logger.info(f"{symbol=}, {mrange.interval_min=}")
      self.logger.info(f"start_loc:{mrange.start.s} / end_loc:{mrange.end.s}") 
      self.logger.info(f"start_utc:{mrange.start.utc.s} / end_utc:{mrange.end.utc.s}")

      url = f"{self.URL}/v5/market/kline?category={self.CATEGORY}&symbol={symbol}&interval={mrange.interval_min}&start={page[0]}&end={page[1]}"
      response = requests.request("GET", url, headers=self.headers, data=self.payload).json()
      
      if(response[RESP_CODE] != 0 or response[RESP_MSG] != 'OK' or response[RESP_RES][RESP_SYM] != symbol):
        errMsg = f"Resquest error {response[RESP_CODE]}, {response[RESP_MSG]}, {response[RESP_RES][RESP_SYM]}"
        self.logger.error(errMsg)
        raise Exception (errMsg)
      
      self.logger.info(f"ByBit.request_data: {response[RESP_CODE]=}, {response[RESP_MSG]=}")
      result += response[RESP_RES][RESP_DATA_LIST]   
    return result
    

