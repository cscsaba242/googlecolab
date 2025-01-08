import broker_abs
from bybit import ByBit
import pandas
from broker_abs import DAY_IN_SEC, HOUR_IN_SEC
import logging
from logging import config
import yaml
import datetime as dt
import pytz
import unittest
import pdb

# log init
with open("./robot/logging_config.yaml", "r") as file:
    config = yaml.safe_load(file)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)

# init tz
budapest_tz = pytz.timezone('Europe/Budapest')

start_loc = budapest_tz.localize(dt.datetime(2024, 12, 30, 1, 39, 0, 0))
end_loc = budapest_tz.localize(dt.datetime(2024, 12, 30, 1, 42, 0, 0))

bybit = ByBit(logger, budapest_tz)
df = bybit.request_data_wrapper(broker_abs.Symbols.BTCUSDT, 60, start_loc, end_loc)

# python3 -W ignore -m unittest testscript.Test.<testmethod>
class Test(unittest.TestCase):
    def test_vrq(self):
        start = dt.datetime(2024, 12, 30, 1, 0, 0, 0)
        end = dt.datetime(2024, 12, 30, 2, 0, 0, 0)
        result = bybit.validate_req_data_count(start, end, HOUR_IN_SEC)
        self.assertEqual(result, 1)
        start = dt.datetime(2024, 12, 30, 0, 0, 0, 0)
        end = dt.datetime(2024, 12, 31, 0, 0, 0, 0)
        result = bybit.validate_req_data_count(start, end, DAY_IN_SEC)
        self.assertEqual(result, 1)

    def test_rolling_interval(self):
        # 1 min diff
        start = dt.datetime(2024, 12, 30, 1, 1, 0, 0)
        end = dt.datetime(2024, 12, 30, 2, 2, 0, 0)
        result = bybit.rolling_interval(start, end, 88)
        print(result)
        self.assertEqual(result, 60)


