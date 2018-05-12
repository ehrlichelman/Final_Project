import redis


class AddressDictionary:
    def __init__(self):
        self.redis_db = redis.Redis(host="localhost", port=6379, db=0)
        for x in ['a1', 'b1', 'c1', 'd1', 'e1', 'f1']:
            self.redis_db.sadd('addr_list', x)

    def add_name_addr(self, name):
        addr = self.redis_db.srandmember('addr_list')
        self.redis_db.srem('addr_list', addr)
        self.redis_db.set(name, addr)
        print('selected address: ' + str(self.redis_db.get(name))[2:-1])
        print('remaining addresses: ' + str(self.redis_db.smembers('addr_list')))

    def remove_name(self, name):
        addr = self.redis_db.get(name)
        self.redis_db.delete(name)
        self.redis_db.sadd('addr_list', addr)
        print('remaining addresses: ' + str(self.redis_db.smembers('addr_list')))

    def value_by_name(self, name):
        print('address: ' + str(self.redis_db.get(name))[2:-1])

    def get_all(self):
        count_keys = 0
        for name in self.redis_db.keys():
            if count_keys < len(self.redis_db.keys())-1:
                name = str(name)[2:-1]
                addr = str(self.redis_db.get(name))[2:-1]
                print('name: ' + name + ' address: ' + addr)
            count_keys += 1


if __name__ == '__main__':
    redis_data = AddressDictionary()
    while True:
        user_input = int(input('1 - add, 2 - remove, 3 - find by name, 4 - all: \n'))
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
            redis_data.get_all()
        else:
            break

