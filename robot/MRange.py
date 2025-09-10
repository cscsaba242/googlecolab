from datetime import datetime, timezone
import pytz
import pdb
from MTime import MTime
MS=1000

class MRange():
  '''
  start
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
  _gen_pages = None
  pages = []
  len_pages = 0
  
  def __init__(self, start: MTime, end: MTime, interval_min:int, max_per_request = 1000):
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
      self.calcPages()

  '''
  generate pages between dates based on interval(granularity) * max_data_per_request 
  '''
  def rolling_pages(self):
      if self.diff > 0:
          if self.diff < self.interval:
            raise Exception("Shouldnt be called in this case.")

          page = self.max_per_request * self.interval

          if page > self.diff:
              page = self.diff

          remainder = self.diff % page
          
          for result in range(self.start.utc.i, self.end.utc.i, page):
            yield result
          
          if remainder > 0:
            yield result + remainder
          else:
            yield self.end.utc.i

  def setMax(self, max: int):
    self.max_per_request = max
    self.calcPages()

  def setInterval(self, interval_min: int):
    self.interval_min = interval_min
    self.interval = self.interval_min * 60 * MS
    self.diff_interval = self.diff / self.interval
    self.calcPages()

  def calcPages(self):
    self.pages = []
    self._gen_pages = self.rolling_pages()
    pages = list(self._gen_pages)
    _ = len(pages)
    i = 0
    while i < _ - 1:
      self.pages.append([pages[i], pages[i+1]])
      start = MTime(pages[i])
      end = MTime(pages[i+1])
      print(f"{start.s} - {end.s}")
      i += 1
    self.len_pages = i
