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
end_loc = MTime(dt.datetime.strptime("2025-03-12 00:00:00", "%Y-%m-%d %H:%M:%S").astimezone(budapest_tz))
start_loc = MTime(end_loc.dt - timedelta(days=1))

class Test(unittest.TestCase):
    
    def testRange(self):
        mrange = MRange(start_loc, end_loc, 1, 10)
        self.assertEqual(mrange.len_pages - 1, 24*60 / 10)

        mrange = MRange(start_loc, end_loc, 1, 20)
        self.assertEqual(mrange.len_pages - 1, 24*60 / 20)

        mrange = MRange(start_loc, end_loc, 15, 20)
        self.assertEqual(mrange.len_pages - 1, 5)
        self.assertEqual(mrange.pages[1][0] == (start_loc.i - 24*60*60*1000)  , True)
