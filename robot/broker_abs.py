from abc import ABC, abstractmethod
import pandas
from pandas import DataFrame, DatetimeIndex
from datetime import datetime, timezone, timedelta
from collections import namedtuple
import asyncio
import pytz
from enum import StrEnum
import pdb
from typing import Tuple
from logging import Logger

COLS=['Date','Open','High','Low','Close', 'x', 'y']
DAY_IN_SEC=86400
HOUR_IN_SEC=3600
MS=1000
SEC_IN_MIN=60

class Symbols(StrEnum):
    BTCUSDT = "BTCUSDT"
    ETHUSDQ = "ETHUSDQ"

class Intervals(StrEnum):
    MIN1 = "1"
    MIN3 = "3"
    MIN5 = "5"
    MIN15 = "15"
    MIN30 = "30"
'''
- date col. must in ms
'''
class Broker(ABC):
  tz_loc = None
  logger: Logger = None
  payload = {}
  headers = {}
  start_time_utc: datetime
  start_time_loc: datetime
  DATE_TIME_DISPLAY_LONG_FORMAT = "%Y %m %d %H:%M:%S %z"
  DATE_TIME_DISPLAY_SHORT_FORMAT = "%Y %m %d %H:%M:%S"

  def __init__(self, logger: Logger, tz_loc):
    self.logger = logger
    self.tz_loc = tz_loc
    self.start_time_utc = pytz.utc.localize(datetime.now())
    self.start_time_loc = self.start_time_utc.astimezone(self.tz_loc)
    self.logger.info(f"start_utc:{self.dtime_str(self.start_time_utc)} / start_loc:{self.dtime_str(self.start_time_loc)}")

  @abstractmethod
  def request_data(self, symbol:str, interval_sec:int, start_utc: datetime, end_utc:datetime) -> dict:
    pass

  def request_data_wrapper(self, symbol:str, interval_sec:int, start_utc: datetime, end_utc:datetime) -> dict:
    '''
    reises: 
      - Invalid length of requested data.
    '''
    data = self.request_data(symbol, interval_sec, start_utc, end_utc)
    start_ts = int(start_utc.timestamp())
    end_ts = int(end_utc.timestamp())
    must_len = int(int((end_ts - start_ts) / MS) / interval_sec)
    l = len(data)
    # lengths check
    if(l == 0.0 or must_len != l):
      errorMsg = f"Invalid length ({l}) of requested data({must_len}), interval_sec: {interval_sec}"
      self.logger.error(errorMsg)
      raise Exception(errorMsg)
    # dates checks
    start_date_utc_ms = data[0][0]
    end_date_utc_ms = data[len-1][0]
    if((start_date_utc_ms != (start_utc * MS)) | (end_date_utc_ms != (end_utc * MS))):
      errorMsg = f"Invalid start - end dates in the requested datas {start_date_utc_ms} / {(start_utc * MS)} | {end_date_utc_ms} / {(end_utc * MS)}"
      self.logger.error(errorMsg)
      raise Exception(errorMsg)
    return data
    
  def interval_in_secs(self, start: datetime, end:datetime, interval_sec: int) -> int:
    diff_end_start:timedelta = end - start
    result = diff_end_start.total_seconds() / interval_sec
    return result

  def rolling_interval(self, start: datetime, end:datetime, page_sec: int):
    start_ts = int(start.timestamp())
    end_ts = int(end.timestamp())

    diff = end_ts - start_ts
    if diff > 0:
      remainder = diff % page_sec
      # if dates are too close and diff is less than page_sec
      result = start_ts
      while result < end_ts:
        if(result + page_sec <= end_ts):
          result = result + page_sec
          yield result
        else:
          result = result + remainder
          yield result

  def convNum(self, dfParam: pandas.Series):
    return (pandas.to_numeric(dfParam)).astype(int)

  def dtime_str(self, date_time: datetime, long=True):
     if long:
        return date_time.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
     else:
        return date_time.strftime(self.DATE_TIME_DISPLAY_SHORT_FORMAT)
