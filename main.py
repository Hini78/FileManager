from FileSystem import *
import pickle

# Пример использования
try:
    fs = FileSystem.load('filesystem_dump.pkl')
except FileNotFoundError:
    fs = FileSystem(total_blocks=10, block_size=10)

root_dir = fs.root

# Создание поддиректории и файлов
fs.create_directory("dir1")
fs.create_directory("dir2")
fs.change_directory("dir1")#пошли в dir1 чтобы там создать файл

file1 = fs.create_file("file1.txt", 5)
file1.write("Hello, this is a test for block-based file system.")

# Перемещение между директориями
print(f"Current path: {fs.get_path()}")
fs.change_directory("dir1")
print(f"Current path: {fs.get_path()}")
fs.change_directory("..")
print(f"Current path: {fs.get_path()}")
fs.change_directory("dir2")
print(f"Current path: {fs.get_path()}")

# Чтение файла
fs.change_directory("..")
fs.change_directory("dir1")
print(fs.read_file("file1.txt"))

# Сохранение файловой системы
fs.save('filesystem_dump.pkl')