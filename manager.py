import pika
import pickle

class manager(object):
    def __init__(self, mq_server_address, exchange_name, exchange_type, routing_key):

        self.exchange_name = exchange_name
        self.routing_key = routing_key

        # initialize TCP connection to server
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_server_address))

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange_name,
                                      exchange_type=exchange_type)

        # declare queue
        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue


        self.channel.basic_consume(self.callback,
                                   queue=self.queue_name,
                                   no_ack=True)

    def send(self,routing_key,message,exchange_name):
        self.channel.basic_publish(exchange=exchange_name,
                                    routing_key=routing_key,
                                    body=message)


class worker_manager(manager):
    def __init__(self,mq_server_address, exchange_name, exchange_type, routing_key):
        super(worker_manager, self).__init__(mq_server_address, exchange_name, exchange_type, routing_key)


    def callback(self,ch, method, properties, body):

        # print(" [x] %r:%r" % (method.routing_key, body))

        # message = body.decode()
        # message = message.split()

        message = pickle.loads(body)
        print("received:")
        print(message)


        """
        if message[0] == self.routing_key: #message is for me:
            print("received a message for me!")
        else:
            print("this message is not for me: ", ' '.join(message))
        """


    # bind worker to neighbour queue
    def bind(self,routing_key):
        self.channel.queue_bind(exchange=self.exchange_name,
                                   queue=self.queue_name,
                                   routing_key=routing_key)


    # unbind worker from neighbout queue
    def unbind(self,routing_key):
        self.channel.queue_unbind(exchange=self.exchange_name,
                                   queue=self.queue_name,
                                   routing_key=routing_key)


    # bind worker to a list of neighbours
    def bind_neighbours(self,neighbours):
        for neighbour in neighbours:
            self.bind(neighbour)

    """
    def executor(self,message, func=basic_strategy):
        if func is None:
            print("strategy not set")
    """

class control_manager(manager):
    def __init__(self,mq_server_address, exchange_name, exchange_type, routing_key):
        super(control_manager, self).__init__(mq_server_address, exchange_name, exchange_type, routing_key)

        # bind worker to control exchange
        self.channel.queue_bind(exchange=self.exchange_name,
                                queue=self.queue_name,
                                routing_key=self.routing_key)


    def callback(self,ch, method, properties, body):
        message = body.decode()
        message = message.split()
        print("im here")
        if message[0] == 'send':


            # message serialization test

            msg = {'source':self.routing_key,
                   'destination':'dummy_destination',
                   'TTL':10,
                   'data':' '.join(message[1:])}

            print("sending:")
            print(msg)


            msg=pickle.dumps(msg)

            self.send(self.routing_key,msg,'workers')


            """
            self.send(self.routing_key,' '.join(message[1:]),"workers")
            print("sent with routing_key: ", self.routing_key)
            print("message: ",' '.join(message[1:]))
            """


        else:
            print(" [x] %r:%r" % (method.routing_key, body))



if __name__ == 'main':
    tester = control_manager("127.0.0.1","test_exchange", "direct", "tester1")
    print(tester)
