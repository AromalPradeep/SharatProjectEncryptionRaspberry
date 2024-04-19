import hashlib

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

def aes_encryption(value):
    return value
