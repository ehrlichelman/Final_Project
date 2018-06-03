#!/usr/bin/env python
import pika
import cmd


class SimulationShell(cmd.Cmd):
    intro = 'Network simulation shell'

    def do_send(self, args):
        print(args)
        if len(args) < 3:
            print('invalid syntax')
            return
        else:
            args = args.split()
            routing_key = args[0]
            message = ' '.join(args[1:])
            message = 'send '+message
            print('{} sends to {} : {}'.format(routing_key,args[1],args[2:]))
            send(routing_key, message)

    def do_kill(self,args):
        args = args.split()
        print('killing worker:', args[0])
        send(args[0], 'kill')

    def do_exit(self,args):
        print('now exiting shell')
        return True


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


# control exchange between user and workers.
channel.exchange_declare(exchange='control',
                         exchange_type='topic')


def send(routing_key, message):
        channel.basic_publish(exchange='control',
                              routing_key=routing_key,
                              body=message)

        print(" [x] Sent %r:%r" % (routing_key, message))


SimulationShell().cmdloop()

"""
while True:

    inputx = input(">>>: ")
    inputx = inputx.split()
    print(inputx)
    if inputx[0] == "quit":
        break

    #message format: <worker_source> send <worker_destination> <message>

    routing_key = inputx[0]
    msg = ' '.join(inputx[1:])
    print(msg)
    send(routing_key, msg)
"""

print('closing connection')
connection.close()
