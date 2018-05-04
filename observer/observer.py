idToWorker = {}

class publisher:
    def register(self, worker):
        idToWorker[worker._id]=worker

    def notify(self,id,msg):
        idToWorker[id].update(msg)

class worker:
    def __init__(self,id):
        self._id = id
        self._msg = ""

    def register(self,publisher):
        publisher.register(self)

    def update(self,msg):
        self._msg = msg

    def printmsg(self):
        print(self._msg)




publisher = publisher()
worker1 = worker(1)
worker2 = worker(2)
worker3 = worker(3)

worker1.register(publisher)
publisher.notify(1,"test")
worker1.printmsg()

#publisher.register(worker1)
#publisher.register(worker2)
#publisher.register(worker3)

for key in idToWorker:
    print(idToWorker[key])

"""
workers=[]
workers.append(worker1)
workers.append(worker2)
workers.append(worker3)

for worker in workers:
    subject.register(worker)

for worker in workers:
    worker.printmsg()

subject.notify("test")

for worker in workers:
    worker.printmsg()
"""
