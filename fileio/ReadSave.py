import pickle
import os


def saveList(list, loc):
    """Default location for saveList is `resultData`"""
    print(os.getcwd() + '\\resultData\\' + str(loc))
    f = open(os.getcwd() + '\\resultData\\' + str(loc), 'wb')
    pickle.dump(list, f)
    return


def readList(loc):
    f = open(loc, "rb")
    list = pickle.load(f)
    return list


def filenameFormat(filename, replaceWith='-'):
    invalid = '<>:"/\|?*'
    for char in invalid:
        filename = filename.replace(char, replaceWith)
    return filename
