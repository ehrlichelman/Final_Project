import redis
import random
import logging

logging.basicConfig(filename="debug.log", level=logging.DEBUG)


class AddressDictionary:
    def __init__(self):
        logging.debug('Initializing list of 3 bytes addresses: ')
        self.redis_db = redis.Redis(host="localhost", port=6379, db=0)
        for i in range(100):
            rand_addr = ''.join(random.choice('0123456789ABCDEF') for i in range(3))
            self.redis_db.sadd('addr_list', rand_addr)

    def add_name_addr(self, name):
        addr = self.redis_db.srandmember('addr_list')
        self.redis_db.srem('addr_list', addr)
        self.redis_db.set(name, addr)
        logging.debug('New device added, id: {} '
                      'address: {}'.format(name, str(addr)[2:-1]))

    # remove device from network
    def remove_name(self, name):
        addr = self.redis_db.get(name)
        # disconnect node from neighbours
        self.remove_node_neighbours(addr)
        self.redis_db.delete(name)
        self.redis_db.sadd('addr_list', addr)
        logging.debug('Device removed, id: {} '
                      'address: {}'.format(name, str(addr)[2:-1]))

    # returns node address
    def value_by_name(self, name):
        address = str(self.redis_db.get(name))[2:-1]
        print('address: ' + address)
        return address

    # returns list of addresses for nodes
    def list_of_addresses(self, l_name=[]):
        l_addr = []
        for x in l_name:
            print(self.value_by_name(str(x)))
            l_addr.append(self.value_by_name(x))
        return l_addr

    # add node neighbour
    def add_node_neighbour(self, node, neighbour):
        self.redis_db.sadd(node, neighbour)
        self.print_node_neighbours(node)
        logging.debug('Added neighbour for node: {}, neighbour: {} '.format(node, neighbour))

    # remove connecting edge between nodes
    def remove_edge(self, node, neighbour):
        self.redis_db.srem(node, neighbour)
        self.redis_db.srem(neighbour, node)
        logging.debug('Removed neighbour for node: {}, neighbour: {} '.format(node, neighbour))
        logging.debug('Removed neighbour for node: {}, neighbour: {} '.format(neighbour, node))

    # disconnect node from all neighbours
    def remove_node_neighbours(self, node):
        neighbours_l = self.node_neighbours_list(node)
        for x in neighbours_l:
            self.remove_edge(node, x)

    def print_node_neighbours(self, node):
        neighbours = str(self.redis_db.smembers(node)).replace("b'", "").replace("'", "")
        print('Node Address: ' + node + ' Neighbours: ' + neighbours)

    def node_neighbours_list(self, node):
        neighbours_l = str(self.redis_db.smembers(node)).replace("b'", "").replace("'", "").split(",")
        return neighbours_l

    def drop_db(self):
        self.redis_db.flushall()
        logging.debug('Dropped database...')


if __name__ == '__main__':
    redis_data = AddressDictionary()
    while True:
        user_input = int(input('1 - add, 2 - remove, 3 - find by name, 4 - neighbours, 5 - remove neighbour: \n'))
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
        elif user_input == 5:
            node = input('enter node address:')
            neighbour = input('enter neighbour address:')
            redis_data.remove_edge(node, neighbour)
        else:
            redis_data.drop_db()
            break

