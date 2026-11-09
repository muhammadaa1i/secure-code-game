# Welcome to Secure Code Game Season-1/Level-5!

# This is the last level of our first season, good luck!

import binascii
import secrets
import hashlib
import hmac
import os
import bcrypt

class Random_generator:

    # generates a random token with a CSPRNG (random is predictable)
    def generate_token(self, length=8, alphabet=(
    '0123456789'
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    )):
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    # generates salt with the library, not a hand-made digit string
    def generate_salt(self, rounds=12):
        return bcrypt.gensalt(rounds)

class SHA256_hasher:

    # produces the password hash by combining password + salt because hashing
    def password_hash(self, password, salt):
        password = binascii.hexlify(hashlib.sha256(password.encode()).digest())
        password_hash = bcrypt.hashpw(password, salt)
        return password_hash.decode('ascii')

    # verifies that the hashed password reverses to the plain text version on verification
    def password_verification(self, password, password_hash):
        password = binascii.hexlify(hashlib.sha256(password.encode()).digest())
        password_hash = password_hash.encode('ascii')
        return bcrypt.checkpw(password, password_hash)

class MD5_hasher:

    # name kept for callers; MD5 is broken and unsalted, so this now uses
    # salted, slow scrypt and stores the result as "salt$hash" in hex
    def password_hash(self, password):
        salt = os.urandom(16)
        digest = self._scrypt(password, salt)
        return salt.hex() + '$' + digest.hex()

    def password_verification(self, password, password_hash):
        try:
            salt_hex, digest_hex = password_hash.split('$', 1)
            salt, expected = bytes.fromhex(salt_hex), bytes.fromhex(digest_hex)
        except ValueError:
            return False
        return hmac.compare_digest(self._scrypt(password, salt), expected)

    def _scrypt(self, password, salt):
        return hashlib.scrypt(password.encode(), salt=salt,
                              n=2**14, r=8, p=1, dklen=32)

# secrets come from the environment, never from source code
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
PASSWORD_HASHER = 'SHA256_hasher'


# Contribute new levels to the game in 3 simple steps!
# Read our Contribution Guideline at github.com/skills/secure-code-game/blob/main/CONTRIBUTING.md
