from django.conf import settings
import os
from .import tools

def divider(name):
    tools.empty_folder('divideFile')
    os.chdir('media/files/')
    CHUNK_SIZE = 500  # 500 Byte
    file_number = 1
    with open(name, "rb") as f:
        chunk = f.read(CHUNK_SIZE)
        while chunk:
            os.chdir(settings.BASE_DIR)
            with open('divideFile/' + name.split('.')[0] + str(file_number), "wb") as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = f.read(CHUNK_SIZE)
