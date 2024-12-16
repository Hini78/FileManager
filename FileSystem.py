import pickle
from Block import Block
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

    def create_file(self, name):
        file = File(name, self, parent=self.current_directory)
        self.current_directory.add_child(file)
        return file

    def delete_file(self, name):
        file = self.get_file(name)
        if file:
            file.delete()
            self.current_directory.remove_child(file)

    def delete_dir(self, name):
        dir = self.get_dir(name)
        if dir:
            dir.deleteDir()
            self.current_directory.remove_child(dir)

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

    def get_dir(self, name):
        for child in self.current_directory.children:
            if isinstance(child, Directory) and child.name == name:
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

    def copy_file(self, src_path, dest_path):
        src_file = self.get_file_from_path(src_path)
        if not src_file:
            print(f"Source file {src_path} not found")
            return

        dest_dir_path, dest_name = dest_path.rsplit('/', 1)
        dest_dir = self.get_dir_from_path(dest_dir_path)
        if not dest_dir:
            print(f"Destination directory {dest_dir_path} not found")
            return

        dest_file = File(dest_name, self, parent=dest_dir)
        dest_dir.add_child(dest_file)
        data = src_file.read()
        dest_file.write(data)
        print(f"File {src_path} copied to {dest_path}")

    def move_file(self, src_path, dest_path):
        src_file = self.get_file_from_path(src_path)
        if not src_file:
            print(f"Source file {src_path} not found")
            return

        dest_dir_path, dest_name = dest_path.rsplit('/', 1)
        dest_dir = self.get_dir_from_path(dest_dir_path)
        if not dest_dir:
            print(f"Destination directory {dest_dir_path} not found")
            return

        # Copy the file
        self.copy_file(src_path, dest_path)

        # Delete the source file
        src_file.delete()
        src_dir_path, _ = src_path.rsplit('/', 1)
        src_dir = self.get_dir_from_path(src_dir_path)
        src_dir.remove_child(src_file)
        print(f"File {src_path} moved to {dest_path}")

    def get_file_from_path(self, path):
        elements = path.split('/')
        if elements[0] != "root":
            print("Path must start with root")
            return None

        current_dir = self.root
        for elem in elements[1:-1]:
            current_dir = current_dir.get_child(elem)
            if not isinstance(current_dir, Directory):
                return None
        return current_dir.get_child(elements[-1])

    def get_dir_from_path(self, path):
        elements = path.split('/')
        if elements[0] != "root":
            print("Path must start with root")
            return None

        current_dir = self.root
        for elem in elements[1:]:
            current_dir = current_dir.get_child(elem)
            if not isinstance(current_dir, Directory):
                return None
        return current_dir

