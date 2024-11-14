# Used to hash and salt passwords
import hashlib
import secrets

class PasswordValidator:
    def __init__(self):
        pass

    def validate_password(self, password, hash_entry):
        parts = hash_entry.split(':')
        if(len(parts) != 2): raise ValueError("Invalid hash entry")
        salt = parts[0]
        hash = parts[1]
        return hash == hashlib.sha256((password + salt).encode()).hexdigest()

    # Hashes contain the salt in the format SALT||HASH
    # Salts and hashes are both 256 bits in length
    def generate_password_hash_entry(self, username, password):
        # Generate a strong random number
        salt_randomness = secrets.token_hex(256)
        salt = hashlib.sha256((salt_randomness).encode()).hexdigest()
        hash = hashlib.sha256((password + salt).encode()).hexdigest()
        hash_entry = f"{salt}:{hash}"
        return hash_entry