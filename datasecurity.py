import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

# Encrypt & Decrypt info by AES
class DataSecurity:
    key = b"\x94\x96w\xdc\xaa\xfd\xb8R\xf7F\\\xa8LiO\x86\xe4'\xb3q>\xb5\x7f\x07/\xb9a\xb5\x7f\x15\x84\x10"

    # Encrypt password by AES
    @classmethod
    def encrypt_password(cls,strpassword):
        # Get IV
        iv = os.urandom(16)
        # AES encryptor
        cipher = Cipher(algorithms.AES(cls.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        # Padding to 16 bytes required by AES
        padding_length = 16 - len(strpassword) % 16
        padded_password = strpassword + chr(padding_length) * padding_length
        encrypted_password = encryptor.update(padded_password.encode('utf-8')) + encryptor.finalize()
        strpwd = base64.b64encode(iv + encrypted_password).decode('utf-8')
        return strpwd

    # Decrypt password by AES
    @classmethod
    def decrypt_password(cls,strpwd):
        # Get IV from encrypted_data
        encrypted_data=base64.b64decode(strpwd)
        iv = encrypted_data[:16]
        encrypted_password = encrypted_data[16:]
        # AES decryptor
        cipher = Cipher(algorithms.AES(cls.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_password = decryptor.update(encrypted_password) + decryptor.finalize()
        # Remove padding
        padding_length = decrypted_password[-1]
        decrypted_password = decrypted_password[:-padding_length]
        return decrypted_password.decode('utf-8')
