import struct
import enum
        
def printMessage(s):
    return ' '.join("{:02x}".format(c) for c in s)

class MessageType(enum.Enum):
    Text = 0
    Numeric = 1
    Logic = 2

def encodeMessage(msgType, mail, value):
    mail = mail + '\x00'
    mailBytes = mail.encode('ascii') 
    mailSize = len(mailBytes)
    fmt = '<H4BB' + str(mailSize) + 'sH'
    
    if msgType == MessageType.Logic:
        valueSize = 1
        valueBytes = 1 if value is True else 0
        fmt += 'B'
    elif msgType == MessageType.Numeric:
        valueSize = 4
        valueBytes = float(value)
        fmt += 'f'
    else:
        value = value + '\x00'
        valueBytes = value.encode('ascii')
        valueSize = len(valueBytes)
        fmt += str(valueSize) + 's'
    
    payloadSize = 7 + mailSize + valueSize
    s = struct.pack(fmt, payloadSize, 0x01, 0x00, 0x81, 0x9e, mailSize, mailBytes, valueSize, valueBytes)
    return s
