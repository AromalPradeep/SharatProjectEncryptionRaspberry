import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import b64encode, b64decode

def aes_encrypt(key, plaintext):
    # Generate a random initialization vector (IV)
    iv = b'\x00' * 16  # You should generate a secure random IV for production use
    
    # Pad the plaintext to be a multiple of 16 bytes
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

    # Create an AES cipher with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    
    # Encrypt the plaintext
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    # Return the IV and ciphertext as Base64 encoded strings
    return b64encode(iv).decode(), b64encode(ciphertext).decode()

def aes_decrypt(key, iv, ciphertext):
    # Decode IV and ciphertext from Base64
    iv = b64decode(iv)
    ciphertext = b64decode(ciphertext)

    # Create an AES cipher with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Decrypt the ciphertext
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the plaintext
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    # Return the plaintext as a string
    return plaintext.decode()

# Example usage:
key = b'ThisIsASecretKey'  # 16, 24, or 32 bytes long
plaintext = "Hello, World!"

iv, ciphertext = aes_encrypt(key, plaintext)
print("IV:", iv)
print("Ciphertext:", ciphertext)

decrypted_plaintext = aes_decrypt(key, iv, ciphertext)
print("Decrypted Plaintext:", decrypted_plaintext)


def md5_hash(text):
    # Convert the text to bytes if it's a string
    if isinstance(text, str):
        text = text.encode('utf-8')

    # Create an MD5 hash object
    md5 = hashlib.md5()

    # Update the hash object with the text
    md5.update(text)

    # Get the hexadecimal representation of the hash
    hashed_text = md5.hexdigest()

    return hashed_text

def file_encrypt(file):
    return

def voice_encrypt():
    return

def key_enccrypt():
    return