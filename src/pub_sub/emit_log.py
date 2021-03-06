#!/usr/bin/env python
import os
import logging
from logging.config import dictConfig
import pika
import sys
from rabbit_python import config


def main():
    logging.info("main")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.host, port=config.port)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange="logs", exchange_type="fanout")

    message = " ".join(sys.argv[1:]) or "info: Hello World!"
    channel.basic_publish(exchange="logs", routing_key="", body=message)
    print(" [x] Sent %r" % message)
    connection.close()


if __name__ == "__main__":
    os.makedirs(config.logging_dir, exist_ok=True)
    dictConfig(config.logging_config_dict)
    main()
