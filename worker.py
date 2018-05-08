import pika
import sys
import threading
import time

# connection object to rabbitmq server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

# channel for user to worker communication
control_channel = connection.channel()
control_channel.exchange_declare(exchange='control',
                         exchange_type='topic')


# declare control queue
control_result = control_channel.queue_declare(exclusive=True)
control_queue_name = control_result.method.queue

# bind worker to exchange
control_channel.queue_bind(exchange='control',
                   queue=control_queue_name,
                   routing_key="worker1")


# channel for worker to worker communication
workers_channel = connection.channel()
workers_channel.exchange_declare(exchange='control',
                         exchange_type='topic')

# declare workers queue
workers_result = workers_channel.queue_declare(exclusive=True)
workers_queue_name = workers_result.method.queue


def control_callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


control_channel.basic_consume(control_callback,
                      queue=control_queue_name,
                      no_ack=True)

# user to worker communication consumer thread


def consume_control():
    control_channel.start_consuming()

# worker to worker communication consumer thread
# def run_workers():


control_thread = threading.Thread(target=consume_control)
control_thread.start()


while True:
    time.sleep(3)
    print("working...")





