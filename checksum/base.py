"""
    Copyright (c) 2015 by Martin Scharrer <martin@scharrer-online.de>

    Base class for checksum classes like CRC.

    Written by Martin Scharrer, Ph.D., April 2015.
"""
import math

REFLECT_BIT_ORDER_TABLE = (
    0x00, 0x80, 0x40, 0xC0, 0x20, 0xA0, 0x60, 0xE0,
    0x10, 0x90, 0x50, 0xD0, 0x30, 0xB0, 0x70, 0xF0,
    0x08, 0x88, 0x48, 0xC8, 0x28, 0xA8, 0x68, 0xE8,
    0x18, 0x98, 0x58, 0xD8, 0x38, 0xB8, 0x78, 0xF8,
    0x04, 0x84, 0x44, 0xC4, 0x24, 0xA4, 0x64, 0xE4,
    0x14, 0x94, 0x54, 0xD4, 0x34, 0xB4, 0x74, 0xF4,
    0x0C, 0x8C, 0x4C, 0xCC, 0x2C, 0xAC, 0x6C, 0xEC,
    0x1C, 0x9C, 0x5C, 0xDC, 0x3C, 0xBC, 0x7C, 0xFC,
    0x02, 0x82, 0x42, 0xC2, 0x22, 0xA2, 0x62, 0xE2,
    0x12, 0x92, 0x52, 0xD2, 0x32, 0xB2, 0x72, 0xF2,
    0x0A, 0x8A, 0x4A, 0xCA, 0x2A, 0xAA, 0x6A, 0xEA,
    0x1A, 0x9A, 0x5A, 0xDA, 0x3A, 0xBA, 0x7A, 0xFA,
    0x06, 0x86, 0x46, 0xC6, 0x26, 0xA6, 0x66, 0xE6,
    0x16, 0x96, 0x56, 0xD6, 0x36, 0xB6, 0x76, 0xF6,
    0x0E, 0x8E, 0x4E, 0xCE, 0x2E, 0xAE, 0x6E, 0xEE,
    0x1E, 0x9E, 0x5E, 0xDE, 0x3E, 0xBE, 0x7E, 0xFE,
    0x01, 0x81, 0x41, 0xC1, 0x21, 0xA1, 0x61, 0xE1,
    0x11, 0x91, 0x51, 0xD1, 0x31, 0xB1, 0x71, 0xF1,
    0x09, 0x89, 0x49, 0xC9, 0x29, 0xA9, 0x69, 0xE9,
    0x19, 0x99, 0x59, 0xD9, 0x39, 0xB9, 0x79, 0xF9,
    0x05, 0x85, 0x45, 0xC5, 0x25, 0xA5, 0x65, 0xE5,
    0x15, 0x95, 0x55, 0xD5, 0x35, 0xB5, 0x75, 0xF5,
    0x0D, 0x8D, 0x4D, 0xCD, 0x2D, 0xAD, 0x6D, 0xED,
    0x1D, 0x9D, 0x5D, 0xDD, 0x3D, 0xBD, 0x7D, 0xFD,
    0x03, 0x83, 0x43, 0xC3, 0x23, 0xA3, 0x63, 0xE3,
    0x13, 0x93, 0x53, 0xD3, 0x33, 0xB3, 0x73, 0xF3,
    0x0B, 0x8B, 0x4B, 0xCB, 0x2B, 0xAB, 0x6B, 0xEB,
    0x1B, 0x9B, 0x5B, 0xDB, 0x3B, 0xBB, 0x7B, 0xFB,
    0x07, 0x87, 0x47, 0xC7, 0x27, 0xA7, 0x67, 0xE7,
    0x17, 0x97, 0x57, 0xD7, 0x37, 0xB7, 0x77, 0xF7,
    0x0F, 0x8F, 0x4F, 0xCF, 0x2F, 0xAF, 0x6F, 0xEF,
    0x1F, 0x9F, 0x5F, 0xDF, 0x3F, 0xBF, 0x7F, 0xFF,
)


def reflectbitorder(width, value):
    """Reflects the bit order of the given value according to the given bit width."""
    nbytes = int((width + 7) / 8)
    databytes = [REFLECT_BIT_ORDER_TABLE[(value >> (8 * n)) & 0xFF] for n in range(0, nbytes)]
    result = 0
    for n in range(0, nbytes):
        result |= (databytes[n] << ((nbytes - n - 1) * 8))
    diff = nbytes * 8 - width
    if diff > 0:
        result >>= diff
    return result


