import broker_abs
from bybit import ByBit
#import pandas
from broker_abs import DAY_IN_SEC, HOUR_IN_SEC
from broker_abs import MTime
import logging
from logging import config
import yaml
import datetime as dt
from datetime import timedelta
import pytz
import unittest
import pdb

# log init
with open("./logging_config.yaml", "r") as file:
    config = yaml.safe_load(file)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)

# init tz
budapest_tz = pytz.timezone('Europe/Budapest')

start_dt_loc = MTime(dt.datetime(2024, 12, 30, 1, 39, 0, 0, tzinfo=budapest_tz))

bybit = ByBit(logger, budapest_tz)
#df = bybit.request_data_wrapper(broker_abs.Symbols.BTCUSDT, broker_abs.Intervals.MIN1, start_dt_loc, end_dt_loc)

# python3 -W ignore -m unittest testscript.Test.<testmethod>
# python -m unittest testscript.Test.test_rolling_interval
class Test(unittest.TestCase):
    def test_rolling_interval(self):
        # 100 sec diff page size 20
        end = MTime(dt.datetime(2024, 12, 30, 1, 1, 0, 0))
        start = end.dt - timedelta(seconds=100)
        gen_pages = bybit.rolling_interval(MTime(start), end, 20)
        pages = list(gen_pages)
        self.assertEqual(len(pages), (100/20) + 1)
        self.assertTrue(pages[0] == MTime(start).i)
        self.assertTrue(pages[-1] == end.i)

        # 100 sec diff
        end = MTime(dt.datetime(2024, 12, 30, 1, 1, 0, 0))
        start = end.dt - timedelta(seconds=100)
        gen_pages = bybit.rolling_interval(MTime(start), end, 23) # 100 % 23 -> 4 * 23 + 8 -> 5 page
        pages = list(gen_pages)
        self.assertEqual(len(pages) - 1, 5)
        self.assertTrue(pages[0] == MTime(start).i)
        self.assertTrue(pages[-1] == end.i)

