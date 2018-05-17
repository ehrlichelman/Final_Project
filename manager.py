import pika
import pickle


class Manager(object):
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


class WorkerManager(Manager):
    def __init__(self,mq_server_address, exchange_name, exchange_type, routing_key):
        super(WorkerManager, self).__init__(mq_server_address, exchange_name, exchange_type, routing_key)

    def callback(self,ch, method, properties, body):
        self.executor(pickle.loads(body), self.basic_strategy)

    # bind worker to neighbour queue
    def bind(self,routing_key):
        self.channel.queue_bind(exchange=self.exchange_name,
                                   queue=self.queue_name,
                                   routing_key=routing_key)

    # unbind worker from neighbour queue
    def unbind(self,routing_key):
        self.channel.queue_unbind(exchange=self.exchange_name,
                                   queue=self.queue_name,
                                   routing_key=routing_key)

    # bind worker to a list of neighbours
    def bind_neighbours(self,neighbours):
        for neighbour in neighbours:
            self.bind(neighbour)

    def executor(self, message, strategy=None):
        if strategy:
            strategy(message)
        else:
            print("strategy not set")

    def basic_strategy(self,message):
        if message['destination']==self.routing_key:
            print("received message:")
            print(message)
        else:
            if message['TTL'] > 0:
                print("message is not for me. decreasing TTL and forwarding.")
                message['TTL']-=1
                self.send(self.routing_key, pickle.dumps(message) ,'workers')
            else:
                print("TTL equals zero, dropping message")


class ControlManager(Manager):
    def __init__(self,mq_server_address, exchange_name, exchange_type, routing_key):
        super(ControlManager, self).__init__(mq_server_address, exchange_name, exchange_type, routing_key)
        self.killme = False

        # bind worker to control exchange
        self.channel.queue_bind(exchange=self.exchange_name,
                                queue=self.queue_name,
                                routing_key=self.routing_key)

        self.menudict = {'kill':self.kill,
                         'send':self.sendmsg}

    def executor(self, args, strategy=None):
        if strategy:
            strategy(args)
        else:
            print('Strategy not set')

    def kill(self,args):
        print(args)
        self.killme = True

    def sendmsg(self,args):
        msg = {'source': self.routing_key,
               'destination': args[1],
               'TTL': 3,
               'data': ' '.join(args[1:])}

        print("sending:")
        print(msg)

        msg = pickle.dumps(msg)

        self.send(self.routing_key, msg, 'workers')

    def callback(self,ch, method, properties, body):
        args = body.decode()
        args = args.split()
        self.executor(args,self.menudict[args[0]])


if __name__ == 'main':
    tester = ControlManager("127.0.0.1","test_exchange", "direct", "tester1")
    print(tester)

# add 'static' decorator to executor functions ?
# static method -> can run with class instatination

