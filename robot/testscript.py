import broker_abs
from bybit import ByBit
from broker_abs import DAY_IN_SEC, HOUR_IN_SEC
from broker_abs import MTime, MRange, rolling_pages
import logging
from logging import config
import yaml
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
MS = 1000

with open("./robot/logging_config.yaml", "r") as file:
    config = yaml.safe_load(file)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)

# INIT LOCAL
budapest_tz = pytz.timezone('Europe/Budapest')
end_dt_loc = MTime(dt.datetime.now().astimezone(budapest_tz))
start_dt_loc = MTime(end_dt_loc.dt - timedelta(days=1))

# UTC
start_dt_utc = MTime(start_dt_loc.dt)
end_dt_utc = MTime(end_dt_loc.dt)

mrange_utc = MRange(start_dt_utc, end_dt_utc, 15)
print("finished")


class Test(unittest.TestCase):
    budapest_tz = pytz.timezone('Europe/Budapest')
    end_dt_loc: MTime
    start_dt_loc: MTime

    def testing_rolling_pages1(self):
        start = dt.datetime.strptime("2024-12-01 02:00:00.000000 +00:00","%Y-%m-%d %H:%M:%S.%f %z")
        end = start - timedelta(hours=1)
        startMtime = MTime(start)
        endMtime = MTime(end) 

        mrange = MRange(endMtime, startMtime, 15)
        mrange_gen = rolling_pages(mrange, 1, mrange.interval_min)
        result = list(mrange_gen)

        for r in result:
            mtime = MTime(r)
            print(mtime.s)

    def testing_rolling_pages2(self):
        start = dt.datetime.strptime("2024-12-01 02:00:00.000000 +00:00","%Y-%m-%d %H:%M:%S.%f %z")
        end = start - timedelta(hours=1)
        startMtime = MTime(start)
        endMtime = MTime(end) 

        mrange = MRange(endMtime, startMtime, 1)
        mrange_gen = rolling_pages(mrange, 10, mrange.interval_min)
        result = list(mrange_gen)

        for r in result:
            mtime = MTime(r)
            print(mtime.s)

t = Test()
t.testing_rolling_pages2()