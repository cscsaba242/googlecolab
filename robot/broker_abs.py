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

class MTime():
  DATE_TIME_DISPLAY_LONG_FORMAT = "%Y %m %d %H:%M:%S.%f %z"
  dt: datetime
  s: str
  n: int
  f: str
  z: timezone
  
  def __init__(self, input, tz = timezone.utc):
    if isinstance(input, datetime):
      self.dt = input
      self.f = input.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
      self.n = int(input.timestamp())
      self.s = str(self.n)
      self.z = self.dt.tzinfo

    if isinstance(input, str):
      self.n = str(input)
      self.dt = datetime.fromtimestamp(self.n, tz)
      self.f = self.dt.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
      self.s = str(self.n)
      self.z = self.dt.tzinfo

    if isinstance(input, int):
      self.n = input
      self.dt = datetime.fromtimestamp(self.n, tz)
      self.f = self.dt.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
      self.s = str(self.n)
      self.z = self.dt.tzinfo

class Symbols(StrEnum):
    BTCUSDT = "BTCUSDT"
    ETHUSDQ = "ETHUSDQ"

class Intervals():
    MIN1 = 1
    MIN3 = 3
    MIN5 = 5
    MIN15 = 15
    MIN30 = 30

'''
- date col. must in ms
'''
class Broker(ABC):
  tz_loc = None
  logger: Logger = None
  payload = {}
  headers = {}
  start_dt_utc: MTime
  start_time_loc: MTime

  def __init__(self, logger: Logger, tz_loc):
    self.logger = logger
    self.tz_loc = tz_loc
    now = datetime.now()
    self.start_dt_utc = MTime(now)
    self.start_dt_loc = MTime(now, tz_loc)
    self.logger.info(f"start_utc:{self.start_dt_utc.f} / start_loc:{self.start_dt_loc.f}")

  @abstractmethod
  def request_data(self, symbol:str, interval_sec:int, start_utc: datetime, end_utc:datetime) -> dict:
    pass

  def request_data_wrapper(self, symbol:str, interval_sec:int, start_utc: datetime, end_utc:datetime) -> dict:
    '''
    reises: 
      - Invalid length of requested data.
    '''
    data, url = self.request_data(symbol, interval_sec, start_utc, end_utc)
    start_ts = int(start_utc.timestamp())
    end_ts = int(end_utc.timestamp())
    must_len_min = int(end_ts - start_ts) / (interval_sec * 60) 
    data_len_min = len(data)
    # lengths check
    if(data_len_min == 0 or must_len_min + 1 != data_len_min):
      errorMsg = f"Invalid response, length:{data_len_min}, must_len: {must_len_min}, url: {url}"
      self.logger.error(errorMsg)
      raise Exception(errorMsg)
    # date checks
    data_start_utc_ms = int(data[0][0])
    data_end_utc_ms = int(data[data_len_min-1][0])
    start_utc_ms = int(start_utc.timestamp() * MS)
    end_utc_ms = int(end_utc.timestamp() * MS)

    if((data_start_utc_ms != (start_utc.timestamp() * MS)) | (data_end_utc_ms != (end_utc.timestamp() * MS))):
      errMsg = f"Invalid start - end dates in the requested datas {data_start_utc_ms} / {(start_utc.timestamp() * MS)}" 
      errMsg = errMsg + f"{data_end_utc_ms} / {(end_utc.timestamp() * MS)}"
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
