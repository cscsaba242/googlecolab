from abc import ABC, abstractmethod
from pandas import DataFrame, DatetimeIndex
from datetime import datetime, timezone
from collections import namedtuple
import asyncio


DTStartEnd = namedtuple("DTStartEnd", ["start","end"])

class GetPrices(ABC):
  timezone = 0 # utc
  logger = None
  payload = {}
  headers = {}
  start_time: datetime

  @abstractmethod
  async def get_server_time() -> datetime:
    pass

  async def init(self, logger, timezone):
    self.logger = logger
    self.timezone = timezone 
    start_time: datetime = await get_server_time()
    logger.info(f"{start_time=}")

  @abstractmethod
  async def do(self, symbol:str, interval:str, start: datetime, end:datetime) -> DataFrame:
    pass