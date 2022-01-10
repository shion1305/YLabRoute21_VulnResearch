import datetime


def getTimeStrNow():
    return str(datetime.datetime.now().strftime("%y%m%d-%H%M%S"))

def filenameFormat(filename, replaceWith='-'):
    invalid = '<>:"/\|?*'
    for char in invalid:
        filename = filename.replace(char, replaceWith)
    return filename