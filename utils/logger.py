import logging.config

import yaml

with open("config/logging/ondewo_t2s_logging.yaml") as fd:
    conf = yaml.safe_load(fd)
logging.config.dictConfig(conf["logging"])

logger = logging.getLogger("root")
