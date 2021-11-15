from Cryptodome.Cipher import AES, DES3, PKCS1_OAEP
from Cryptodome.Util.Padding import unpad
import base64
from Cryptodome.Cipher import ARC2
from Cryptodome import Random
from . import tools
import os
from Cryptodome.PublicKey import RSA


def AESAlgo(filename, key):
   # print(key)
    source_file = 'encrypt/' + filename
    target_file = 'decrypt/' + filename
    c_file = open(source_file, "rb")
    iv = c_file.read(16)
    ciphertext = c_file.read()
    p_file = open(target_file, "wb")
    # cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    p_file.write(plaintext)
    c_file.close()
    p_file.close()


def DESAlgo(filename, key):
   # print(key)
    raw_data = b''
    source_file = 'encrypt/' + filename
    target_file = 'decrypt/' + filename

    c_file = open(source_file, "rb")
    p_file = open(target_file, "wb")
    ciphertext = c_file.read()
    cipher = DES3.new(key, DES3.MODE_ECB)
    raw_data = base64.b64decode(ciphertext)
    plaintext = unpad(cipher.decrypt(raw_data), DES3.block_size)
    p_file.write(plaintext)
    p_file.close()
    c_file.close()


def RC2Algo(filename, key):
   # print(key)
    source_file = 'encrypt/' + filename
    target_file = 'decrypt/' + filename
    c_file = open(source_file, "rb")
    p_file = open(target_file, "wb")
    ciphertext = c_file.read()
    #iv = Random.new().read(ARC2.block_size)
    iv = ciphertext[:ARC2.block_size]
    ciphertext = ciphertext[ARC2.block_size:]
    cipher = ARC2.new(key, ARC2.MODE_CFB, iv)
    plaintext = cipher.decrypt(ciphertext)
    p_file.write(plaintext)
    p_file.close()
    c_file.close()


def decrypter(keyfile):
    tools.empty_folder('decrypt')
    files = sorted(os.listdir('encrypt/'))
    print(files)
    # Key_1 = b'mysecretpassword'  # 16 byte password
    #  Key_2 = b'1234567887654321'  # DES 16 byte Key
    # Key_3 = b'Sixteen byte key'  # RC2 16 byte key

    # Three algoritham Key Decryption
    file_in = open("Secret/encrypted_data.bin", "rb")
    private_key = RSA.import_key(open("Key/" + keyfile).read())
    print(keyfile)

    enc_session_key, nonce, tag, ciphertext = [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]
    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)
    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    #  print("=========================")

    # print(data.decode("utf-8"))
    # Key Separation
    Key = data.decode("utf-8").split("\n")
    # print(Key)
    # print("=========================")

    s1 = Key[0]
    s2 = Key[1][2:-1]
    s3 = Key[2][2:-1]
    # Bytes Convertion
    Key_1 = bytes(s1, 'UTF-8')
    Key_2 = bytes(s2, 'UTF-8')
    Key_3 = bytes(s3, 'UTF-8')
    #  print(Key_1, "\n", type(Key_1))
    # print(Key_2, "\n", type(Key_2))
    # print(Key_3, "\n", type(Key_3))

    print("=========================")

    for index in range(len(files)):
        if index % 4 == 0:
            AESAlgo(files[index], Key_1)
        elif index % 4 == 1:
            DESAlgo(files[index], Key_2)
        else:
            RC2Algo(files[index], Key_3)
