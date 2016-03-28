from crccheck.base import CrccheckBase, CrccheckError


class ChecksumBase(CrccheckBase):
    _width = 0
    _mask = 0
    _check_data = (0xDE, 0xAD, 0xBE, 0xEF, 0xAA, 0x55, 0xC2, 0x8C)
    _check_result_littleendian = None

    def __init__(self, initvalue=0, byteorder='big'):
        super(ChecksumBase, self).__init__(initvalue)
        self._byteorder = byteorder

    def process(self, data, startindex=0, endindex=None):
        dataword = 0
        n = 0
        if startindex == 0 and endindex is None:
            databytes = data
        else:
            databytes = data[startindex:endindex]
        bigendian = (self._byteorder == 'big')
        width = self._width
        mask = self._mask
        value = self._value
        for byte in databytes:
            if bigendian:
                dataword = (dataword << 8) | byte
            else:
                dataword |= (byte << n)
            n += 8
            if n == width:
                value = mask & (value + dataword)
                dataword = 0
                n = 0
        self._value = value

    @classmethod
    def selftest(cls, data=None, expectedresult=None, byteorder='big'):
        if data is None:
            data = cls._check_data
        if expectedresult is None:
            if byteorder == 'big':
                expectedresult = cls._check_result
            else:
                expectedresult = cls._check_result_littleendian
        result = cls.calc(data, byteorder=byteorder)
        if result != expectedresult:
            raise CrccheckError(hex(result))


class Checksum32(ChecksumBase):
    _width = 32
    _mask = 0xFFffFFff
    _check_result = 0x8903817B
    _check_result_littleendian = 0x7C810388


class Checksum16(ChecksumBase):
    _width = 16
    _mask = 0xFFff
    _check_result = 0x0A7D
    _check_result_littleendian = 0x8008


class Checksum8(ChecksumBase):
    _width = 8
    _mask = 0xFF
    _check_result = 0x85
    _check_result_littleendian = _check_result


class ChecksumXorBase(ChecksumBase):
    def process(self, data, startindex=0, endindex=None):
        dataword = 0
        n = 0
        if startindex == 0 and endindex is None:
            databytes = data
        else:
            databytes = data[startindex:endindex]
        bigendian = (self._byteorder == 'big')
        width = self._width
        mask = self._mask
        value = self._value
        for byte in databytes:
            if bigendian:
                dataword = (dataword << 8) | byte
            else:
                dataword |= (byte << n)
            n += 8
            if n == width:
                value = mask & (value ^ dataword)
                dataword = 0
                n = 0
        self._value = value


class ChecksumXor32(ChecksumXorBase):
    _width = 32
    _mask = 0xFFffFFff
    _check_result = 0x74F87C63
    _check_result_littleendian = 0x637CF874


class ChecksumXor16(ChecksumXorBase):
    _width = 16
    _mask = 0xFFff
    _check_result = 0x089B
    _check_result_littleendian = 0x9B08


class ChecksumXor8(ChecksumXorBase):
    _width = 8
    _mask = 0xFF
    _check_result = 0x93
    _check_result_littleendian = _check_result


ALLCHECKSUMCLASSES = (
    Checksum8, Checksum16, Checksum32,
    ChecksumXor8, ChecksumXor16, ChecksumXor32,
)

