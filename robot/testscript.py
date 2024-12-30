import broker_abs
from bybit import ByBit
import pandas
from backtesting.test import SMA, GOOG
import logging
from logging import config
import yaml
import datetime as dt
import pytz

# log init
with open("./robot/logging_config.yaml", "r") as file:
    config = yaml.safe_load(file)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)

# init tz
budapest_tz = pytz.timezone('Europe/Budapest')

start_loc = dt.datetime(2024, 12, 30, 1, 0, 0, 0, budapest_tz)
end_loc = dt.datetime(2024, 12, 30, 2, 0, 0, 0, budapest_tz)

bybit = ByBit(logger, budapest_tz)
df = bybit.request_data(broker_abs.Symbols.BTCUSDT, broker_abs.Intervals.MIN1, start_loc, end_loc)
print(df)

