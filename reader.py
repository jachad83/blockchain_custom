import os

BUFFERSIZE = 65536
FILELIMIT = 10
DATAFOLDER = 'data'


def file_capture():
    data_array = []
    file_list = os.listdir(DATAFOLDER)

    if len(file_list) < FILELIMIT:
        filelimit_ = len(file_list)
    else:
        filelimit_ = FILELIMIT

    for _ in range(filelimit_):
        with open(os.path.join(DATAFOLDER, file_list[_]), 'r') as afile:
            buffer = afile.read(BUFFERSIZE)

            while len(buffer) > 0:
                data_array.append(buffer)
                buffer = afile.read(BUFFERSIZE)
                afile.close()

    return data_array

