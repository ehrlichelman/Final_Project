import pika
import sys
import threading
import time

args = sys.argv[1:]

worker_queue_key = args[0]

def bind(routing_key):
    workers_channel.queue_bind(exchange='workers',
                               queue=workers_queue_name,
                               routing_key=routing_key)

def unbind(routing_key):
    workers_channel.queue_unbind(exchange='workers',
                               queue=workers_queue_name,
                               routing_key=routing_key)

def bind_neighbours(neighbours):
    for neighbour in neighbours:
        bind(neighbour)

def send(routing_key, message):
    workers_channel.basic_publish(exchange='workers',
                          routing_key=routing_key,
                          body=message)


def create_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

def create_channel(connection, exchange_name, exchange_type):
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name,
                         exchange_type=exchange_type)
    return channel

control_connection = create_connection()
control_channel = create_channel(control_connection,'control','topic')

# declare control queue
control_result = control_channel.queue_declare(exclusive=True)
control_queue_name = control_result.method.queue

# bind worker to exchange
control_channel.queue_bind(exchange='control',
                   queue=control_queue_name,
                   routing_key=args[0])

workers_connection = create_connection()
workers_channel = create_channel(workers_connection,'workers','topic')

# channel for worker to worker communication
workers_channel = workers_connection.channel()
workers_channel.exchange_declare(exchange='workers',
                         exchange_type='topic')

# declare workers queue
workers_result = workers_channel.queue_declare(exclusive=True)
workers_queue_name = workers_result.method.queue

# workers_queue_name = workers_result.method.queue






def control_callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    if body.decode() == "send":
        send(args[0],"this is a message from worker to worker")
        print("sned message from: ", args[0])

def workers_callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

control_channel.basic_consume(control_callback,
                      queue=control_queue_name,
                      no_ack=True)


workers_channel.basic_consume(workers_callback,
                      queue=workers_queue_name,
                      no_ack=True)


# user to worker communication consumer thread

binding_keys = args[1:]
print("neighbours:", binding_keys)

bind_neighbours(binding_keys)


def consume_control():
    control_channel.start_consuming()

def consume_workers():
    workers_channel.start_consuming()


control_thread = threading.Thread(target=consume_control)
control_thread.start()

workers_thread = threading.Thread(target=consume_workers)
workers_thread.start()

while True:
    time.sleep(3)
    print("working...")









