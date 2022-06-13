# IMPORTS
from typing import IO
import threading as th
from constants import *
from utils import time


# CLASSES

# Logger
class Logger:

    # CONSTRUCTOR
    def __init__(self, lock: th.Lock, domain: str, level: int, log_file: IO = None) -> None:

        # Set lock, domain, level and log file
        self.lock = lock
        self.domain = domain
        self.level = level
        self.log_file = log_file


    # METHODS

    # Debug
    def debug(self, message: str):
        if self.level <= LOG_DEBUG:
            self._out(f"[{time.datetime_f1()}] [{self.domain}] [{LOG_LEVEL_NAMES[LOG_DEBUG]}] {message}\n")

    # Info
    def info(self, message: str):
        if self.level <= LOG_INFO:
            self._out(f"[{time.datetime_f1()}] [{self.domain}] [{LOG_LEVEL_NAMES[LOG_INFO]}] {message}\n")

    # Warning
    def warning(self, message: str):
        if self.level <= LOG_WARNING:
            self._out(f"[{time.datetime_f1()}] [{self.domain}] [{LOG_LEVEL_NAMES[LOG_WARNING]}] {message}\n")

    # Error
    def error(self, message: str):
        if self.level <= LOG_ERROR:
            self._out(f"[{time.datetime_f1()}] [{self.domain}] [{LOG_LEVEL_NAMES[LOG_ERROR]}] {message}\n")

    # Custom
    def custom(self, text: str):
        self._out(text)

    # Blank line
    def blank_line(self, count: int = 1):
        self._out("\n" * count)

    # Out
    def _out(self, text: str):

        # Lock all other threads
        self.lock.acquire()

        # Print the text to the console
        print(text, end="")

        # Write the text to the log file
        if self.log_file:
            self.log_file.write(text)

        # Release all other threads
        self.lock.release()


# FUNCTIONS

# Log main
def log_main(message: str, level: int) -> None:

    # Print the log to the console
    print(f"[{time.datetime_f1()}] [{NAME} - MAIN] [{LOG_LEVEL_NAMES[level]}] {message}")
