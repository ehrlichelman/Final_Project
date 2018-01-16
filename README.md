# Final_Project
Final Project for College
Instructions for network script:

cd /etc/modprobe.d 
vi dummy.conf
edit in file:
options dummy numdummies=4

(dummyX - name of interface, type - name of .conf file)
ip link add dummyX type dummy

(to turn on the dummyX interface)
sudo ifconfig dummyX up 

(viewing tcpdump)
sudo tcpdump -i dummyX
