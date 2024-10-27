import logging.config
import yaml

# Load YAML configuration
with open("logging_config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Apply logging configuration
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)