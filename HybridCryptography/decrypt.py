from Cryptodome.Cipher import AES, DES3
from Cryptodome.Util.Padding import unpad
import base64
from Cryptodome.Cipher import ARC2
from Cryptodome import Random
from .import tools
import os


def AESAlgo(filename, key):
    source_file = 'encrypt/' + filename
    target_file = 'decrypt/' + filename
    c_file = open(source_file, "rb")
    iv = c_file.read(16)
    ciphertext = c_file.read()
    p_file = open(target_file, "wb")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    p_file.write(plaintext)
    c_file.close()
    p_file.close()


def DESAlgo(filename, key):
    source_file = 'encrypt/' + filename
    target_file = 'decrypt/' + filename
    cipher = DES3.new(key, DES3.MODE_ECB)
    c_file = open(source_file, "rb")
    p_file = open(target_file, "wb")
    raw_data = b''
    ciphertext = c_file.read()
    raw_data = base64.b64decode(ciphertext)
    plaintext = unpad(cipher.decrypt(raw_data), DES3.block_size)
    p_file.write(plaintext)
    p_file.close()
    c_file.close()

def RC2Algo(filename,key):
    source_file = 'encrypt/' + filename
    target_file = 'decrypt/' + filename
    c_file = open(source_file, "rb")
    p_file = open(target_file, "wb")
    ciphertext = c_file.read()
    iv = Random.new().read(ARC2.block_size)
    cipher = ARC2.new(key, ARC2.MODE_CFB, iv)
    plaintext = iv + cipher.decrypt(ciphertext)
    p_file.write(plaintext)
    p_file.close()
    c_file.close()

def decrypter():
    tools.empty_folder('decrypt')
    files = sorted(os.listdir('encrypt/'))
    print(files)
    key_1 = b'mysecretpassword'  # 16 byte password
    key_2 = b'1234567887654321'  # DES 16 byte Key
    Key_3 = b'Sixteen byte key'  #  RC2 16 byte key
    for index in range(len(files)):
        for name in files:
            if "AES" in name:
                AESAlgo(name, key_1)
                print(name)
            elif "DES" in name:
                DESAlgo(name, key_2)
                print(name)
            elif "RC2" in name:
                RC2Algo(name,Key_3)
                print(name)
