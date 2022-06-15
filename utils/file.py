# IMPORTS

# Builtins
from typing import IO
import os
import json


# FUNCTIONS

# Open text file
def open_text(path: str, mode: str, encoding: str = "utf-8") -> IO:
    if not exist(os.path.dirname(path)):
        make_dir(os.path.dirname(path))
    try:
        return open(path, mode, encoding=encoding)
    except OSError:
        open(path, "x", encoding=encoding)
        return open_text(path, mode, encoding)


# Open binary file
def open_binary(path: str, mode: str) -> IO:
    if not exist(os.path.dirname(path)):
        make_dir(os.path.dirname(path))
    try:
        return open(path, mode)
    except OSError:
        open(path, "xb")
        open_binary(path, mode)


# Load json
def load_json(path: str) -> dict:
    file = open_text(path, "r")
    try:
        data = json.load(file)
    except json.JSONDecodeError:
        data = {}
    file.close()
    return data


# Save json
def save_json(path: str, data: dict) -> None:
    file = open_text(path, "w")
    json.dump(data, file, indent=4, separators=(", ", ": "))
    file.close()


# Delete
def delete(path: str) -> None:
    os.remove(path)


# Rename
def rename(old_path: str, new_path: str) -> None:
    os.rename(old_path, new_path)


# Exist
def exist(path: str) -> bool:
    return os.path.exists(path)


# Make directory
def make_dir(path: str) -> None:
    os.makedirs(path)


# Remove directory
def remove_dir(path: str) -> None:
    os.removedirs(path)


# List directory
def list_dir(path: str)-> list[str]:
    return os.listdir(path)


# File type
def file_type(path: str) -> str:
    return os.path.splitext(path)[1]


# Is file
def is_file(path: str) -> bool:
    return os.path.isfile(path)


# Is directory
def is_dir(path: str) -> bool:
    return os.path.isdir(path)


# Full path
def full_path(path: str) -> str:
    return os.path.abspath(path)


# Base name
def name(path: str) -> str:
    return os.path.basename(path)


# Directory
def directory(path: str) -> str:
    return os.path.dirname(path)


# File size
def file_size(path: str) -> int:
    return os.path.getsize(path)
