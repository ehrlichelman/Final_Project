import pika
import sys
import threading
import time
import manager

args = sys.argv[1:]
manager.worker_routing_key=args[0]

manager.run()

binding_keys = args[1:]
print("neighbours:", binding_keys)

manager.bind_neighbours(binding_keys)


def consume_control():
    manager.control_channel.start_consuming()

def consume_workers():
    manager.workers_channel.start_consuming()


control_thread = threading.Thread(target=consume_control)
control_thread.start()

workers_thread = threading.Thread(target=consume_workers)
workers_thread.start()

while True:
    time.sleep(3)
    print("working...")
    print(manager.worker_routing_key)






