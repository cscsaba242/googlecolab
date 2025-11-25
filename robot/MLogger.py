import importlib
import logging
from logging import Logger

import yaml

class MLogger:
    LOG_CONFIG = "./robot/logging_config.yaml"

    def __init__(self, name):
        self.name = name

    def _getLogger(self, config_name: str) -> Logger:
        with open(self.LOG_CONFIG, "r") as file:
            config: dict = yaml.safe_load(file)
            config['handlers']['timed_file']['filename'] = config_name + '.log'
            logging_config = importlib.import_module("logging.config")
            logging_config.dictConfig(config)
            return logging.getLogger(config_name)
