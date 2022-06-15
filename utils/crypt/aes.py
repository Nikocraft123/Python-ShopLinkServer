# IMPORTS
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from constants import *
from utils import file
import secrets
import string


# METHODS

# Encrypt bytes
def encrypt_bytes(key: bytes, data: bytes) -> bytes:
    data_size = str(len(data)).zfill(16).encode("utf-8")
    iv = Random.new().read(16)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    output = data_size + iv
    index = 0
    while True:
        chunk = data[index:index + AES_CHUNK_SIZE]
        if len(chunk) == 0:
            break
        if len(chunk) % 16 != 0:
            chunk += b' ' * (16 - (len(chunk) % 16))
        output += cipher.encrypt(chunk)
        index += AES_CHUNK_SIZE
    return output


# Encrypt file
def encrypt_file(key: bytes, file_path: str):
    file_size = str(file.file_size(file_path)).zfill(16).encode("utf-8")
    iv = Random.new().read(16)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    in_file = file.open_binary(file_path, "rb")
    out_file = file.open_binary(f"{file.directory(file_path)}/encrypted-{file.name(file_path)}", "wb")
    out_file.write(file_size)
    out_file.write(iv)
    while True:
        chunk = in_file.read(AES_CHUNK_SIZE)
        if len(chunk) == 0:
            break
        if len(chunk) % 16 != 0:
            chunk += b' ' * (16 - (len(chunk) % 16))
        out_file.write(cipher.encrypt(chunk))
    in_file.close()
    out_file.close()


# Decrypt bytes
def decrypt_bytes(key: bytes, data: bytes) -> bytes:
    output = b''
    data_size = int(data[0:16])
    iv = data[16:32]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    index = 32
    while True:
        chunk = data[index:index + AES_CHUNK_SIZE]
        if len(chunk) == 0:
            break
        output += cipher.decrypt(chunk)
        index += AES_CHUNK_SIZE
    output = output[:data_size]
    return output


# Decrypt file
def decrypt_file(key: bytes, file_path: str):
    in_file = file.open_binary(file_path, "rb")
    out_file = file.open_binary(f"{file.directory(file_path)}/{''.join(file.name(file_path).split('-')[1:])}", "wb")
    file_size = int(in_file.read(16))
    iv = in_file.read(16)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    while True:
        chunk = in_file.read(AES_CHUNK_SIZE)
        if len(chunk) == 0:
            break
        out_file.write(cipher.decrypt(chunk))
    out_file.truncate(file_size)


# Get key
def get_key(password: str) -> bytes:
    hashing = SHA256.new(password.encode("utf-8"))
    return hashing.digest()


# Generate password
def generate_password(length: int = 20) -> str:
    chars = string.digits + string.ascii_letters + string.punctuation
    return "".join(secrets.choice(chars) for _ in range(length))
