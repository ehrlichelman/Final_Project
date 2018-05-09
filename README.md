# to do:


immediate goals:  
add manager module  
define control interface and implement it -in work     
test bind\unbind functions after inter-workers communication test is passed  

intermediate goals:  
add message processing in workers_consume  -in work  
manage neighbours list through redis or using control queue  

long term goals:  
add startegy pattern for message processing in workers_consume  

low priority:  
replace if-then-else pattern in sender command menu  
replace if-then-else pattern in worker action menu and add basic functionality  
add error handling  
add logging module  

done:  

* add connection object to prevent multiple threads using the same connection  
* add thread to worker to consume inter-workers communication and test it 
* add arguments to workers for routing_key and neighbours list  

# usage:  

* run user cli interface: python3 send.py  
* set up devices: python3 worker.py '<worker name'> '<neighbour1'> '<neighbour2'> ..  
* send a message to a worker: '<worker name'> '<message'>  
* send a worker a 'send' command: '<worker source'> send '<worker destination'> '<message'>

