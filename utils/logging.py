# IMPORTS

# Builtins
from typing import IO

# Locals
from constants import *
from utils import time
from utils import file


# CLASSES

# Logger
class Logger:

    # CONSTRUCTOR
    def __init__(self, domain: str, level: int, log_file: IO = None) -> None:

        # Set domain, level and log file
        self.domain = domain
        self.level = level
        self.log_file = log_file


    # METHODS

    # Log



# FUNCTIONS

# Log main
def log_main(message: str, level: int) -> None:
    print(f"[{time.datetime_f1()}] [{NAME} - MAIN] ({LOG_LEVEL_NAMES[level]}) {message}")
