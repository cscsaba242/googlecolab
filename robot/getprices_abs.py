from abc import ABC, abstractmethod
from pandas import DataFrame, DatetimeIndex
from datetime import datetime, timezone
from collections import namedtuple
import asyncio


DTStartEnd = namedtuple("DTStartEnd", ["start","end"])

class GetPrices(ABC):
  timezone = 0 # utc
  logger = None
  payload = {};
  headers = {'User-Agent': 'Mozilla/5.0'}

  def init(self, logger, timezone):
    self.logger = logger
    self.timezone = timezone 

  @abstractmethod
  async def do(self, symbol:str, interval:str, start: datetime, end:datetime) -> DataFrame:
    pass