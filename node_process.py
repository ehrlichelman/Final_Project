#!/usr/bin/env python
import shlex, subprocess
import sys
import time
import simulation_send


class NodeProcess:
    """starts new worker process for every node"""
    def __init__(self):
        super(NodeProcess, self).__init__()
        self.nodeList = []
        self.sender = simulation_send.SimulationSend()

    def send_msg(self, source, destination, msg, ttl=3):
        args = source+' '+destination+' '+msg
        print(args)
        self.sender.do_send(args)

    def new_node_process(self, node, neighbours_l):
        neighbours_str = ""
        args = ['python3', 'worker.py', node]
        self.nodeList.append(node)
        # add all neighbours to args
        for x in neighbours_l:
            args.append(x)
        subprocess.Popen(args)

    def kill_all_nodes(self):
        for x in self.nodeList:
            self.sender.do_kill(x)
        time.sleep(2)
        self.nodeList = []
        #self.sender.do_exit(' ')


if __name__ == '__main__':
    # this is for test purposes
    manager = NodeProcess()
    manager.new_node_process('worker1', ['worker2', 'worker3'])
    manager.new_node_process('worker2', ['worker1', 'worker4'])
    manager.new_node_process('worker4', ['worker2', 'worker5'])
    manager.new_node_process('worker5', ['worker4'])
    time.sleep(5)
    manager.send_msg('worker1', 'worker5', 'this is a test message')
    manager.kill_all_nodes()
