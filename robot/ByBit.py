from IRequestData import IRequestData
from MTime import MTime
from MRange import MRange
import requests
from typing import Tuple, List
from datetime import datetime

symbols = [{"SYM": "BTCUSD", "INT":"1", "DATA": [], "LAST_TIME": 0}, 
           {"SYM": "BTCUSD", "INT":"3", "DATA": [], "LAST_TIME": 0}]

class ByBit(IRequestData):
  CATEGORY = "linear"
  URL = "https://api-testnet.bybit.com"
  max_data_per_request = 1000
  
  def __init__(self, tz, max):
    self.name = "bybit"
    self.tz_loc = tz
    super().__init__(self.name, tz, max)
    self.data = [{"SYM": "BTCUSD", "INT":"1", "DATA": [], "LAST_TIME": 0}, 
    {"SYM": "BTCUSD", "INT":"3", "DATA": [], "LAST_TIME": 0}]

  
  def request_data(self, mrange: MRange) -> Tuple[List, str]:
    if len(mrange.pages) == 0:
        return None, None
    RESP_CODE = "retCode"
    RESP_MSG = "retMsg"
    RESP_SYM = "symbol"
    RESP_RES = "result"
    RESP_DATA_LIST = "list"

    for data in self.data:
      result = []
      for page in mrange.pages:
        url = f"{self.URL}/v5/market/kline?category={self.CATEGORY}&symbol={data['SYM']}&interval={mrange.interval_min}&start={page[0]}&end={page[1]}"
        response = requests.request("GET", url, headers=self.headers, data=self.payload).json()
        
        if(response[RESP_CODE] != 0 or response[RESP_MSG] != 'OK' or response[RESP_RES][RESP_SYM] != data['SYM']):
          errMsg = f"Resquest error {response[RESP_CODE]}, {response[RESP_MSG]}, {response[RESP_RES][RESP_SYM]}"
          self.logger.error(errMsg)
          raise Exception (errMsg)
        
        self.logger.info(f"ByBit.request_data: {response[RESP_CODE]=}, {response[RESP_MSG]=}")
        result += response[RESP_RES][RESP_DATA_LIST]   
    return result
    

