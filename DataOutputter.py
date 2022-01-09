from FormatStandizer import *
import os
from pathlib import Path


def easyOutput(data, folder=getTimeStrNow()):
    if not Path(os.path.join(os.getcwd(), 'output', folder)).exists():
        os.mkdir(os.path.join(os.getcwd(), 'output', folder))
        for d in data:
            f = open(os.getcwd() + '\\output\\' + folder + '\\' + d['_id'] + '.json', 'wt')
            f.write(str(d))
            f.close()
    else:
        print('Skipped. Folder \'%s\' already exists in output' % str(folder))
