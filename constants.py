# IMPORTS

# Builtins
import os


# CONSTANTS

# Credits
NAME = "Shop Link Server"
AUTHOR = "Nikocraft"
VERSION = "Alpha 1.1"

# Logging
LOG_DEBUG = 0
LOG_INFO = 1
LOG_WARNING = 2
LOG_ERROR = 3
LOG_LEVEL_NAMES = {
    LOG_DEBUG: "DEBUG",
    LOG_INFO: "INFO",
    LOG_WARNING: "WARNING",
    LOG_ERROR: "ERROR",
}

# Paths
PATH = os.path.dirname(__file__)
DATA_PATH = f"{PATH}/data"
LIST_PATH = f"{DATA_PATH}/lists"
LOG_PATH = f"{DATA_PATH}/logs"
CONFIG_PATH = f"{DATA_PATH}/configs"
