import os
import utime

def fileExists(path):
    try:
        return (os.stat(path)[0] & 0x4000) != 0
    except OSError:
        return False

def firstOrDefault(sequence, selector, default=None):
    for s in sequence:
        if selector(s):
            return s
    return default

def getTimeString():
    time = utime.localtime(utime.time())
    return f"{time[3]:02}:{time[4]:02}"

def take(sequence, amount):
    amount += 1
    for s in sequence:
        amount -= 1
        if amount > 0:
            yield s
        else:
            return