class ChecksumError(Exception):
    """General checksum error exception"""
    pass


class ChecksumBase(object):
    """Abstract base class for checksumming classes"""
    _initvalue = 0x00
    _check_result = None
    _check_data = None
    _file_chunksize = 512
    _width = 0

    def __init__(self, initvalue=None):
        if initvalue is None:
            self._value = self._initvalue
        else:
            self._value = initvalue

    def init(self, initvalue=None):
        self.__init__(initvalue)

    def process(self, data, startindex=0, endindex=None):
        """Processes given data, from [startindex:endindex] if given.
        """
        pass

    @classmethod
    def _iter(cls, data, startindex=0, endindex=None):
        from mmap import mmap
        if isinstance(data, (str, bytes, mmap)):
            return cls._iterstring(data, startindex, endindex)
        elif hasattr(data, 'seek') and hasattr(data, 'tell') and hasattr(data, 'read'):
            return cls._iterfile(data, startindex, endindex)
        else:
            if startindex == 0 and endindex is None:
                return data
            else:
                return data[startindex:endindex]

    @classmethod
    def _iterstring(cls, data, startindex=0, endindex=None):
        if startindex < 0:
            startindex += len(data)
        if endindex is None:
            endindex = len(data)
        elif endindex < 0:
            endindex += len(data)
        for n in range(startindex, endindex):
            yield ord(data[n])

    @classmethod
    def _iterfile(cls, data, startindex=0, endindex=None):
        if startindex < 0:
            data.seek(startindex, 2)
            startindex = data.tell()
        elif startindex > 0:
            data.seek(startindex, 1)
        if endindex is None:
            endindex = float('inf')
        elif endindex < -1:
            pos = data.tell()
            data.seek(endindex, 2)
            endindex = data.tell() - pos
            data.seek(pos, 0)
        nleft = endindex - startindex + 1
        while nleft > 0:
            content = data.read(min(nleft, cls._file_chunksize))
            if not content:
                break
            nleft -= len(content)
            for byte in content:
                yield ord(byte)

    def final(self):
        """Return final checksum value.
           The internal state is not modified by this so further data can be processed afterwards.
        """
        return self._value

    def finalhex(self):
        """Return final checksum value as hexadecimal string (without leading "0x"). The hex value is zero padded to bitwidth/8.
           The internal state is not modified by this so further data can be processed afterwards.
        """
        hexfrm = "{{:0{:d}X}}".format(math.ceil(self._width / 8.0))
        return hexfrm.format(self.final())

    def finalbytes(self, bigendian=True):
        """Return final checksum value as byte array.
           The internal state is not modified by this so further data can be processed afterwards.
        """
        cbytes = bytearray.fromhex(self.finalhex())
        if not bigendian:
            cbytes.reverse()
        return cbytes

    def value(self):
        """Returns current intermediate checksum value.
           Note that in general final() must be used to get the a final checksum.
        """
        return self._value

    @classmethod
    def calc(cls, data, startindex=0, endindex=None, initvalue=None, **kwargs):
        """Fully calculate checksum over given data."""
        inst = cls(initvalue, **kwargs)
        inst.process(data, startindex, endindex)
        return inst.final()

    @classmethod
    def calchex(cls, data, startindex=0, endindex=None, initvalue=None, **kwargs):
        """Fully calculate checksum over given data. Return result as hex string."""
        inst = cls(initvalue, **kwargs)
        inst.process(data, startindex, endindex)
        return inst.finalhex()

    @classmethod
    def calcbytes(cls, data, startindex=0, endindex=None, initvalue=None, bigendian=True, **kwargs):
        """Fully calculate checksum over given data. Return result as bytearray."""
        inst = cls(initvalue, **kwargs)
        inst.process(data, startindex, endindex)
        return inst.finalbytes(bigendian=bigendian)

    @classmethod
    def selftest(cls, data=None, expectedresult=None):
        if data is None:
            data = cls._check_data
            expectedresult = cls._check_result
        result = cls.calc(data)
        if result != expectedresult:
            raise ChecksumError(hex(result))
