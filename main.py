# IMPORTS
from typing import IO
import sys
import subprocess as sp
import threading as th
import traceback
from constants import *
from utils import file
from utils import time
from utils import logging
from utils.config import Config
from utils.crypt import rsa


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
        self.control_config = Config(f"{CONFIG_PATH}/control.json")

        # Load the server private and public rsa key
        self.logger.debug("Load server private rsa key ...")
        if file.exist(f"{KEY_PATH}/private_key.pem"):
            self.private_key = rsa.import_key_from_file(f"{KEY_PATH}/private_key.pem")
        else:
            self.logger.warning("No server private rsa key found! Generating new one ...")
            self.private_key = rsa.generate_private_key()
            rsa.export_key_to_file(f"{KEY_PATH}/private_key.pem", self.private_key)
        self.logger.debug("Load server public rsa key ...")
        if file.exist(f"{KEY_PATH}/public_key.pem"):
            self.public_key = rsa.import_key_from_file(f"{KEY_PATH}/public_key.pem")
        else:
            self.logger.warning("No server public rsa key found! Generating new one ...")
            self.public_key = rsa.generate_public_key(self.private_key)
            rsa.export_key_to_file(f"{KEY_PATH}/public_key.pem", self.public_key)

        # Load the control server
        self.logger.debug("Load the control server ...")
        from control import Control
        self.control = Control(self)

        # Define exit and restart variable
        self.exit = False
        self.restart = ""

        # Log info
        self.logger.info("Initialized.")


    # METHODS

    # Run
    def run(self) -> None:

        # Start the control thread
        self.logger.debug("Start the control server ...")
        self.control.start()

        # Wait for control thread started
        while not self.control.started:
            time.sleep(0.01)

        # Check for cancel
        if self.exit:
            self.logger.info("Cancel start and shutdown server, because an error occurred ...")
            self.quit()

        # Log info
        self.logger.info(f"Done! ({time.run_time():.2f}s)")

        # Wait for quit
        while not self.exit:
            time.sleep(0.01)

        # Quit the server
        self.quit(self.restart)

    # Quit
    def quit(self, restart: str = "") -> None:

        # Log info
        self.logger.info("Quit ...")

        # Stop control listener
        self.control.exit = True
        self.control.join()

        # Save configurations
        self.logger.debug("Save configurations ...")
        self.control_config.save()

        # Exit
        exit(self.debug, self.log_file, restart)


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
    debug = "-d" in args

    # Setup directories
    for directory in (LOG_PATH, CONFIG_PATH, SERVER_PATH, KEY_PATH):
        if not file.exist(directory):
            if debug: logging.log_main(f"Create data directory '{directory}' ...", LOG_DEBUG)
            file.make_dir(directory)

    # Clear log directory
    if debug: logging.log_main(f"Clear log directory '{LOG_PATH}' ...", LOG_DEBUG)
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
    if debug: logging.log_main(f"Setup log file at '{log_file_path}' ...", LOG_DEBUG)
    log_file = file.open_text(log_file_path, "w")
    log_file.write(f"{NAME}\n")
    log_file.write(f"{'-' * len(NAME)}\n")
    log_file.write("\n")
    log_file.write(f"Author: {AUTHOR}\n")
    log_file.write(f"Version: {VERSION}\n")
    log_file.write("\n")

    # Define secure environment
    try:

        # Initialize server
        logging.log_main("Initialize server ...", LOG_INFO)
        server = Server(debug, log_file)

        # Run server
        logging.log_main("Run server ...", LOG_INFO)
        server.run()

    # If there is a keyboard interrupt
    except KeyboardInterrupt:

        # Log info
        logging.log_main("Keyboard interrupted! Shutdown server ...", LOG_INFO)

        # Try to quit the server
        try:
            server.quit("")
        except Exception:
            pass

    # If an unexpected error occurred
    except Exception:

        # Log error
        logging.log_main("--------------------------------------------", LOG_ERROR)
        logging.log_main("", LOG_ERROR)
        logging.log_main("!!! A FATAL ERROR OCCURRED IN THE SERVER !!!", LOG_ERROR)
        logging.log_main("       !!! PLEASE REPORT THIS BUG !!!", LOG_ERROR)
        logging.log_main("", LOG_ERROR)
        logging.log_main("                  THREAD:", LOG_ERROR)
        logging.log_main("                Main thread", LOG_ERROR)
        logging.log_main("", LOG_ERROR)
        logging.log_main("               ERROR MESSAGE:", LOG_ERROR)
        for line in traceback.format_exc().splitlines():
            logging.log_main(line, LOG_ERROR)
        logging.log_main("", LOG_ERROR)
        logging.log_main("--------------------------------------------", LOG_ERROR)

        # Try to quit the server
        try:
            server.quit("")
        except Exception:
            pass

# Exit
def exit(debug: bool, log_file: IO, restart: str = "") -> None:

    # Close log file
    if debug: logging.log_main("Close log file ...", LOG_DEBUG)
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
