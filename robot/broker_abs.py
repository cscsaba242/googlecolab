from abc import ABC, abstractmethod
from datetime import datetime, timezone
from collections import namedtuple
from MTime import MTime
from MRange import MRange
import logging
from logging import Logger
from logging import config
import yaml
import pdb
from typing import Tuple, List
import asyncio

COLS=['Date','Open','High','Low','Close', 'x', 'y']
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
  '''
  generaly 1 min in ms 60 * 1000
  '''
  request_max_time_ms = 0
  '''
  max ms per request based on smallest interval e.g 1min * 1000 (max data per request)
  in ms 60 * 1000 * 1000 = 60_000_000
  '''

  def __init__(self, tz_loc, max_data_per_request = 0):
    self.logger = self.getLogger(self.name)
    self.tz_loc = tz_loc
    self.max_data_per_request = max_data_per_request
    now = datetime.now()
    self.start_dt_utc = MTime(now)
    self.start_dt_loc = MTime(now, tz_loc)
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
        errMsg = f"Request data length error: {len(result)} != {mrange.diff_interval}"
        self.logger.error(errMsg)
        raise Exception (errMsg)
    return result, url

  def getDataAsDataFrame(self, symbol: str, range: MRange) -> List:
    data, url =self.request_data_wrapper(symbol, range)
    return data

  def getLogger(self, config_name: str) -> Logger:
    with open(self.LOG_CONFIG, "r") as file:
        config: dict = yaml.safe_load(file)
        config['handlers']['timed_file']['filename'] = config_name + '.log'
        logging.config.dictConfig(config)
        logger = logging.getLogger(__name__)
        return logger