# IMPORTS
from typing import IO
import sys
import os
import subprocess as sp
import threading as th
from constants import *
from utils import file
from utils import time
from utils import logging


# CLASSES

# Server
class Server:

    # CONSTRUCTOR
    def __init__(self, debug: bool, log_file: IO) -> None:

        # Set debug and log file
        self.debug = debug
        self.log_file = log_file

        # Define the threading lock
        self.lock = th.Lock()

        # Define the logger
        self.logger = logging.Logger(self.lock, f"{NAME} - SERVER", LOG_DEBUG if self.debug else LOG_INFO, self.log_file)

        # Load configurations
        self.logger.debug("Load configurations ...")


    # METHODS

    # Run
    def run(self) -> None:
        self.quit()

    # Quit
    def quit(self, restart: str = "") -> None:

        # Exit
        self.logger.info("Exit ...")
        exit(self.log_file, restart)


# FUNCTIONS

# Main
def main(args: list[str]) -> None:

    # Print header
    print(f"{NAME}")
    print('-' * len(NAME))
    print("")
    print(f"Author: {AUTHOR}")
    print(f"Version: {VERSION}")
    print("")

    # Print info
    logging.log_main("Initialize main ...", LOG_INFO)

    # Read arguments
    logging.log_main("Read arguments ...", LOG_DEBUG)
    debug = "-d" in args

    # Setup directories
    for directory in (LOG_PATH, CONFIG_PATH, LIST_PATH):
        if not file.exist(directory):
            logging.log_main(f"Create data directory '{directory}' ...", LOG_DEBUG)
            file.make_dir(directory)

    # Clear log directory
    logging.log_main(f"Clear log directory '{LOG_PATH}' ...", LOG_DEBUG)
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
    logging.log_main(f"Setup log file at '{log_file_path}' ...", LOG_DEBUG)
    log_file = file.open_text(log_file_path, "w", "utf-8")
    log_file.write(f"{NAME}\n")
    log_file.write(f"{'-' * len(NAME)}\n")
    log_file.write("\n")
    log_file.write(f"Author: {AUTHOR}\n")
    log_file.write(f"Version: {VERSION}\n")
    log_file.write("\n")

    # Initialize server
    logging.log_main("Initialize server ...", LOG_INFO)
    server = Server(debug, log_file)

    # Run server
    logging.log_main("Run server ...", LOG_INFO)
    server.run()


# Exit
def exit(log_file: IO, restart: str = "") -> None:

    # Close log file
    logging.log_main("Close log file ...", LOG_DEBUG)
    log_file.close()

    # Run restart, if available
    if restart != "":
        logging.log_main(f"Restart with '{restart}' ...", LOG_INFO)
        sp.run(restart, shell=True)

    # Exit program
    logging.log_main("Exit ...", LOG_INFO)
    sys.exit(0)


# MAIN
if __name__ == '__main__':

    # Call main function
    main(sys.argv)
