from FileSystem import *


def print_commands() -> None:
    print(
        "Commands: \n" +
        "1)CreateDir [dirname]\n" +
        "2)CreateFile [filename] [size]\n" +
        "3)WriteFile [filename] [data]\n" +
        "4)DeleteFile [filename]\n" +
        "4)ReadFile [filename]\n" +
        "5)Into [dirname] or [..]\n" +
        "6)All\n" +
        "7)Exit\n"
    )




try:
    fs = FileSystem.load('filesystem_dump.pkl')
except FileNotFoundError:
    fs = FileSystem(total_blocks=10, block_size=10)

cur = fs.root
while True:
    print("Current path: " + fs.get_path())
    print_commands()

    command = input()
    if command == "Exit":
        break
    command = command.strip().split(" ")

    match command[0]:
        case "CreateDir":
            if len(command) != 2:
                print("Invalid command")
            else:
                fs.create_directory(command[1])

        case "CreateFile":
            if len(command) != 3:
                print("Invalid command")
            else:
                fs.create_file(command[1], command[2])

        case "WriteFile":
            if len(command) < 3:
                print("Invalid command")
            else:
                file = fs.get_file(command[1])
                if file is None:
                    print("File not found")
                else:
                    file.write("".join(command[2:]))

        case "DeleteFile":
            if len(command) != 2:
                print("Invalid command")
            else:
                fs.delete_file(command[1])
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
                print()
        case _:
            print("Invalid command")
    fs.save('filesystem_dump.pkl')


fs.save('filesystem_dump.pkl')
