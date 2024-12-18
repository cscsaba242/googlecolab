from abc import ABC, abstractmethod
from pandas import DataFrame, DatetimeIndex
from datetime import datetime, timezone
from collections import namedtuple
import asyncio
import pytz

class Get_Prices_Abstract(ABC):
  timezone = 0 # utc
  logger = None
  payload = {}
  headers = {}
  start_time_utc: datetime
  start_time_loc: datetime

  def __init__(self, logger, tz):
    self.logger = logger
    self.timezone = pytz.timezone(tz)
    self.start_time_utc = pytz.utc.localize(datetime.now())
    self.start_time_loc = self.start_time_utc.astimezone(self.timezone)
    logger.info(f"{self.start_time_utc=} {self.start_time_loc=}")

  @abstractmethod
  async def request_data(self, symbol:str, interval_sec:int, start_utc: datetime, end_utc:datetime) -> dict:
    pass

  def validate_req_data_count(interval_sec: int, start_utc: datetime, end_utc:datetime) -> int:
    diff_start_end = start_utc - end_utc
    result = diff_start_end / interval_sec
    return result 