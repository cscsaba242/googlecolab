import pytz
from IRequestData import IRequestData
from MRange import MRange
import requests
from typing import Tuple, List
from MException import MException
from MTime import MTime
import datetime as dt

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
    result_len = len(result)
    test = self._debug_get_time_array(result)
    return_msg = ""
    # TODO must go to IRequestData.py 
    if(result_len == 0):
        return_msg = "No data returned from ByBit"
        self.logger.warning(return_msg)
    
    elif(result[-1][0] != str(mrange.pages[-1][0])):
        return_msg = f"ByBit: Data end time error: {result[-1][0]} != {mrange.pages[-1][0]}"
        self.logger.error(return_msg)
        raise MException(return_msg, self.name)

    elif(result[0][0] != str(mrange.pages[0][1])):
        return_msg = f"ByBit: Data start time error: {result[0][0]} != {mrange.pages[0][1]}"
        self.logger.error(return_msg)
        raise MException(return_msg, self.name) 
    
    if(result_len != int(mrange.diff_min / mrange.interval_min * self.max_data_per_request)):
        return_msg = f"{self.name} :Data array length error: {result_len} != {int(mrange.diff_min / mrange.interval_min * self.max_data_per_request)}"
        self.logger.error(return_msg)
        raise MException(return_msg, self.name)
    return result
  
    # make a function which converts the result array first column to by s property fo MTime
  def _debug_get_time_array(self, data_array: List) -> List[MTime]:
      time_array = []
      for row in data_array:
          time_array.append(MTime(dt.datetime.fromtimestamp(int(int(row[0])/1000), pytz.utc)).s)
      return time_array
     