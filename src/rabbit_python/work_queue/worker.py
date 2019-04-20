#!/usr/bin/env python
import os
import logging
from logging.config import dictConfig
import pika
import time
from rabbit_python import config

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.host, port=config.port)
)
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    logging.info("callback")
    logging.debug("properties = {}".format(properties))
    print(" [x] Received %r" % body)
    time.sleep(body.count(b"."))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="task_queue", on_message_callback=callback)

channel.start_consuming()


def main():
    pass


if __name__ == "__main__":
    os.makedirs(config.logging_dir, exist_ok=True)
    dictConfig(config.logging_config_dict)
    main()
