import datetime


def getTimeStrNow():
    return str(datetime.datetime.now().strftime("%y%m%d-%H%M%S"))
