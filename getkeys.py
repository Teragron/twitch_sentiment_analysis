import win32api as wapi
import time

keyList = ["\b"]
for char in "BH ":
    keyList.append(char)

def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    if 'H' in keys:
        return 'H'
    elif 'B' in keys:
        return 'B'

    elif ' ' in keys:
        return 'Space'
    else:
        return "Nothing"
    # else:
    #     return "Nothing"
