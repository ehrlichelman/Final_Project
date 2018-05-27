#!/usr/bin/env python
import pika
import cmd


class SimulationSend:
    def __init__(self):
        #super(SimulationSend, self).__init__()
        #intro = 'Network simulation shell'
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # control exchange between user and workers.
        self.channel.exchange_declare(exchange='control',
                                 exchange_type='topic')

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
            self.send(routing_key, message)

    def do_kill(self,args):
        args = args.split()
        print('killing worker:', args[0])
        self.send(args[0], 'kill')

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
