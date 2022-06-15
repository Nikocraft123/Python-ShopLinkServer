# IMPORTS
import bcrypt
import hashlib
import base64


# FUNCTIONS

# Hash a password
def hash_password(password: str) -> str:

    # Encode the password
    encoded_password = password.encode("utf-8")
    encoded_password = base64.b64encode(hashlib.sha512(encoded_password).digest())

    # Hash the encoded password with a random salt
    salt = bcrypt.gensalt(15)
    hash = bcrypt.hashpw(encoded_password, salt)

    # Return the decoded hash
    return hash.decode("utf-8")


# Check a password
def check_password(password: str, hash: str) -> bool:

    # Encode the string and hash
    encoded_password = password.encode("utf-8")
    encoded_password = base64.b64encode(hashlib.sha512(encoded_password).digest())
    encoded_hash = hash.encode("utf-8")

    # Return, is the password correct for this hash
    return bcrypt.checkpw(encoded_password, encoded_hash)
