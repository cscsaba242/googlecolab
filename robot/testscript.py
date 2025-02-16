import broker_abs
from bybit import ByBit
from broker_abs import DAY_IN_SEC, HOUR_IN_SEC
from MTime import MTime
from MRange import MRange
import datetime as dt
from datetime import timedelta
import pytz
import unittest
import pdb
import pandas as pd
from pandas import DataFrame

DAY_IN_SEC = 86400
WEEK_IN_SEC = 604800
MONTH_IN_SEC = 2419200

# INIT LOCAL
budapest_tz = pytz.timezone('Europe/Budapest')
now_dt_loc = MTime(dt.datetime.strptime("2025-03-12 00:00:00", "%Y-%m-%d %H:%M:%S").astimezone(budapest_tz))
now_minus1h_dt_loc = MTime(now_dt_loc.dt - timedelta(days=1))

class Test(unittest.TestCase):
    
    def testRange(self):
        mrange = MRange(now_minus1h_dt_loc, now_dt_loc, 1, 10)
        self.assertEqual(mrange.len_pages, 24*60 / 10)

mrange = MRange(now_minus1h_dt_loc, now_dt_loc, 1, 10)
print(mrange.pages)