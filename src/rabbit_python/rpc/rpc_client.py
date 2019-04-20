#!/usr/bin/env python
import os
import logging
from logging.config import dictConfig

import pika
import uuid

from rabbit_python import config


class FibonacciRpcClient(object):

    def __init__(self):
        self.response = 0
        self.corr_id = 0
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.host, port=config.port))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare('', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        logging.info("on_response")
        logging.debug("ch = {}".format(ch))
        logging.debug("method= {}".format(method))
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = 0
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response == 0:
            self.connection.process_data_events()
        return int(self.response)


def main():
    logging.info("main")
    fibonacci_rpc = FibonacciRpcClient()

    print(" [x] Requesting fib(30)")
    response = fibonacci_rpc.call(30)
    print(" [.] Got %r" % response)


if __name__ == '__main__':
    os.makedirs(config.logging_dir, exist_ok=True)
    dictConfig(config.logging_config_dict)
    main()
