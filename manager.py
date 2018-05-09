import pika



def create_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

def create_channel(connection, exchange_name, exchange_type):
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name,
                         exchange_type=exchange_type)
    return channel

def control_callback(ch, method, properties, body):
    message = body.decode()
    message = message.split()
    print("im here")
    if message[0] == 'send':

        send(worker_routing_key,' '.join(message[1:]))
        print("sent with routing_key: ", worker_routing_key)
        print("message: ",' '.join(message[1:]))
    else:
        print(" [x] %r:%r" % (method.routing_key, body))


def workers_callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

    message = body.decode()
    message = message.split()

    if message[0] == worker_routing_key: #message is for me:
        print("received a message for me!")
    else:
        print("this message is not for me: ", ' '.join(message))

worker_routing_key=""

def run():
    if __name__ == "manager":

        global workers_channel
        global control_channel
        global workers_queue_name

        control_connection = create_connection()
        control_channel = create_channel(control_connection,'control','topic')

        # declare control queue
        control_result = control_channel.queue_declare(exclusive=True)
        control_queue_name = control_result.method.queue

        # bind worker to exchange
        control_channel.queue_bind(exchange='control',
                       queue=control_queue_name,
                       routing_key=worker_routing_key)

        workers_connection = create_connection()
        workers_channel = create_channel(workers_connection,'workers','topic')

        # channel for worker to worker communication
        workers_channel = workers_connection.channel()
        workers_channel.exchange_declare(exchange='workers',
                                         exchange_type='topic')

        # declare workers queue
        workers_result = workers_channel.queue_declare(exclusive=True)
        workers_queue_name = workers_result.method.queue

        control_channel.basic_consume(control_callback,
                          queue=control_queue_name,
                          no_ack=True)


        workers_channel.basic_consume(workers_callback,
                          queue=workers_queue_name,
                          no_ack=True)

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