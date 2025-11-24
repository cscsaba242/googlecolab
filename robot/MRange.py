from datetime import datetime, timezone
from typing import Iterator, Optional
from MTime import MTime
from Range import Range
from MLogger import MLogger

MS=1000

class MRange(Range, MLogger):
  '''
  start must be < end 
  ..
  ..
  end
  '''
  start: MTime
  end: MTime
  interval_min: int
  '''
  interval in min
  '''
  interval: int
  '''
  interval in ms
  '''
  interval_min: int
  diff_min: int
  diff_interval: int
  diff_interval_min: int
  diff: int
  quotient: int
  remainder: int
  max_per_request: int
  _gen_pages: Optional[Iterator[int]] = None
  pages = []
  len_pages = 0
  logger: MLogger = None

  def __init__(self, start: MTime, end: MTime, interval_min:int, max_per_request = 1000, name = "MRange"):
    super().__init__(name)

    if start.i > end.i:
      raise Exception("start must be < end ")
    self.max_per_request = max_per_request
    self.start = start
    self.end = end
    self.interval_min = interval_min
    self.interval = self.interval_min * 60 * MS
    self.diff = end.i - start.i
    self.diff_min = self.diff / MS / 60
    self.diff_interval = self.diff / self.interval
    self.diff_interval_min = self.diff_min / self.interval_min
    # if start end diff is less than the interval we need
    if (self.diff < self.interval):
      self.len_pages = 0
      self.pages = []
    else: 
      self.calcPages(self.start.i, self.end.i, self.interval, self.max_per_request)

  def setInterval(self, interval_min: int):
    self.interval_min = interval_min
    self.interval = self.interval_min * 60 * MS
    self.diff_interval = self.diff / self.interval
    self.calcPages(self.start.i, self.end.i, self.interval, self.max_per_request)
