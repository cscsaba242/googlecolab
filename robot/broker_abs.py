from abc import ABC, abstractmethod
from datetime import datetime, timezone
from collections import namedtuple
import pytz
from logging import Logger
import re
import pdb
from typing import Tuple
import asyncio

COLS=['Date','Open','High','Low','Close', 'x', 'y']
DAY_IN_SEC=86400
HOUR_IN_SEC=3600
MS=1000
SEC_IN_MIN=60

class MTime():
  DATE_TIME_DISPLAY_LONG_FORMAT = "%Y-%m-%d %H:%M:%S.%f %z"
  FLOAT_TS = r"[0-9]{10}\.[0-9]{3}"
  INT_TS = r"[0-9]{13}"

  utc: datetime
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
      _ = input
      self.dt = tz.localize(_) if _.tzinfo is None else _.astimezone(tz)
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
        _ = datetime.fromtimestamp(self.f)
        self.dt = tz.localize(_) if _.tzinfo is None else _.astimezone(tz)
        self.s = self.dt.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
        self.tz = self.dt.tzinfo
      elif re.match(self.INT_TS, input):
        self.si = input
        self.i = int(self.si)
        self.f = self.i / MS
        self.sf = str(self.f)
        _ = datetime.fromtimestamp(self.f)
        self.dt = tz.localize(_) if _.tzinfo is None else _.astimezone(tz)
        self.s = self.dt.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
        self.tz = self.dt.tzinfo
      else:
        raise Exception(f"Invalid string datetime format: {input}")  
    elif isinstance(input, float):
      self.f = input
      self.i = self.f * MS
      _ = datetime.fromtimestamp(self.f)
      self.dt = tz.localize(_) if _.tzinfo is None else _.astimezone(tz)
      self.s = self.dt.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
      self.fs = str(self.f)
      self.fi = str(self.i)
      self.tz = self.dt.tzinfo
    elif isinstance(input, int):
      self.i = input
      self.f = self.i / MS
      _ = datetime.fromtimestamp(self.f)
      self.dt = tz.localize(_) if _.tzinfo is None else _.astimezone(tz)
      self.s = self.dt.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
      self.fs = str(self.f)
      self.fi = str(self.i)
      self.tz = self.dt.tzinfo
    else:
      raise Exception(f"Invalid type of input: {input}")
    self.utc = self.dt.astimezone(pytz.utc)

class MRange():
  '''
  end > start
  '''
  start: MTime
  end: MTime
  interval_min: int
  '''
  interval in min
  '''
  interval: int
  diff: int
  quotient: int
  remainder: int

  def __init__(self, start: MTime, end: MTime, interval_min:int):
    if start.i > end.i:
      raise Exception("start must be < end ")
    self.start = start
    self.end = end
    self.interval_min = interval_min
    self.interval = self.interval_min * 60 * MS
    self.diff = end.i - start.i
    # if diff < interval -> raise error 'date diff must be greater than interval'
    if self.diff < self.interval:
      raise Exception("date diff must be greater than interval")
    # if diff % self.intervall != 0 -> raise error 'diff must be multiple of the interval'
    if self.diff % self.interval != 0:
      raise Exception("diff must be multiple of the interval")
    
    
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

  def __init__(self, logger: Logger, tz_loc, max_data_per_request = 0):
    self.logger = logger
    self.tz_loc = tz_loc
    self.max_data_per_request = max_data_per_request
    now = datetime.now()
    self.start_dt_utc = MTime(now)
    self.start_dt_loc = MTime(now, tz_loc)
    self.logger.info(f"start_utc:{self.start_dt_utc.f} / start_loc:{self.start_dt_loc.f}")

  @abstractmethod
  def request_data(self, symbol:str, interval:int, start_utc: MTime, end_utc:MTime) -> Tuple[dict, str]:
    pass

  def request_data_wrapper(self, symbol:str, interval:int, start_utc: MTime, end_utc:MTime) -> Tuple[dict, str]:
    '''
    reises: 
      - Invalid length
      - Invalid start - end date
    '''
    data, url = self.request_data(symbol, interval, start_utc, end_utc) 
    data_len = len(data)
    # lengths check
    if(self.max_data_per_request != data_len):
      errorMsg = f"Invalid length, length:{data_len}, max data per request: {self.max_data_per_request}, url:{url}"
      self.logger.error(errorMsg)
      raise Exception(errorMsg)
    # date checks
    data_start_utc = MTime(str(data[0][0]))
    data_end_utc = MTime(str(data[self.max_data_per_request-1][0]))

    if((data_start_utc.i != end_utc.i) | (data_end_utc.i != start_utc.i)):
      errMsg = f"Invalid start - end dates in the requested datas {data_start_utc.s} / {start_utc.s}" 
      errMsg = errMsg + f"{data_end_utc.s} / {end_utc.s}"
      self.logger.error(errMsg)
      raise Exception(errMsg)
    return data, url
    
'''
generate pages between dates based on interval(granularity) * max_data_per_request 
'''
def rolling_pages(mrange_utc: MRange, max, granularity):
    diff = mrange_utc.diff
    if diff > 0:
        page = max * granularity * 60 * MS
        remainder = diff % page

        for result in range(mrange_utc.start.i, mrange_utc.end.i, page):
          yield result
        
        if remainder > 0:
          yield result + remainder
        else:
          yield mrange_utc.end.i


