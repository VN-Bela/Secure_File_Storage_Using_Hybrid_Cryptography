from Cryptodome.PublicKey import RSA
from . import tools


def Key_Generate():
    tools.empty_folder('Key')
    key = RSA.generate(2048)
    private_key = key.export_key()
    # private Key
    file_out = open("Key/private.pem", "wb")
    file_out.write(private_key)
    file_out.close()
    # public Key
    public_key = key.publickey().export_key()
    file_out = open("Key/receiver.pem", "wb")
    file_out.write(public_key)
    file_out.close()
