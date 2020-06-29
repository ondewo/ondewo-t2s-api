import logging.config

import yaml

with open("utils/logging.yaml") as fd:
    conf = yaml.safe_load(fd)
logging.config.dictConfig(conf["logging"])

logger = logging.getLogger("console")