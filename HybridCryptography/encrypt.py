from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Cipher import DES3
from Cryptodome.Cipher import ARC2
from Cryptodome import Random
import base64
from .import tools
import os


def AESAlgo(filename, key):
    source_file = 'divideFile/' + filename
    target_file = 'encrypt/' + 'AES' + filename
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC)  # mode and encode utf-8 format
    plaintext = b''
    p_file = open(source_file, 'rb')
    c_file = open(target_file, 'wb')
    plaintext = p_file.read()
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    c_file.write(cipher.iv)
    c_file.write(ciphertext)
    p_file.close()
    c_file.close()


def DESAlgo(filename, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    raw_data = b''
    source_file = 'divideFile/' + filename
    target_file = 'encrypt/' + 'DES' + filename
    p_file = open(source_file, "rb")
    c_file = open(target_file, "wb")
    raw_data = p_file.read()
    raw_data = pad(raw_data, DES3.block_size)
    ciphertext = cipher.encrypt(raw_data)
    En_text = base64.b64encode(ciphertext)
    c_file.write(En_text)
    p_file.close()
    c_file.close()


def RC2Algo(filename,key):
    plaintext = b''
    source_file = 'divideFile/' + filename
    target_file = 'encrypt/' + 'RC2' + filename
    p_file = open(source_file, "rb")
    c_file = open(target_file, "wb")
    plaintext = p_file.read()
    iv = Random.new().read(ARC2.block_size)
    cipher = ARC2.new(key, ARC2.MODE_CFB, iv)
    ciphertext = iv + cipher.encrypt(plaintext)
    c_file.write(ciphertext)
    p_file.close()
    c_file.close()


def encrypter():
    tools.empty_folder('encrypt')
    files = sorted(os.listdir('divideFile/'))
    key_1 = 'mysecretpassword'  # AES 16 byte password 128 bit Key
    Key_2 = b'1234567887654321'  # DES 16 byte Key
    Key_3 = b'Sixteen byte key'
    for index in range(len(files)):
        AESAlgo(files[index], key_1)
        DESAlgo(files[index], Key_2)
        RC2Algo(files[index],Key_3)
