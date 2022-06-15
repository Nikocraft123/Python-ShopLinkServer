# IMPORTS
import threading as th
import traceback
from constants import *
from utils import logging
from main import Server


# CLASSES

# Thread
class Thread(th.Thread):

    # CONSTRUCTOR
    def __init__(self, server: Server, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):

        # Initialize the thread
        th.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)

        # Set the server
        self.server = server


    # METHODS

    # Main
    def main(self) -> None:
        pass

    # Run
    def run(self) -> None:

        # Define secure environment
        try:

            # Call the main method of the thread
            self.main()

        # If an unexpected error occurred
        except Exception:

            # Log error
            logging.log_main("--------------------------------------------", LOG_ERROR)
            logging.log_main("", LOG_ERROR)
            logging.log_main("!!! A FATAL ERROR OCCURRED IN THE SERVER !!!", LOG_ERROR)
            logging.log_main("       !!! PLEASE REPORT THIS BUG !!!", LOG_ERROR)
            logging.log_main("", LOG_ERROR)
            logging.log_main("                  THREAD:", LOG_ERROR)
            logging.log_main(" " * (22 - len(self.name) // 2) + self.name, LOG_ERROR)
            logging.log_main("", LOG_ERROR)
            logging.log_main("               ERROR MESSAGE:", LOG_ERROR)
            for line in traceback.format_exc().splitlines():
                logging.log_main(line, LOG_ERROR)
            logging.log_main("", LOG_ERROR)
            logging.log_main("--------------------------------------------", LOG_ERROR)

            # Try to quit the server
            try:
                self.server.exit = True
            except Exception:
                pass
