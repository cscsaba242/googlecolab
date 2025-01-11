from abc import ABC, abstractmethod
#import pandas
#from pandas import DataFrame, DatetimeIndex
from datetime import datetime, timezone, timedelta
from collections import namedtuple
import pytz
from enum import StrEnum
from typing import Tuple
from logging import Logger
import re
import pdb
from sqlalchemy import create_engine

COLS=['Date','Open','High','Low','Close', 'x', 'y']
DAY_IN_SEC=86400
HOUR_IN_SEC=3600
MS=1000
SEC_IN_MIN=60

class MTime():
  DATE_TIME_DISPLAY_LONG_FORMAT = "%Y %m %d %H:%M:%S.%f %z"
  FLOAT_TS = r"[0-9]{10}\.[0-9]{3}"
  INT_TS = r"[0-9]{13}"

  dt: datetime
  s: str
  '''
  datetime in string format
  '''
  sf: str
  '''
  timestamp is an float as string
  '''
  si: str
  '''
  timestamp is an int as string
  '''
  f: float
  '''
  timestamp in float 
  '''
  i: int
  '''
  timestamp in int 
  '''
  z: timezone
  
  def __init__(self, input, tz = pytz.utc):
    if isinstance(input, datetime):
      self.dt = tz.localize(input) if input.tzinfo is None else input
      self.s = self.dt.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
      self.f = self.dt.timestamp() 
      self.i = int(self.f * MS)
      self.sf = str(self.f)
      self.si = str(self.i)
      self.tz = self.dt.tzinfo
    elif isinstance(input, str):
      input = str(input)
      if re.match(self.FLOAT_TS, input):
        self.sf = input
        self.f = float(self.sf)
        self.i = self.f * MS
        self.dt = tz.localize(datetime.fromtimestamp(self.f))
        self.s = self.dt.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
        self.tz = self.dt.tzinfo
      elif re.match(self.INT_TS, input):
        self.si = input
        self.i = int(self.si)
        self.f = self.i / MS
        self.sf = str(self.f)
        self.dt = tz.localize(datetime.fromtimestamp(self.f))
        self.s = self.dt.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
        self.tz = self.dt.tzinfo
      else:
        raise Exception(f"Invalid string datetime format: {input}")  
    elif isinstance(input, float):
      self.f = input
      self.i = self.f * MS
      self.dt = tz.localize(datetime.fromtimestamp(self.f, tz))
      self.s = self.dt.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
      self.fs = str(self.f)
      self.fi = str(self.i)
      self.tz = self.dt.tzinfo
    else:
      raise Exception(f"Invalid type of input: {input}")
  

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
  def request_data(self, symbol:str, interval_sec:int, start_utc: MTime, end_utc:MTime) -> dict:
    pass

  def request_data_wrapper(self, symbol:str, interval_sec:int, start_utc: MTime, end_utc:MTime) -> dict:
    '''
    reises: 
      - Invalid length
      - Invalid start - end date
    '''
    data, url = self.request_data(symbol, interval_sec, start_utc, end_utc)
    must_len_min = int((end_utc.i - start_utc.i) / (interval_sec * 60 * MS))  
    data_len_min = len(data)
    # lengths check
    if(data_len_min == 0 or must_len_min + 1 != data_len_min):
      errorMsg = f"Invalid length, length:{data_len_min}, must_len: {must_len_min}, url: {url}"
      self.logger.error(errorMsg)
      raise Exception(errorMsg)
    # date checks
    data_start_utc = MTime(str(data[0][0]))
    data_end_utc = MTime(str(data[data_len_min-1][0]))

    if((data_start_utc.i != end_utc.i) | (data_end_utc.i != start_utc.i)):
      errMsg = f"Invalid start - end dates in the requested datas {data_start_utc.s} / {start_utc.s}" 
      errMsg = errMsg + f"{data_end_utc.s} / {end_utc.s}"
      self.logger.error(errMsg)
      raise Exception(errMsg)
    return data
    
  def rolling_interval(self, start: MTime, end:MTime, page_sec: int):
    diff = end.i - start.i
    if diff > 0:
      page_ms = page_sec * MS
      remainder = diff % page_ms
      # if dates are too close and diff is less than page_sec
      result = start.i
      yield result
      while result < end.i:
        if(result + page_ms <= end.i):
          result = result + page_ms
          yield result
        else:
          result = result + remainder
          yield result
