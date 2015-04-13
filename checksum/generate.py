
import pprint

def reflect(byte):
    result = 0
    for i in range(0,8):
        if byte & (1<<i):
            result |= (0x80>>i)
    return result
    

def reflecttable():
    table = tuple(( reflect(i) for i in range(0,256) ))
    return table
    
def printreflecttable():
    s = "("
    i = 0
    while i < 256:
        s += "\n   "
        for n in range(0,8):
            s += " 0x{:02X},".format(reflect(i))
            i+=1
    s += "\n)"
    return s
    