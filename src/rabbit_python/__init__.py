import logging
from rabbit_python import config

logging.getLogger(__name__).addHandler(logging.NullHandler())

for var in dir(config):
    if not var.startswith("__"):
        logging.info("{} = {}".format(var, config.__dict__[var]))
