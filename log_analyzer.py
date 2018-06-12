import matplotlib.pyplot as plt
import numpy as np
import re

NETWORK_RUN_TIME = 50
regex = r"(INFO:root).*(received|dropping|forwarding).*"


class LogAnalyzer:
    def __init__(self):
        self.log_list = [0]*NETWORK_RUN_TIME
        self.read_log_file()
        self.create_graph()

    def read_log_file(self):
        f = open("debug.log", "r")
        for line in f:
            str_line = re.match(regex, line)
            if str_line is not None:
                milli_count = str_line.group(0)
                self.log_list[int(milli_count[19:21])] +=1

    def create_graph(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([x for x in range(NETWORK_RUN_TIME)], self.log_list)
        plt.xlabel('time (10 milliseconds)')
        plt.ylabel('messages received')
        plt.title('Network Performance Analysis')
        plt.grid(True)
        plt.savefig("test.png")
        plt.show()


if __name__ == '__main__':
    log_res = LogAnalyzer()

#REGEX for logger:
#(INFO:root).*(received|dropping|forwarding).*
