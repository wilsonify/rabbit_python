#!/usr/bin/env python
import logging
import os
import sys
from logging.config import dictConfig

import pika
from rabbit_python import config


def callback(ch, method, properties, body):
    logging.info("callback")
    logging.debug("properties = {}".format(properties))
    logging.debug("ch = {}".format(ch))

    print(" [x] %r:%r" % (method.routing_key, body))


def main():
    logging.info("main")


    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            credentials=credentials_rabbit,
            host=config.host,
            port=config.port
        )
    )
    channel = connection.channel()

    channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue

    binding_keys = ["#", "kern.*", "*.critical"]
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange="topic_logs", queue=queue_name, routing_key=binding_key
        )

    print(" [*] Waiting for logs. To exit press CTRL+C")
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == "__main__":
    os.makedirs(config.logging_dir, exist_ok=True)
    dictConfig(config.logging_config_dict)
    main()
