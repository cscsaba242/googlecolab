import broker_abs
from bybit import ByBit
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

# init tz
budapest_tz = pytz.timezone('Europe/Budapest')

start_dt_loc = MTime(dt.datetime(2024, 1, 1, 0, 0, 0, 0, tzinfo=budapest_tz))
end_dt_loc = MTime(dt.datetime.now().astimezone(budapest_tz))

bybit = ByBit(logger, budapest_tz)

df = DataFrame()

page_ms = 9_090 * 15 * 60 * 1000
pages = bybit.rolling_pages(start_dt_loc, end_dt_loc, page_ms)
page_list = list(pages)
for page in page_list: 
    start = MTime(page)
    end = MTime(start.i + page_ms)
    df_page = bybit.request_data_wrapper(broker_abs.Symbols.BTCUSDT, 15, start, end)
    df = pd.concat([df, df_page], ignore_index=True)

print("finished")


#python3 -W ignore -m unittest testscript.Test.<testmethod>
#python -m unittest testscript.Test.test_rolling_interval


class Test(unittest.TestCase):
    pass