from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Util.Padding import pad
from Cryptodome.Cipher import DES3
from Cryptodome.Cipher import ARC2
from Cryptodome import Random
import base64
from . import tools
import os
from . import RSA_Key
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes


def AESAlgo(filename, key):
    source_file = 'divideFile/' + filename
    # target_file = 'encrypt/' + 'AES' + filename
    target_file = 'encrypt/' + filename
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC)  # mode and encode utf-8 format
    #cipher = AES.new(key, AES.MODE_CBC)  # mode and encode utf-8 format
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
    target_file = 'encrypt/' + filename
    p_file = open(source_file, "rb")
    c_file = open(target_file, "wb")
    raw_data = p_file.read()
    raw_data = pad(raw_data, DES3.block_size)
    ciphertext = cipher.encrypt(raw_data)
    En_text = base64.b64encode(ciphertext)
    c_file.write(En_text)
    p_file.close()
    c_file.close()


def RC2Algo(filename, key):
    plaintext = b''
    source_file = 'divideFile/' + filename
    target_file = 'encrypt/' + filename
    p_file = open(source_file, "rb")
    c_file = open(target_file, "wb")
    plaintext = p_file.read()
    iv = Random.new().read(ARC2.block_size)
    cipher = ARC2.new(key, ARC2.MODE_CFB, iv)
    ciphertext = iv + cipher.encrypt(plaintext)
    c_file.write(ciphertext)
    p_file.close()
    c_file.close()


def key_Encryption(key):
    tools.empty_folder("Secret")
    data = key.encode("utf-8")
    print(data)

    file_out = open("Secret/encrypted_data.bin", "wb")
    recipient_key = RSA.import_key(open("Key/receiver.pem").read())
    session_key = get_random_bytes(16)
    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
    file_out.close()


def encrypter():
    tools.empty_folder('encrypt')
    files = sorted(os.listdir('divideFile/'))
    Key_1 = 'mysecretpassword'  # AES 16 byte password 128 bit Key
    Key_2 = b'1234567887654321'  # DES 16 byte Key
    Key_3 = b'Sixteen byte key'  # RC2
    for index in range(len(files)):
        if index % 4 == 0:
            AESAlgo(files[index], Key_1)
        elif index % 4 == 1:
            DESAlgo(files[index], Key_2)
        else:
            RC2Algo(files[index], Key_3)
    # Key store in one file
    RSA_Key.Key_Generate()
    Secret_Information = str(Key_1) + '\n' + str(Key_2) + '\n' + str(Key_3)
    key_Encryption(Secret_Information)
