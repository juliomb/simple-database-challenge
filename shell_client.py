import sys
from database import MyDB, NoTransactionError, InvalidNameError, COMMANDS, END_COMMAND


ERROR_PREFIX = "***ERROR*** "


def print_error(message):
    print(ERROR_PREFIX + message)


"""
Interpreter
"""


def command_interpreter(line):

    components = line.split(' ')
    if len(components) == 0:
        print_error("Empty command")
        return

    command = components[0]
    if command in COMMANDS:
        try:
            operation = getattr(MyDB, command.lower())
            result = operation(database, *components[1:])
            if result is not None:
                print(result)
        except InvalidNameError:
            print("NULL")
        except NoTransactionError:
            print("NO TRANSACTION")
    else:
        print_error("Unknown command: " + line)


"""
Command line reader
"""


def start_reading():

    line = sys.stdin.readline().strip()

    while line != END_COMMAND:
        command_interpreter(line)
        line = sys.stdin.readline().strip()


# database init and start reading from stdin
database = MyDB()
start_reading()
