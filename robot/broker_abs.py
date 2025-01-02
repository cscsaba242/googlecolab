from abc import ABC, abstractmethod
import pandas
from pandas import DataFrame, DatetimeIndex
from datetime import datetime, timezone, timedelta
from collections import namedtuple
import asyncio
import pytz
from enum import StrEnum
import pdb

COLS=['Date','Open','High','Low','Close', 'x', 'y']
DAY_IN_SEC=86400
HOUR_IN_SEC=3600

class Symbols(StrEnum):
    BTCUSDT = "BTCUSDT"
    ETHUSDQ = "ETHUSDQ"

class Intervals(StrEnum):
    MIN1 = "1" 
    MIN3 = "3"
    MIN5 = "5" 
    MIN15 = "15" 
    MIN30 = "30" 

class Broker(ABC):
  tz_loc = None
  logger = None
  payload = {}
  headers = {}
  start_time_utc: datetime
  start_time_loc: datetime
  DATE_TIME_DISPLAY_LONG_FORMAT = "%Y %m %d %H:%M:%S %z"
  DATE_TIME_DISPLAY_SHORT_FORMAT = "%Y %m %d %H:%M:%S"

  def __init__(self, logger, tz_loc):
    self.logger = logger
    self.tz_loc = tz_loc
    self.start_time_utc = pytz.utc.localize(datetime.now())
    self.start_time_loc = self.start_time_utc.astimezone(self.tz_loc)
    logger.info(f"start_utc:{self.dtime_str(self.start_time_utc)} / start_loc:{self.dtime_str(self.start_time_loc)}")

  @abstractmethod
  async def request_data(self, symbol:str, interval_sec:int, start_utc: datetime, end_utc:datetime) -> dict:
    pass

  def validate_req_data_count(self, start: datetime, end:datetime, interval_sec: int, data: dict) -> int:
    diff_end_start:timedelta = end - start
    result = diff_end_start.total_seconds() / interval_sec
    return result
  
  def convNum(self, dfParam: pandas.Series):
    return (pandas.to_numeric(dfParam)).astype(int)
  
  def dtime_str(self, date_time: datetime, long=True):
     if long:
        return date_time.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
     else:
        return date_time.strftime(self.DATE_TIME_DISPLAY_SHORT_FORMAT)
