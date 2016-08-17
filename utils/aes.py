#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains some algorithms to encrypt and decrypt based on AES256.
"""

# Metadata
__author__ = 'Moises Lodeiro Santiago'
__credits__ = ['Moises Lodeiro-Santiago']
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = 'Moises Lodeiro-Santiago'
__email__ = "moises.lodeiro[at]gmail.com"
__status__ = "Production"

# Python Imports
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):
    """
    AESCipher is a class that uses the Crypto.Cipher AES algorithm
    to encrypt and decrypt the string. Also when encode and decode
    it uses a base64 to pack the data into a string.
    """

    def __init__(self, key):
        """
        __init__ is the constructor of the object

        @param self: Self instance of the object
        @param key: Key that will be used to crypt an decrypt the messages
        """
        self.key = key
        self.BLOCK_SIZE = 16

    def _pad(self, data):
        length = self.BLOCK_SIZE - (len(data) % self.BLOCK_SIZE)
        return data + chr(length) * length

    def _unpad(self, data):
        return data[:-ord(data[-1])]

    def encrypt(self, message):
        """
        Encrypt receives the message and returns the encoded AES256
        result as base64 string.

        @param message: Message to be encoded
        @return: base64 string
        @see base64
        """

        IV = Random.new().read(self.BLOCK_SIZE)
        aes = AES.new(self.key, AES.MODE_CBC, IV)
        return base64.b64encode(IV + aes.encrypt(self._pad(message)))

    def decrypt(self, encrypted):
        """
        Decrypt receives the encrypted message and returns to the original
        message using the inverse operation.

        @param encrypted: Encrypted message to be decrypted
        @return: Original string message
        """

        encrypted = base64.b64decode(encrypted)
        IV = encrypted[:self.BLOCK_SIZE]
        aes = AES.new(self.key, AES.MODE_CBC, IV)
        return self._unpad(aes.decrypt(encrypted[self.BLOCK_SIZE:]))


class JavaAESCipher:
    """
    JavaAESCipher is a class that uses the Crypto.Cipher AES algorithm
    to encrypt and decrypt the string. Also when encode and decode
    it uses a base64 to pack the data into a string.
    """

    def __init__(self, key):
        """
        __init__ is the constructor of the object

        @param self: Self instance of the object
        @param key: Key that will be used to crypt an decrypt the messages
        """
        self.bs = 16
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, message):
        """
        Encrypt receives the message and returns the encoded AES256
        result as base64 string.

        @param message: Message to be encoded
        @return: base64 string
        @see base64
        """

        message = self._pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(message)).decode('utf-8')

    def decrypt(self, enc):
        """
        Decrypt receives the encrypted message and returns to the original
        message using the inverse operation.

        @param encrypted: Encrypted message to be decrypted
        @return: Original string message
        """

        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]



if __name__ == '__main__':

    BLOCK_SIZE = 16
    key = b"1234567890123456"

    def pad(data):
        length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
        return data + chr(length) * length

    def unpad(data):
        return data[:-ord(data[-1])]

    def encrypt(message, passphrase):
        IV = Random.new().read(BLOCK_SIZE)
        aes = AES.new(passphrase, AES.MODE_CBC, IV)
        return base64.b64encode(IV + aes.encrypt(pad(message)))

    def decrypt(encrypted, passphrase):
        encrypted = base64.b64decode(encrypted)
        IV = encrypted[:BLOCK_SIZE]
        aes = AES.new(passphrase, AES.MODE_CBC, IV)
        return unpad(aes.decrypt(encrypted[BLOCK_SIZE:]))

    texto = 'idi9Oqer9ax05E9x/F9jH3bmeg/J1jYQoi6QwWgBd8Gj9KSs+0N/VQxgTq2CA8Zsx5t1cDT01S6vOYatRFiKrOpnnuE4c8Iv/zzFWSSZPk/8elJoYVO+vJe/OuWQh7GYlhCxRvVwCk2hpCI2BOwHCEtPhoEaXIE+lW5x6vskVOsU74QYg1aVlG63wzvquTn17hqpIJfvubGe5/M5yQWpOTMPZKMCfRlVeXT2h+diF3BbiGYbUha/7wq9I62MDmZ4I6ec4EhgPZFoDxWoyk0lMTFHvbw0dBEJJxMTp0fsUl3fLfAuFZ5QcOkqL/pwXn7mg4t2rNfL7HVrwt8GRnPuLl+SKSXtsFxXp7axsZ+MNmJ5Fx+YqN/hiLauEoD7QBXkBI6LuFMxPxu+vk0TD8t8x1T5B+I55hs6KnerDoDUyN8c76/dYomPzhnntJ20HqAiiiuABjDiq0TYsKh6k85mobIS/tTVRBffrKKpEnYDXkn2c0tB12DP+qI3Qt7dm2AKIBo0RvMYzrDHFINzukE5k3WP4PvQDZjukWekumoQrJrIRPgNXEuPNCDkmlWhGFYS6lA3bcRwaF8+7NhLZpDtlTUmH5Afry5lqCkof2RYphRjzGUc92NeMlVmDZ6ZHezYVUyYkkEKfhW/+Z1tMYfBpudHGPd/z9NFmxqN/e8RJUvkr0qT4wdBoOxRbwiZhyQHwveQL1iB8qB0kxKl9Peq5r08ubf4K+0sfkkUF+yM30lLTyNbVrEd8SpFxO2TOAZuSJkG1O7AOLv1SILXLq3yjshJDpoJKJrzFNWySMCpRjkIiEPUiwG3LMu52MMmTfxrWPFC7XYgMXhYmySo68+c3ybwQ6+4uDQemCFOtlOt/wSWuL6WzPBELcaqtSxIlJ94AZzGg4eukJfvwgTPNOyo6C7zSWx2c26AyWKw7pb/0FQrxwMnQ5bYncKjbeDYBGxbfTXojkHNlY70eYoYifhEAcOu6qKWIbCJM2IBt21NjTkBUt93JcDR48B99kXY/yJsSj2YiWThl68Ha4VTgcmdDe3rvyoSW7Q9hwufwg/dBFetgfW6Lh7liSbGu0AHP94IUxEhFjkJjvIoWsCXhmFomgKdPFp6vPrwotu0S0TbN/xt1OIfsgj0uSd6SqUzYurRkPqXhZvIL7VN9HgxCpulFqkiIZRwyfoB45tfezI4lfYwdgJ/IxNyW1l625s8cEgine/YAvm3mhG/JHECrUN5vA=='

    key = b'abcdefghijklmnqw' # 16 bits!!
    print decrypt(texto, key)
