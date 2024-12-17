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
  start_time: datetime

  async def init(self, logger, tz):
    self.logger = logger
    self.timezone = pytz.timezone("Europe/Budapest")
    self.start_time_utc = pytz.utc(datetime.now())
    self.start_time_loc = self.timezone.localize(self.start_time_utc)
    logger.info(f"{self.start_time_utc=} {self.start_time_loc=}")

  @abstractmethod
  async def request_data(self, symbol:str, interval_sec:int, start_utc: datetime, end_utc:datetime) -> DataFrame:
    pass

  def validate_req_data_count(interval_sec: int, start_utc: datetime, end_utc:datetime) -> int:
    diff_start_end = start_utc - end_utc
    result = diff_start_end / interval_sec
    return result 