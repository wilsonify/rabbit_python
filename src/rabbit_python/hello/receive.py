#!/usr/bin/env python
import os
import logging
from logging.config import dictConfig
import pika
from rabbit_python import config


def main():
    logging.info("main")
    logging.info("connecting")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.host, port=config.port))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        logging.debug("callback")
        print(" [x] Received %r" % body)

    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)

    logging.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    os.makedirs(config.logging_dir, exist_ok=True)
    dictConfig(config.logging_config_dict)
    main()
