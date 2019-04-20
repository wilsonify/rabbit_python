#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost:5672'))

channel = connection.channel()

channel.queue_declare(queue='hello')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_declare(queue='rpc_queue')

channel.exchange_declare(exchange='logs', exchange_type='fanout')
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

connection.close()
