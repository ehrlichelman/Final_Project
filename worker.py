import sys
import threading
import time
import manager


args = sys.argv[1:]

control_manager = manager.ControlManager('localhost', 'control', 'topic', args[0])
worker_manager = manager.WorkerManager('localhost', 'workers', 'topic', args[0])


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

    if control_manager.killme:
        control_manager.channel.stop_consuming()
        worker_manager.channel.stop_consuming()
        break

    # add block function later...
    # if control_manager.block == True:
    #     worker_manager.channel.stop_consuming()

    print("working...")
    print(worker_manager.routing_key)


print("worker {} terminated".format(args[0]))



