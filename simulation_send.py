#!/usr/bin/env python
import pika
import cmd
import logging


logging.basicConfig(filename="debug.log", level=logging.INFO)

class SimulationSend:
    def __init__(self):
        #open("result.log", "w").close()
        #super(SimulationSend, self).__init__()
        #intro = 'Network simulation shell'
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # control exchange between user and workers.
        self.channel.exchange_declare(exchange='control',
                                 exchange_type='topic')
        logging.info('Initializing message broker ')

    def do_send(self, args):
        if len(args) < 2:
            print('invalid syntax')
            return
        else:
            args = args.split()
            routing_key = args[0]
            message = ' '.join(args[1:])
            message = 'send '+message
            print('{} sends to {} : {}'.format(routing_key,args[1],args[2:]))
            logging.info('{} sends to {} : {}'.format(routing_key,args[1],args[2:]))
            self.send(routing_key, message)

    def do_kill(self, node):
        #args = args.split()
        print('killing worker:', node)
        logging.info('killing worker: {}'.format(node))
        self.send(node, 'kill')

    def do_exit(self,args):
        print('now exiting shell')
        self.connection.close()
        print('closing connection')
        return True

    def send(self, routing_key, message):
        self.channel.basic_publish(exchange='control',
                              routing_key=routing_key,
                              body=message)

        print(" [x] Sent %r:%r" % (routing_key, message))
