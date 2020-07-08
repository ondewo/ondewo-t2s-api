import logging.config

import yaml

with open("config/logging/stella-logging.yaml") as fd:
    conf = yaml.safe_load(fd)
logging.config.dictConfig(conf["logging"])

logger = logging.getLogger("root")
