#!/usr/bin/env python
import os
import logging
from logging.config import dictConfig
import pika
import sys

from rabbit_python import config

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.host, port=config.port)
)
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)

message = " ".join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange="",
    routing_key="task_queue",
    body=message,
    properties=pika.BasicProperties(delivery_mode=2),  # make message persistent
)
print(" [x] Sent %r" % message)
connection.close()


def main():
    logging.info("main")
    pass


if __name__ == "__main__":
    os.makedirs(config.logging_dir, exist_ok=True)
    dictConfig(config.logging_config_dict)
    main()
