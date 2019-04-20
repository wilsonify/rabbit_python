#!/usr/bin/env python
import os
import logging
from logging.config import dictConfig
import pika
from rabbit_python import config


def callback(ch, method, properties, body):
    logging.info("callback")
    logging.debug("ch = {}".format(ch))
    logging.debug("method = {}".format(method))
    logging.debug("properties = {}".format(properties))
    print(" [x] %r" % body)


def main():
    logging.info("main")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.host,
                                  port=config.port)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange="logs",
                             exchange_type="fanout")

    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange="logs",
                       queue=queue_name)

    print(" [*] Waiting for logs. To exit press CTRL+C")
    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback,
                          auto_ack=True)

    channel.start_consuming()


if __name__ == "__main__":
    os.makedirs(config.logging_dir, exist_ok=True)
    dictConfig(config.logging_config_dict)
    main()
