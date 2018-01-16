import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

iface0 = 'dummy0'
iface1 = 'dummy1'


print("Welcome to the ethernet network simulation")
x = Ether(src='61:73:73:68:6f:6c', dst='48:65:6c:6c:6f:20')/ICMP()/("Hello There")
srp(x, iface=iface0)

srp(x, iface=iface1)

#sendp("Hello there dummy0 ", iface='dummy0')
#sendp("Hello there dummy1 ", iface='dummy1')
