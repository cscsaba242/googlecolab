import logging.config
import yaml

def get_logger(filename:str) -> logging.Logger:
    with open("./logging_config.yaml", "r") as file:
        config = yaml.safe_load(file)
        config["handlers"]["timed_file"]["filename"] = filename
        logging.config.dictConfig(config)
        return logging.getLogger(__name__)
