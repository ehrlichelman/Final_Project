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
    print(type(inputx))
    inputx = inputx.split()

    if inputx[0] == "quit":
        break
    if inputx[0] == "send":
        routing_key = inputx[1]
        msg = inputx[2]
        send(routing_key, msg)



connection.close()