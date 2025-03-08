import broker_abs
from bybit import ByBit
from broker_abs import DAY_IN_SEC, HOUR_IN_SEC
from MTime import MTime
from MRange import MRange
import datetime as dt
from datetime import timedelta, datetime
import pytz
import unittest
import pdb
import pandas as pd
from pandas import DataFrame

budapest_tz = pytz.timezone('Europe/Budapest')
end_loc = MTime(datetime.now(budapest_tz))
start_loc = MTime(end_loc.dt - timedelta(hours=1), budapest_tz)

bybit = ByBit(budapest_tz, 1000)
bybit.run("BTCUSD", MRange(MTime(start_loc.dt), MTime(end_loc.dt), 15, 2))

# data = bybit.getDataAsDataFrame("BTCUSD", MRange(MTime(start_loc.dt), MTime(end_loc.dt), 15, 2))
print("end")

class Test(unittest.TestCase):
    budapest_tz = pytz.timezone('Europe/Budapest')
    end_loc = MTime(dt.datetime.strptime("2025-02-17 14:00:00.000000 +0100", MTime.DATE_TIME_DISPLAY_LONG_FORMAT), budapest_tz)
    start_loc = MTime(end_loc.dt - timedelta(days=1), budapest_tz)
    
    def testRange(self):
        self.assertEqual(self.end_loc.s, "2025-02-17 14:00:00.000000 +0100")
        self.assertEqual(self.end_loc.utc.s, "2025-02-17 13:00:00.000000 +0000")
        self.assertEqual(self.start_loc.s, "2025-02-16 14:00:00.000000 +0100")
        self.assertEqual(self.start_loc.utc.s, "2025-02-16 13:00:00.000000 +0000")

        mrange = MRange(self.start_loc, self.end_loc, 1, 10)
        self.assertEqual(mrange.len_pages, 24*60 / 10)

        mrange = MRange(self.start_loc, self.end_loc, 1, 20)
        self.assertEqual(mrange.len_pages, 24*60 / 20)

        mrange = MRange(self.start_loc, self.end_loc, 15, 20)
        self.assertEqual(mrange.len_pages, 5)
        
        start = MTime(mrange.pages[0][0])
        self.assertEqual(start.s, "2025-02-16 13:00:00.000000 +0000")
        end = MTime(mrange.pages[4][1])
        self.assertEqual(end.s, "2025-02-17 13:00:00.000000 +0000")
        
        # interval bigger than time diff
        mrange = MRange(self.start_loc, self.end_loc, 24*60 + 1, 20)
        self.assertEqual(mrange.len_pages, 0)
