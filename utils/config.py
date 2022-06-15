# IMPORTS
import json
from utils import file


# CLASSES

# Configuration
class Config:

    # CONSTRUCTOR
    def __init__(self, path: str):

        # Set the path
        self.path = path

        # Load the data
        self.data = file.load_json(path)


    # METHODS

    # Save
    def save(self):

        # Save the data
        file.save_json(self.path, self.data)
