#!/usr/bin/env python
import os
import pika
import logging
from logging.config import dictConfig
from rabbit_python import config


def main():
    logging.info("main")
    logging.info("connecting to rabbit")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.host, port=config.port)
    )

    channel = connection.channel()

    channel.queue_declare(queue="hello")

    channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
    logging.info(" [x] Sent 'Hello World!'")
    connection.close()


if __name__ == "__main__":
    os.makedirs(config.logging_dir, exist_ok=True)
    dictConfig(config.logging_config_dict)
    main()
