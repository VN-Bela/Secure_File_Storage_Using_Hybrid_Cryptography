import os
from . import tools


def merge():
    tools.empty_folder('restore')
    files = os.listdir('decrypt')
    for index in range(len(files)):
        print(files[index])
        reader = open('decrypt/' + files[index], 'r')
        data = reader.read()
        print(data)
        reader.close()
        writer = open('restore/' + files[0], 'a+')
        writer.write(data)
        writer.close()
