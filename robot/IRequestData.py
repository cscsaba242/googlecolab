from abc import ABC, abstractmethod

import pytz

from MRange import MRange
from logging import Logger
import sys
import os
import pandas as pd
from pandas import DataFrame
from typing import List
import time

from MException import MException
from MLogger import MLogger

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

class IRequestData(ABC, MLogger):
  name: str = None
  tz_loc = pytz.timezone('Europe/Budapest')
  logger: Logger = None
  payload = {}
  headers = {}
  MAX_DATA_PER_REQUEST = 1000
  COLS=[]
  URL = None
  data = None # data description what we need
  run_file_name = None
  
  def __init__(self, name, tz_loc, max_data_per_request = 10, cols = COLS, symbols = []):
    self.name = name
    self.logger = self._getLogger(self.name)
    self.tz_loc = tz_loc
    self.max_data_per_request = max_data_per_request
    self.COLS = cols
    self.run_file_name = f'run_{self.name}.txt'

  @abstractmethod
  def request_data(self, range: MRange) -> List:
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
          df = self._getDataAsDataFrame(range)
          i = 0
      self._on_end("OK")
    except Exception:
      self._on_end("Exception")

  # PROTECTED METHODS
  def _request_data_validator_wrapper(self, mrange: MRange) -> List:
    result = self.request_data(mrange)
    if result is None:
       raise MException("No data returned from broker", self.name)
    
    result = sorted(result, key=lambda d: d[0])
    
    if(len(result) != mrange.diff_interval_min):
        errMsg = f"Request data length error: {len(result)} != {mrange.diff_interval_min}"
        self.logger.error(errMsg)
        raise Exception (errMsg)
    else:
       self.logger.info(f"Requested data length OK. {len(result)=} == {mrange.diff_interval_min=}")
    return result

  def _getDataAsDataFrame(self, range: MRange) -> List:
    data = self._request_data_validator_wrapper(range)
    if data is None:
      return None
    result = pd.DataFrame(data, columns=self.COLS)
    result['timestamp'] = pd.to_datetime(result['timestamp'], unit='ms')
    for col in ['Open', 'High', 'Low', 'Close']:
        if col in result.columns:
          result[col] = pd.to_numeric(result[col], errors='coerce')
    return result

  def _on_end(self, message):
    if os.path.exists(self.run_file_name):
      os.remove(self.run_file_name)
      self.logger.info(f"on_end: {self.run_file_name} end: {message}")
    return
  
  def _put_progress_text(self, text, x, y):
        progress_char = "-" if x % y == 0 else "+"   
        sys.stdout.write('\r' + progress_char + text)
        sys.stdout.flush()