# to do:


immediate goals:  
define control interface and implement it   
test bind\unbind functions after inter-workers communication test is passed  

intermediate goals:  
add message processing in workers_consume  
  
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
