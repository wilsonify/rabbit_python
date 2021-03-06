#!/usr/bin/env python
import os
import logging
from logging.config import dictConfig
import pika
import sys

from rabbit_python import config


def callback(ch, method, properties, body):
    logging.info("callback")
    logging.debug("ch = {}".format(ch))
    logging.debug("properties = {}".format(properties))
    print(" [x] %r:%r" % (method.routing_key, body))


def main():
    logging.info("main")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.host, port=config.port)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange="direct_logs",
                             exchange_type="direct")

    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue

    severities = ["info", "error", "warning", "debug"]

    for severity in severities:
        channel.queue_bind(exchange="direct_logs",
                           queue=queue_name,
                           routing_key=severity
                           )

    print(" [*] Waiting for logs. with severity {} To exit press CTRL+C".format(severities))
    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback,
                          auto_ack=True
                          )

    channel.start_consuming()


if __name__ == "__main__":
    os.makedirs(config.logging_dir, exist_ok=True)
    dictConfig(config.logging_config_dict)
    main()
