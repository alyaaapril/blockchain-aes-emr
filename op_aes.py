from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
import base64
from base64 import b64decode
import binascii

def decrypt_data(key, ciphertext):
    try:
        iv = base64.b64decode(ciphertext[:24])  # Extract IV and decode from base64
        if len(iv) != 16:
            raise ValueError("Invalid IV length")
    except (binascii.Error, ValueError) as e:
        try:
            iv = base64.b64decode(ciphertext[:24] + '==')  # Add padding manually
            if len(iv) != 16:
                raise ValueError("Invalid IV length")
        except (binascii.Error, ValueError) as e:
            print("Error decoding IV:", e)
            return None

    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(base64.b64decode(ciphertext[24:])), AES.block_size)
        return decrypted_data.decode()  # Convert decrypted data to string
    except (ValueError, binascii.Error) as e:
        print("Error decrypting data:", e)
        return None



# AES encryption and decryption functions
def encrypt_data(key, data):
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
    return cipher.iv + encrypted_data

# Generate a random encryption key
def encryption_key():
    return get_random_bytes(32)  # 256-bit encryption key
