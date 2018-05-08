#!/usr/bin/env python
import pika
import sys
import threading
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


"""
    routing_key = "worker2"
    message = "this is a message from worker2"
    channel.basic_publish(exchange='topic_logs',
                          routing_key=routing_key,
                          body=message)
    print(" [x] Sent %r:%r" % (routing_key, message))
"""

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

def consume_thread():
    channel.start_consuming()

myThread = threading.Thread(target=consume_thread)
myThread.start()

while True:
    time.sleep(3)
    print("-")

