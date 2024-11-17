from abc import ABC, abstractmethod
from pandas import DataFrame, DatetimeIndex
from datetime import datetime, timezone
from collections import namedtuple
import asyncio


DT_from_to_tupple = namedtuple("DTfromto", ["from","to"])

class GetPrices(ABC):
  timezone = timezone.utc

  @abstractmethod
  def init(self, timezone):
    self.timezone = timezone 

  @abstractmethod
  async def do(self, time_frame:str, symbol:str, DT_from: datetime, DT_to:datetime) -> DataFrame:
    pass

  def convertDTime(DTime: datetime) -> DT_from_to_tupple:
    pass