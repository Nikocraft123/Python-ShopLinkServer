# IMPORTS

# Builtins
from typing import IO
import sys
import os
import subprocess as sp

# Locals
from constants import *
from utils import file
from utils import time
from utils.logging import Logger, log_main

# 3rd party
import keyboard


# CLASSES

# Server
class Server:

    # CONSTRUCTOR
    def __init__(self, debug: bool, log_file: IO) -> None:

        # Set debug and log file
        self.debug = debug
        self.log_file = log_file

        # Load configurations
        #


    # METHODS

    # Run
    def run(self) -> None:
        time.sleep(3)
        self.quit()

    # Quit
    def quit(self, restart: str = "") -> None:

        # Exit
        exit(self.log_file, restart)


# FUNCTIONS

# Main
def main(args: list[str]) -> None:

    # Print header
    print(NAME)
    print('-' * len(NAME))
    print("")
    print(f"Author: {AUTHOR}")
    print(f"Version: {VERSION}")
    print("")

    # Print info
    log_main("Initialize main ...", LOG_INFO)

    # Read arguments
    log_main("Read arguments ...", LOG_DEBUG)
    debug = "-d" in args

    # Setup directories
    for directory in (LOG_PATH, CONFIG_PATH, LIST_PATH):
        if not file.exist(directory):
            log_main(f"Create data directory '{directory}' ...", LOG_DEBUG)
            file.make_dir(directory)

    # Clear log directory
    log_main(f"Clear log directory '{LOG_PATH}' ...", LOG_DEBUG)
    files = []
    for element in file.list_dir(LOG_PATH):
        if file.is_file(f"{LOG_PATH}/{element}"):
            if file.file_type(element) == ".txt" and element.startswith("server_log_"):
                files.append(f"{LOG_PATH}/{element}")
    if len(files) >= 5:
        for index, element in enumerate(files):
            file.delete(element)
            if index >= len(files) - 5:
                break

    # Setup log file
    log_file_path = f"{LOG_PATH}/server_log_{time.datetime_f2()}.txt"
    log_main(f"Setup log file at '{log_file_path}' ...", LOG_DEBUG)
    log_file = open(log_file_path, "w", encoding="utf-8")
    log_file.write(f"{NAME}\n")
    log_file.write(f"{'-' * len(NAME)}\n")
    log_file.write("\n")
    log_file.write(f"Author: {AUTHOR}\n")
    log_file.write(f"Version: {VERSION}\n")
    log_file.write("\n")

    # Initialize server
    log_main("Initialize server ...", LOG_INFO)
    server = Server(debug, log_file)

    # Run server
    log_main("Run server ...", LOG_INFO)
    server.run()


# Exit
def exit(log_file: IO, restart: str = "") -> None:

    # Close log file
    log_main("Close log file ...", LOG_DEBUG)
    log_file.close()

    # Run restart, if available
    if restart != "":
        log_main(f"Restart with '{restart}' ...", LOG_INFO)
        sp.run(restart, shell=True)

    # Exit program
    log_main("Exit ...", LOG_INFO)
    sys.exit(0)


# MAIN
if __name__ == '__main__':

    # Call main function
    main(sys.argv)
