import pika


class connectionmanager:

    # initialize connection to control and worker exchange
    def __init__(self, worker_routing_key):
        #self.workers_channel = None
        #self.control_channel = None
        #self.workers_queue_name = None
        self.worker_routing_key = worker_routing_key

        # control TCP connection to MQ server
        self.control_connection = self.create_connection()
        self.control_channel = self.create_channel(self.control_connection, 'control', 'topic')

        # declare control queue
        control_result = self.control_channel.queue_declare(exclusive=True)
        self.control_queue_name = control_result.method.queue

        # bind worker to control exchange
        self.control_channel.queue_bind(exchange='control',
                                   queue=self.control_queue_name,
                                   routing_key=worker_routing_key)

        # workers TCP connection to MQ server
        self.workers_connection = self.create_connection()
        self.workers_channel = self.create_channel(self.workers_connection, 'workers', 'topic')

        # channel for worker to worker communication
        self.workers_channel = self.workers_connection.channel()
        self.workers_channel.exchange_declare(exchange='workers',
                                         exchange_type='topic')

        # declare workers queue
        self.workers_result = self.workers_channel.queue_declare(exclusive=True)
        self.workers_queue_name = self.workers_result.method.queue

        self.control_channel.basic_consume(self.control_callback,
                                      queue=self.control_queue_name,
                                      no_ack=True)

        self.workers_channel.basic_consume(self.workers_callback,
                                      queue=self.workers_queue_name,
                                      no_ack=True)

    def create_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))


    def create_channel(self,connection, exchange_name, exchange_type):
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange_name,
                             exchange_type=exchange_type)
        return channel


    # callback for user-worker communication
    def control_callback(self,ch, method, properties, body):
        message = body.decode()
        message = message.split()
        print("im here")
        if message[0] == 'send':

            self.send(self.worker_routing_key,' '.join(message[1:]))
            print("sent with routing_key: ", self.worker_routing_key)
            print("message: ",' '.join(message[1:]))
        else:
            print(" [x] %r:%r" % (method.routing_key, body))


    # callback for worker-worker communication
    def workers_callback(self,ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))

        message = body.decode()
        message = message.split()

        if message[0] == self.worker_routing_key: #message is for me:
            print("received a message for me!")
        else:
            print("this message is not for me: ", ' '.join(message))

    # bind worker to neighbour queue
    def bind(self,routing_key):
        self.workers_channel.queue_bind(exchange='workers',
                                   queue=self.workers_queue_name,
                                   routing_key=routing_key)


    # unbind worker from neighbout queue
    def unbind(self,routing_key):
        self.workers_channel.queue_unbind(exchange='workers',
                                   queue=self.workers_queue_name,
                                   routing_key=routing_key)


    # bind worker to a list of neighbours
    def bind_neighbours(self,neighbours):
        for neighbour in neighbours:
            self.bind(neighbour)

    def send(self,routing_key, message):
        self.workers_channel.basic_publish(exchange='workers',
                                    routing_key=routing_key,
                                    body=message)





