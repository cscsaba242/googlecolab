from broker_abs import Broker, MTime, MRange
import requests
from typing import Tuple

class ByBit(Broker):
  CATEGORY = "linear"
  URL = "https://api-testnet.bybit.com"
  max_data_per_request = 1000
  LOG_CONFIG = "./robot/broker_logging.yaml"
  
  def __init__(self, tz, max):
    self.name = "bybit"
    super().__init__(tz, max)
  
  def request_data(self, symbol:str, mrange_loc: MRange) -> Tuple[dict, str]:
    RESP_CODE = "retCode"
    RESP_MSG = "retMsg"
    RESP_SYM = "symbol"
    RESP_RES = "result"

    mrange_utc = MRange(MTime(mrange_loc.start.dt), MTime(mrange_loc.end.dt), mrange_loc.interval_min)
    
    self.logger.info(f"{symbol=}, {mrange_loc.interval=}")
    self.logger.info(f"start_loc:{mrange_loc.start.s} / end_loc:{mrange_loc.end.s}") 
    self.logger.info(f"start_utc:{mrange_utc.start.s} / end_utc:{mrange_utc.end.s}")
    
    url = f"{self.URL}/v5/market/kline?category={self.CATEGORY}&symbol={symbol}&interval={mrange_loc.interval_min}&start={mrange_utc.start.si}&end={mrange_utc.end.si}"
    response = requests.request("GET", url, headers=self.headers, data=self.payload).json()
    
    if(response[RESP_CODE] != 0 or response[RESP_MSG] != 'OK' or response[RESP_RES][RESP_SYM] != symbol):
      errMsg = f"Resquest error {response[RESP_CODE]}, {response[RESP_MSG]}, {response[RESP_RES][RESP_SYM]}"
      self.logger.error(errMsg)
      raise Exception (errMsg)
    
    self.logger.info(f"ByBit.request_data: {response[RESP_CODE]=}, {response[RESP_MSG]=}")
    return response[RESP_RES]['list'], url