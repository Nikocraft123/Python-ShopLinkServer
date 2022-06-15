# IMPORTS
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from utils import file


# METHODS

# Generate private key
def generate_private_key() -> RSA.RsaKey:
    key = RSA.generate(2048)
    return key


# Generate public key
def generate_public_key(private_key: RSA.RsaKey) -> RSA.RsaKey:
    key = private_key.publickey()
    return key


# Import key from file
def import_key_from_file(file_path: str) -> RSA.RsaKey:
    with file.open_binary(file_path, "rb") as f:
        key = RSA.import_key(f.read())
    return key


# Import key from bytes
def import_key_from_bytes(data: bytes) -> RSA.RsaKey:
    key = RSA.import_key(data)
    return key


# Export key to file
def export_key_to_file(file_path: str, key: RSA.RsaKey) -> None:
    with file.open_binary(file_path, "wb") as f:
        f.write(key.export_key("PEM"))


# Export key to bytes
def export_key_to_bytes(key: RSA.RsaKey) -> bytes:
    data = key.export_key("PEM")
    return data


# Encrypt bytes
def encrypt_bytes(public_key: RSA.RsaKey, data: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(public_key)
    encrypt_data = cipher.encrypt(data)
    return encrypt_data


# Decrypt bytes
def decrypt_bytes(private_key: RSA.RsaKey, encrypt_data: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(private_key)
    data = cipher.decrypt(encrypt_data)
    return data
