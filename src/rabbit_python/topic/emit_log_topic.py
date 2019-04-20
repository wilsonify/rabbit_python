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
        pika.ConnectionParameters(host=config.host, port=config.port))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
    message = ' '.join(sys.argv[2:]) or 'Hello World!'
    channel.basic_publish(
        exchange='topic_logs', routing_key=routing_key, body=message)
    print(" [x] Sent %r:%r" % (routing_key, message))
    connection.close()


if __name__ == '__main__':
    os.makedirs(config.logging_dir, exist_ok=True)
    dictConfig(config.logging_config_dict)
    main()
