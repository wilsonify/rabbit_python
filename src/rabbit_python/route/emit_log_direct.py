#!/usr/bin/env python
import os
from logging.config import dictConfig

import pika
import sys

from rabbit_python import config

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.host, port=config.port))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(
    exchange='direct_logs', routing_key=severity, body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()


def main():
    logging.info("main")
    pass


if __name__ == '__main__':
    os.makedirs(config.logging_dir, exist_ok=True)
    dictConfig(config.logging_config_dict)
    main()
