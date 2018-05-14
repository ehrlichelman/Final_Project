import redis
import random


class AddressDictionary:
    def __init__(self):
        self.redis_db = redis.Redis(host="localhost", port=6379, db=0)
        for i in range(100):
            rand_addr = ''.join(random.choice('0123456789ABCDEF') for i in range(3))
            self.redis_db.sadd('addr_list', rand_addr)

    def add_name_addr(self, name):
        addr = self.redis_db.srandmember('addr_list')
        self.redis_db.srem('addr_list', addr)
        self.redis_db.set(name, addr)
        #print('selected address: ' + str(self.redis_db.get(name))[2:-1])
        #print('remaining addresses: ' + str(self.redis_db.smembers('addr_list')))

    def remove_name(self, name):
        addr = self.redis_db.get(name)
        self.redis_db.delete(name)
        self.redis_db.sadd('addr_list', addr)
        #print('remaining addresses: ' + str(self.redis_db.smembers('addr_list')))

    def value_by_name(self, name):
        address = str(self.redis_db.get(name))[2:-1]
        print('address: ' + address)
        return address

    def list_of_addresses(self, l_name=[]):
        #print(str(l_name))
        l_addr = []
        for x in l_name:
            print(self.value_by_name(str(x)))
            l_addr.append(self.value_by_name(x))
        return l_addr

    def get_all(self):
        count_keys = 0
        for name in self.redis_db.keys():
            if count_keys < len(self.redis_db.keys())-1:
                name = str(name)[2:-1]
                addr = str(self.redis_db.get(name))[2:-1]
                print('name: ' + name + ' address: ' + addr)
            count_keys += 1

    def add_node_neighbour(self, node, neighbour):
        self.redis_db.sadd(node, neighbour)
        self.print_node_neighbours(node)

    def print_node_neighbours(self, node):
        neighbours = str(self.redis_db.smembers(node))
        print('Node Address: ' + node + ' Neighbours: ' + neighbours)

    def node_neighbours_list(self, node):
        neighbours_l = str(self.redis_db.smembers(node)).split(",")
        return neighbours_l

    def drop_db(self):
        self.redis_db.flushall()


if __name__ == '__main__':
    redis_data = AddressDictionary()
    while True:
        user_input = int(input('1 - add, 2 - remove, 3 - find by name, 4 - neighbours: \n'))
        if user_input == 1:
            name = input('enter name:')
            redis_data.add_name_addr(name)
        elif user_input == 2:
            name = input('enter name:')
            redis_data.remove_name(name)
        elif user_input == 3:
            name = input('enter name:')
            redis_data.value_by_name(name)
        elif user_input == 4:
            address = input('enter address:')
            redis_data.print_node_neighbours(address[2:-1])
        else:
            break

