import os

paths = os.walk('./')

for path, tmp2, file_list in paths:
    for i in file_list:
        print('{0:<50}'.format(os.path.join(path, i))+str(os.stat(os.path.join(path, i)).st_size))