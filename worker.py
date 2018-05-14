import pika
import sys
import threading
import time
import manager1


args = sys.argv[1:]
#manager.worker_routing_key=args[0]

#manager.run()

#manager = manager.connectionmanager(args[0])

control_manager = manager1.control_manager('localhost', 'control', 'topic', args[0])
worker_manager = manager1.worker_manager('localhost', 'workers', 'topic', args[0])

binding_keys = args[1:]
print("neighbours:", binding_keys)

worker_manager.bind_neighbours(binding_keys)



def consume_control():
    control_manager.channel.start_consuming()

def consume_workers():
    worker_manager.channel.start_consuming()


control_thread = threading.Thread(target=consume_control)
control_thread.start()

workers_thread = threading.Thread(target=consume_workers)
workers_thread.start()

while True:
    time.sleep(3)
    print("working...")
    print(worker_manager.routing_key)






