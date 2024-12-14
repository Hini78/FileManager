from datetime import datetime


class FileSystemObject:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.creation_date = datetime.now()


class File(FileSystemObject):
    def __init__(self, name, file_system, parent=None):
        super().__init__(name, parent)
        self.file_system = file_system
        self.first_block = None

    def write(self, content):
        remaining_content = content
        current_block = None
        while remaining_content:
            free_block = self.file_system.find_free_block()
            if not free_block:
                raise ValueError("No free blocks available")
            if not self.first_block:
                self.first_block = free_block
            if current_block:
                current_block.next_block = free_block
                free_block.prev_block = current_block
            current_block = free_block
            current_block.file = self
            space_available = current_block.size - current_block.used
            current_block.write_data(remaining_content[:space_available])
            remaining_content = remaining_content[space_available:]

    def read(self):
        result = []
        current_block = self.first_block
        while current_block:
            result.append(current_block.read_data())
            current_block = current_block.next_block
        return ''.join(result)

    def delete(self):
        current_block = self.first_block
        while current_block:
            current_block.file = None
            next_block = current_block.next_block
            current_block.clear()
            current_block = next_block
        self.first_block = None



class Directory(FileSystemObject):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def remove_child(self, child):
        self.children.remove(child)

    def deleteDir(self):
        for child in self.children:
            if isinstance(child, Directory):
                child.deleteDir()
            else: child.delete()


    def list_contents(self):
        return ['dir: ' + child.name if isinstance(child, Directory) else 'file: ' + child.name for child in self.children]