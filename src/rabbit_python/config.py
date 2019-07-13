import logging
import os

import pika

host = "10.152.183.148"
port = 5672

username_rabbit = "user"
password_rabbit = "pzUxWgF6oN"

credentials_rabbit = pika.PlainCredentials(username_rabbit, password_rabbit)

logging_dir = "logs"

logging_config_dict = dict(
    version=1,
    formatters={
        "simple": {"format": """%(asctime)s %(name)-12s %(levelname)-8s %(message)s"""}
    },
    handlers={
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(logging_dir, "rabbit_python.log"),
            "formatter": "simple",
        },
    },
    root={"handlers": ["console", "file"], "level": logging.DEBUG},
)
