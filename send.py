#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


#control exchange between user and workers.
channel.exchange_declare(exchange='control',
                         exchange_type='topic')




def send(routing_key, message):
    channel.basic_publish(exchange='control',
                          routing_key=routing_key,
                          body=message)

    print(" [x] Sent %r:%r" % (routing_key, message))


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



connection.close()
