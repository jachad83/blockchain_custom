import os


def file_capture(buffer, limit, folder):
    _data_array = []
    _file_list = os.listdir(folder)

    if len(_file_list) < limit:
        _filelimit = len(_file_list)
    else:
        _filelimit = limit

    for _ in range(_filelimit):
        with open(os.path.join(folder, _file_list[_]), 'r') as afile:
            _buffer = afile.read(buffer)

            while len(_buffer) > 0:
                _data_array.append(_buffer)
                _buffer = afile.read(buffer)

    return _data_array
