from FileSystem import *

def print_commands() -> None:
    print(
        "Commands: \n" +
        "1) CreateDir [dirname]\n" +
        "2) CreateFile [filename]\n" +
        "3) WriteFile [filename] [data]\n" +
        "4) DeleteFile [filename]\n" +
        "5) DeleteDir [directory name]\n" +
        "6) ReadFile [filename]\n" +
        "7) Into [dirname] or [..]\n" +
        "8) All\n" +
        "9) copy [source_path] [dest_path]\n" +
        "10) move [source_path] [dest_path]\n" +
        "11) Exit\n"
    )

try:
    fs = FileSystem.load('filesystem_dump.pkl')
except FileNotFoundError:
    fs = FileSystem(total_blocks=10, block_size=10)

cur = fs.root
while True:
    print("Current path: " + fs.get_path())
    print_commands()

    command = input().strip().split(" ")

    if command[0] == "Exit":
        break

    match command[0]:
        case "CreateDir":
            if len(command) != 2:
                print("Invalid command")
            else:
                fs.create_directory(command[1])

        case "CreateFile":
            if len(command) != 2:
                print("Invalid command")
            else:
                fs.create_file(command[1])

        case "WriteFile":
            if len(command) < 3:
                print("Invalid command")
            else:
                file = fs.get_file(command[1])
                if file is None:
                    print("File not found")
                else:
                    file.write(" ".join(command[2:]))

        case "DeleteFile":
            if len(command) != 2:
                print("Invalid command")
            else:
                fs.delete_file(command[1])

        case "DeleteDir":
            if len(command) != 2:
                print("Invalid command")
            else:
                fs.delete_dir(command[1])

        case "ReadFile":
            if len(command) != 2:
                print("Invalid command")
            else:
                file = fs.get_file(command[1])
                if file is None:
                    print("File not found")
                else:
                    print("Data:", file.read())

        case "Into":
            if len(command) != 2:
                print("Invalid command")
            else:
                fs.change_directory(command[1])

        case "All":
            if len(command) != 1:
                print("Invalid command")
            else:
                fs.print_all_in_curr_directory()

        case "copy":
            if len(command) != 3:
                print("Invalid command")
            else:
                fs.copy_file(command[1], command[2])

        case "move":
            if len(command) != 3:
                print("Invalid command")
            else:
                fs.move_file(command[1], command[2])

        case _:
            print("Invalid command")

    fs.save('filesystem_dump.pkl')

fs.save('filesystem_dump.pkl')
