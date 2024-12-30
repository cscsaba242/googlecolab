from abc import ABC, abstractmethod
import pandas
from pandas import DataFrame, DatetimeIndex
from datetime import datetime, timezone
from collections import namedtuple
import asyncio
import pytz
from enum import StrEnum

COLS=['Date','Open','High','Low','Close']

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

  def __init__(self, logger, tz_loc):
    self.logger = logger
    self.tz_loc = tz_loc
    self.start_time_utc = pytz.utc.localize(datetime.now())
    self.start_time_loc = self.start_time_utc.astimezone(self.tz_loc)
    logger.info(f"{self.start_time_utc=} {self.start_time_loc=}")

  @abstractmethod
  async def request_data(self, symbol:str, interval_sec:int, start_utc: datetime, end_utc:datetime) -> dict:
    pass

  def validate_req_data_count(interval_sec: int, start_utc: datetime, end_utc:datetime) -> int:
    diff_start_end = start_utc - end_utc
    result = diff_start_end / interval_sec
    return result 
  
  def convNum(self, dfParam: pandas.Series):
    return (pandas.to_numeric(dfParam)*100).astype(int)
