from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def get_key(key):
    return key.zfill(32).encode()

def encrypt_text(text, key):
    key = get_key(key)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(text.encode()) + padder.finalize()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ct

def decrypt_text(encrypted_text, key):
    try:
        key = get_key(key)
        iv = encrypted_text[:16]
        ct = encrypted_text[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()
        padded_data = decryptor.update(ct) + decryptor.finalize()
        pt = unpadder.update(padded_data) + unpadder.finalize()
        return pt.decode()
    except Exception as e:
        return "The key you entered is not used for this file."

def encrypt_image(image_path, key):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    key = get_key(key)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(image_data) + padder.finalize()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    encrypted_image_path = 'encrypted_' + os.path.basename(image_path)
    with open(encrypted_image_path, 'wb') as f:
        f.write(iv + ct)
    return encrypted_image_path

def decrypt_image(encrypted_image_path, key):
    try:
        with open(encrypted_image_path, 'rb') as f:
            encrypted_data = f.read()
        key = get_key(key)
        iv = encrypted_data[:16]
        ct = encrypted_data[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()
        padded_data = decryptor.update(ct) + decryptor.finalize()
        pt = unpadder.update(padded_data) + unpadder.finalize()
        decrypted_image_path = 'decrypted_' + os.path.basename(encrypted_image_path).replace('encrypted_', '')
        with open(decrypted_image_path, 'wb') as f:
            f.write(pt)
        return decrypted_image_path
    except Exception as e:
        return "The key you entered is not used for this file."

def print_banner():
    print("""
    ######################################
    #             +--------+             #
    #             |CrypJack|             #
    #             +--------+             #
    ######################################
    """)

def main():
    print_banner()
    action = input("Do you want to encrypt or decrypt? (e/d): ").strip().lower()
    if action == 'e':
        data_type = input("What do you want to encrypt? (text/image): ").strip().lower()
        key = input("Enter a number as a key: ").strip()
        if data_type == 'text':
            text = input("Enter the text to encrypt: ").strip()
            encrypted_text = encrypt_text(text, key)
            print("Encrypted text:", encrypted_text.hex())
        elif data_type == 'image':
            image_path = input("Enter the image path to encrypt: ").strip()
            encrypted_image_path = encrypt_image(image_path, key)
            print("Encrypted image saved at:", encrypted_image_path)
    elif action == 'd':
        data_type = input("What do you want to decrypt? (text/image): ").strip().lower()
        key = input("Enter the key used for encryption: ").strip()
        if data_type == 'text':
            encrypted_text = bytes.fromhex(input("Enter the encrypted text (in hex): ").strip())
            decrypted_text = decrypt_text(encrypted_text, key)
            print("Decrypted text:", decrypted_text)
        elif data_type == 'image':
            encrypted_image_path = input("Enter the encrypted image path: ").strip()
            decrypted_image_path = decrypt_image(encrypted_image_path, key)
            print("Decrypted image saved at:", decrypted_image_path)
    else:
        print("Invalid action. Please choose 'e' for encrypt or 'd' for decrypt.")

if __name__ == "__main__":
    main()
