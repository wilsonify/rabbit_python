#!/usr/bin/env python
import logging
import os
from logging.config import dictConfig

import pika
from rabbit_python import config


def main():
    logging.info("main")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=config.host,
            port=config.port,
            credentials=config.credentials_rabbit
        )
    )
    channel = connection.channel()

    channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

    routing_key = "kern.critical"
    message = "A critical kernel error"
    channel.basic_publish(exchange="topic_logs", routing_key=routing_key, body=message)
    print(" [x] Sent %r:%r" % (routing_key, message))
    connection.close()


if __name__ == "__main__":
    os.makedirs(config.logging_dir, exist_ok=True)
    dictConfig(config.logging_config_dict)
    main()
