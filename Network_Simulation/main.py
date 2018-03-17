#!/usr/bin/python

# list of all network devices
device_l = []


class Device:
    """All network devices available in simulation"""

    # 24 bit addresses
    address = 0
    neighbours_l = []
    packets_l = []


class Packet:
    """Represents packets which are sent between network components"""

    # 3 byte addresses
    src_addr = 0
    dst_addr = 0

    # time to live
    ttl = 5

    next_header = 0

    def __init__(self,src_address,dst_address,p_ttl):
        self.src_addr = src_address
        self.dst_addr = dst_address
        self.ttl = p_ttl


class AccessPoint:
    """Network access point which are used as intersections"""

    ap_addr = 0

    packet_l = []
    neighbours_l = []

    def __init__(self, addr, neighbours = []):
        self.ap_addr = addr
        self.neighbours_l = neighbours

        device_l.append(addr)

        print('AccessPoint created with address = ' +str(self.ap_addr)+ ' and neighbours = ' + str(self.neighbours_l))


def send_packet(src_addr,dst_addr,packet='abcdef'):
    if src_addr in device_l:
        print ("")
    #    while (src_addr != dst_addr):

    #       print ('') #if (device_l[src_addr])

    print('here we send a packet from source to destination')

    print(len(ap2.packet_l))
    ap1.packet_l.append(packet)
    print(str(ap1.packet_l[-1]))

    temp = ap1.packet_l.pop()
    ap2.packet_l.append(temp)

    print(len(ap1.packet_l))

    print(str(ap1.packet_l[-1]))

    print(len(ap2.packet_l))


ap1 = AccessPoint(1,[2])

ap2 = AccessPoint(2,[1])

send_packet(1,2,'hello world')

