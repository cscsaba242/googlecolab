from datetime import datetime, timezone
import pytz
import re
from logging import Logger
from MLogger import MLogger

MS=1000
class MTime(MLogger):
  DATE_TIME_DISPLAY_LONG_FORMAT = "%Y-%m-%d %H:%M:%S.%f %z"
  DATE_TIME_DISPLAY_SHORT_FORMAT = "%Y-%m-%d"
  FLOAT_TS = r"[0-9]{10}\.[0-9]{3}"
  INT_TS = r"[0-9]{13}"
  logger: Logger = None

  utc: datetime
  dt: datetime
  sYmdHMS: str
  '''
  datetime in string format %Y-%m-%d %H:%M:%S" without timezone information
  '''
  
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
  tz: timezone
  '''
  timezone
  '''

  def __init__(self, input, tz = pytz.utc):
    self.utc: MTime = None
    if isinstance(input, datetime):
      _ = input
      self.dt = tz.localize(_) if _.tzinfo is None else _.astimezone(tz)
      self.dt.replace(microsecond=0)
      self.f = self.dt.timestamp() 
      self.i = int(self.f * MS)
      self.sf = str(self.f)
      self.si = str(self.i)
      self._generateCommons(self.dt)
    elif isinstance(input, str):
      input = str(input)
      # if the input string is FLOAT format
      if re.match(self.FLOAT_TS, input):
        self.sf = input
        self.f = float(self.sf)
        self.i = self.f * MS
        _ = datetime.fromtimestamp(self.f)
        self.dt = tz.localize(_) if _.tzinfo is None else _.astimezone(tz)
        self._generateCommons(self.dt)
      # if the input string is in INT format
      elif re.match(self.INT_TS, input):
        self.si = input
        self.i = int(self.si)
        self.f = self.i / MS
        self.sf = str(self.f)
        _ = datetime.fromtimestamp(self.f)
        self.dt = tz.localize(_) if _.tzinfo is None else _.astimezone(tz)
        self._generateCommons(self.dt)
      else:
        raise Exception(f"Invalid string datetime format: {input}")  
    elif isinstance(input, float):
      self.f = input
      self.i = self.f * MS
      if tz == pytz.utc:
        _ = datetime.utcfromtimestamp(self.f)
        if _.tzinfo is None:
          _ = _.replace(tzinfo=pytz.utc)
      else:
        _ = datetime.fromtimestamp(self.f)
        _ = tz.localize(_) if _.tzinfo is None else _.astimezone(tz)
      self.dt = _
      self.fs = str(self.f)
      self.fi = str(self.i)
      self._generateCommons(self.dt)
    elif isinstance(input, int):
      self.i = input
      self.f = self.i / MS
      if tz == pytz.utc:
        _ = datetime.utcfromtimestamp(self.f)
        if _.tzinfo is None:
          _ = _.replace(tzinfo=pytz.utc)
      else:
        _ = datetime.fromtimestamp(self.f)
        _ = tz.localize(_) if _.tzinfo is None else _.astimezone(tz)
      self.dt = _
      self.fs = str(self.f)
      self.fi = str(self.i)
      self._generateCommons(self.dt)
    else:
      raise Exception(f"Invalid type of input: {input}")

  def _generateCommons(self, dt: datetime):
      self.tz = self.dt.tzinfo
      self.s = self.dt.strftime(self.DATE_TIME_DISPLAY_LONG_FORMAT)
      self.sYmdHMS = self.dt.strftime(self.DATE_TIME_DISPLAY_SHORT_FORMAT)

      if(self.tz != pytz.utc):
        self.utc = MTime(self.dt)
      else: 
        self.utc = self

