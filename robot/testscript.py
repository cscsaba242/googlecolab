import getprices_abs
from getprices_abs import Get_Prices_Abstract
import pandas
from backtesting.test import SMA, GOOG
import logging
from logging import config
import yaml

with open("./robot/logging_config.yaml", "r") as file:
    config = yaml.safe_load(file)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)




class Test_Get_Prices(Get_Prices_Abstract):
    def request_data(cls, subclass):
        return super().register(subclass)

test_get_prices = Test_Get_Prices(logger, "Europe/Budapest")

print(test_get_prices.start_time_utc)
print(type(GOOG))

