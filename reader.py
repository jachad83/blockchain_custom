import os

BUFFERSIZE = 65536
FILELIMIT = 10
DATAFOLDER = 'data'


def file_capture():
    _data_array = []
    _file_list = os.listdir(DATAFOLDER)

    if len(_file_list) < FILELIMIT:
        _filelimit = len(_file_list)
    else:
        _filelimit = FILELIMIT

    for _ in range(_filelimit):
        with open(os.path.join(DATAFOLDER, _file_list[_]), 'r') as afile:
            _buffer = afile.read(BUFFERSIZE)

            while len(_buffer) > 0:
                _data_array.append(_buffer)
                _buffer = afile.read(BUFFERSIZE)
                afile.close()

    return _data_array
