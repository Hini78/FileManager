from datetime import datetime
import pickle
from Block import *
from FileSystemObject import *

class FileSystem:
    def __init__(self, total_blocks, block_size):
        self.blocks = [Block(block_size) for _ in range(total_blocks)]
        self.root = Directory("root")
        self.current_directory = self.root

    def find_free_block(self):
        for block in self.blocks:
            if block.file is None:
                return block
        return None

    def create_file(self, name, size):
        file = File(name, size, self, parent=self.current_directory)
        self.current_directory.add_child(file)
        return file

    def delete_file(self, name):
        file = self.get_file(name)
        if file:
            file.delete()
            self.current_directory.remove_child(file)

    def read_file(self, name):
        file = self.get_file(name)
        if file:
            return file.read()
        return None

    def change_directory(self, name):
        if name == "..":
            if self.current_directory.parent is not None:
                self.current_directory = self.current_directory.parent
        else:
            for child in self.current_directory.children:
                if isinstance(child, Directory) and child.name == name:
                    self.current_directory = child
                    return
            print("Directory not found")

    def create_directory(self, name):
        directory = Directory(name, parent=self.current_directory)
        self.current_directory.add_child(directory)
        return directory

    def get_file(self, name):
        for child in self.current_directory.children:
            if isinstance(child, File) and child.name == name:
                return child
        return None

    def get_path(self):
        path = []
        current = self.current_directory
        while current is not None:
            path.append(current.name)
            current = current.parent
        return "/".join(reversed(path))

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        #print(f"File system saved to {filename}")

    def print_all_in_curr_directory(self):
        for name in self.current_directory.list_contents():
            print(name)
    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            fs = pickle.load(f)
        print(f"File system loaded from {filename}")
        return fs


