from abc import ABC, abstractmethod
from datetime import datetime, timezone
from collections import namedtuple
from MTime import MTime
from MRange import MRange
import logging
from logging import Logger
from logging import config
import sys
import yaml
import os
import pandas as pd
from pandas import DataFrame
from typing import Tuple, List
import time

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

class Broker(ABC):
  name: str = None
  tz_loc = None
  logger: Logger = None
  payload = {}
  headers = {}
  start_dt_utc: MTime
  start_time_loc: MTime
  max_data_per_request = 1000
  smallest_interval_ms = 60_000
  cols=[]
  df: DataFrame = None
  run_file_name = 'run.txt'
  '''
  controlling the run of script from outside
  if you delete this file then main loop in script will stopped
  '''
  
  request_max_time_ms = 0
  '''
  max ms per request based on smallest interval e.g 1min * 1000 (max data per request)
  in ms 60 * 1000 * 1000 = 60_000_000
  '''

  def __init__(self, tz_loc, max_data_per_request = 0, cols = COLS):
    self.logger = self.getLogger(self.name)
    self.on_init()

    self.tz_loc = tz_loc
    self.max_data_per_request = max_data_per_request
    now = datetime.now()
    self.start_dt_utc = MTime(now)
    self.start_dt_loc = MTime(now, tz_loc)
    self.cols = cols
    self.request_max_time_ms = self.smallest_interval_ms * self.max_data_per_request
    self.logger.info(f"start_utc:{self.start_dt_utc.s} / start_loc:{self.start_dt_loc.s}")

  @abstractmethod
  def request_data(self, symbol:str, range: MRange) -> Tuple[List, str]:
    pass

  def request_data_wrapper(self, symbol:str, mrange: MRange) -> Tuple[List, str]:
    '''
    reises: 
      - Invalid length
      - Invalid start - end date
    '''
    result, url = self.request_data(symbol, mrange)
    result = sorted(result, key=lambda d: d[0])
    
    if(len(result) != mrange.diff_interval_min):
        errMsg = f"Request data length error: {len(result)} != {mrange.diff_interval_min}"
        self.logger.error(errMsg)
        raise Exception (errMsg)
    else:
       self.logger.info(f"Requested data length OK. {len(result)=} == {mrange.diff_interval_min=}")
    return result, url

  def getDataAsDataFrame(self, symbol: str, range: MRange) -> List:
    data, url =self.request_data_wrapper(symbol, range)
    result = pd.DataFrame(data, columns=self.cols)
    result['timestamp'] = pd.to_datetime(result['timestamp'], unit='ms')
    for col in ['Open', 'High', 'Low', 'Close']:
        if col in result.columns:
          result[col] = pd.to_numeric(result[col], errors='coerce')
    return data

  def getLogger(self, config_name: str) -> Logger:
    with open(self.LOG_CONFIG, "r") as file:
        config: dict = yaml.safe_load(file)
        config['handlers']['timed_file']['filename'] = config_name + '.log'
        logging.config.dictConfig(config)
        logger = logging.getLogger(__name__)
        return logger
  
  def run(self, symbol: str, range: MRange):
    i = 0
    step = 1
    max = 65
    while os.path.exists(self.run_file_name):
      self.put_progress_text("working " + str(i) + "/" + str(max) + " sec...", i, 2)
      time.sleep(1)
      # for calling something every X sec
      i += step
      if i == max:
         # calling something
         self.logger.info(range.start.s + " - " + range.end.s)
         df = self.getDataAsDataFrame(symbol, range)
         print(df)
         range = MRange(MTime(datetime.now(range.end.tz)), MTime(datetime.now(range.end.tz)), range.interval_min, range.max)
         i = 0
    self.on_end()
  
  def on_init(self):
      if os.path.exists(self.run_file_name):
        os.remove(self.run_file_name)
        # waiting to make sure another process recognize
        # the file removel and stop itself        
        i = 0
        step = 10
        max_sec = 80
        while i != max_sec:
          text = "waiting " + str(i) + "/" + str(max_sec) + " sec... to stop and start again"
          self.put_progress_text(text, i , 20)
          time.sleep(step)
          i += step
      with open(self.run_file_name, 'w') as file:
        pass
      return
  
  def on_end(self):
    if os.path.exists(self.run_file_name):
      os.remove(self.run_file_name)
      self.logger.info(f"on_end: {self.run_file_name} normal end")
    else:
      self.logger.info(f"on_end: {self.run_file_name} not expected end")
    return
  
  def put_progress_text(self, text, x, y):
        progress_char = "-" if x % y == 0 else "+"   
        sys.stdout.write('\r' + progress_char + text)
        sys.stdout.flush()

     