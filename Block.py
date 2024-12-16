import array


class Block:
    def __init__(self, size):
        self.data = array.array('u', ' ' * size)
        self.next_block = None
        self.prev_block = None
        self.file = None
        self.size = size
        self.used = 0

    def write_data(self, content):
        length = min(len(content), self.size - self.used)
        self.data[self.used:self.used+length] = array.array('u', content[:length])
        self.used += length

    def read_data(self):
        return ''.join(self.data[:self.used])

    def clear(self):
        self.data = array.array('u', ' ' * self.size)
        self.next_block = None
        self.prev_block = None
        self.file = None
        self.used = 0