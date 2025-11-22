from abc import ABC, abstractmethod

import pytz

from MRange import MRange
import logging
from logging import Logger
import sys
import yaml
import os
import pandas as pd
from pandas import DataFrame
from typing import List
import time

from MException import MException

COLS=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'FOO']
DAY_IN_SEC=86400
HOUR_IN_SEC=3600
MS=1000
SEC_IN_MIN=60

class Intervals():
    MIN1 = 1
    MIN3 = 3
    MIN5 = 5
    MIN15 = 15
    MIN30 = 30

class IBroker(ABC):
  name: str = None
  tz_loc = pytz.timezone('Europe/Budapest')
  logger: Logger = None
  payload = {}
  headers = {}
  MAX_DATA_PER_REQUEST = 1000
  COLS=[]
  URL = None
  df: DataFrame = None
  run_file_name = None
 
  def __init__(self, name, tz_loc, max_data_per_request = 10, cols = COLS, symbols = []):
    self.name = name
    self.logger = self._getLogger(self.name)
    self.tz_loc = tz_loc
    self.max_data_per_request = max_data_per_request
    self.COLS = cols
    self.run_file_name = f'run_{self.name}.txt'

  @abstractmethod
  def request_data(self, symbol:str, range: MRange) -> List:
    pass

  # PUBLIC METHODS
  def run(self, range: MRange):
    i = 0
    step = 1
    max = 65
    try:
      while os.path.exists(self.run_file_name):
        self.put_progress_text("working " + str(i) + "/" + str(max) + " sec...", i, 2)
        time.sleep(1)
        i += step
        if i == max:
          self.logger.info("range:" + range.start.s + " - " + range.end.s)
          ## df = self.getDataAsDataFrame(symbol, range)
          ## range = MRange(range.end, MTime(datetime.now(range.end.tz)), range.interval_min, range.max_per_request)
          i = 0
      self._on_end("OK")
    except Exception:
      self._on_end("Exception")

  # PROTECTED METHODS
  def _request_data_validator_wrapper(self, symbol:str, mrange: MRange) -> List:
    result = self.request_data(symbol, mrange)
    if result is None:
       raise MException("No data returned from broker", symbol, self.name)
    
    result = sorted(result, key=lambda d: d[0])
    
    if(len(result) != mrange.diff_interval_min):
        errMsg = f"Request data length error: {len(result)} != {mrange.diff_interval_min}"
        self.logger.error(errMsg)
        raise Exception (errMsg)
    else:
       self.logger.info(f"Requested data length OK. {len(result)=} == {mrange.diff_interval_min=}")
    return result

  def _getDataAsDataFrame(self, symbol: str, range: MRange) -> List:
    data = self._request_data_validator_wrapper(symbol, range)
    if data is None:
      return None
    result = pd.DataFrame(data, columns=self.COLS)
    result['timestamp'] = pd.to_datetime(result['timestamp'], unit='ms')
    for col in ['Open', 'High', 'Low', 'Close']:
        if col in result.columns:
          result[col] = pd.to_numeric(result[col], errors='coerce')
    return result

  def _getLogger(self, config_name: str) -> Logger:
    with open(self.LOG_CONFIG, "r") as file:
        config: dict = yaml.safe_load(file)
        config['handlers']['timed_file']['filename'] = config_name + '.log'
        logging.config.dictConfig(config)
        logger = logging.getLogger(__name__)
        return logger

  def _on_end(self, message):
    if os.path.exists(self.run_file_name):
      os.remove(self.run_file_name)
      self.logger.info(f"on_end: {self.run_file_name} end: {message}")
    return
  
  def _put_progress_text(self, text, x, y):
        progress_char = "-" if x % y == 0 else "+"   
        sys.stdout.write('\r' + progress_char + text)
        sys.stdout.flush()