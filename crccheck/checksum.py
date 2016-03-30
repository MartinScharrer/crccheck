""" Classes to calculated additive and XOR checksums.

  License::

    Copyright (C) 2015-2016 by Martin Scharrer <martin@scharrer-online.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from crccheck.base import CrccheckBase, CrccheckError


class ChecksumBase(CrccheckBase):
    """ Base class for all checksum classes.

        Args:
            initvalue (int): Initial value. If None then the default value for the class is used.
            byteorder ('big' or 'little'): byte order (endianness) used when reading the input bytes.
    """
    _width = 0
    _mask = 0
    _check_data = (0xDE, 0xAD, 0xBE, 0xEF, 0xAA, 0x55, 0xC2, 0x8C)
    _check_result_littleendian = None

    def __init__(self, initvalue=0, byteorder='big'):
        super(ChecksumBase, self).__init__(initvalue)
        self._byteorder = byteorder

    def process(self, data):
        """ Process given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.

            Returns:
                self
        """
        dataword = 0
        n = 0
        bigendian = (self._byteorder == 'big')
        width = self._width
        mask = self._mask
        value = self._value
        for byte in data:
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
        return self

    @classmethod
    def selftest(cls, data=None, expectedresult=None, byteorder='big'):
        """ Selftest method for automated tests.

            Args:
                data (bytes, bytearray or list of int [0-255]): data to process
                expectedresult (int): expected result
                byteorder ('big' or 'little'): byte order (endianness) used when reading the input bytes.

            Raises:
                CrccheckError: if result is not as expected
        """
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
    """ 32-bit checksum.

        Calculates 32-bit checksum by adding the input bytes in groups of four.
        Input data length must be a multiple of four, otherwise the last bytes are not used.
    """
    _width = 32
    _mask = 0xFFffFFff
    _check_result = 0x8903817B
    _check_result_littleendian = 0x7C810388


class Checksum16(ChecksumBase):
    """ 16-bit checksum.

        Calculates 16-bit checksum by adding the input bytes in groups of two.
        Input data length must be a multiple of two, otherwise the last byte is not used.
    """
    _width = 16
    _mask = 0xFFff
    _check_result = 0x0A7D
    _check_result_littleendian = 0x8008


class Checksum8(ChecksumBase):
    """ 8-bit checksum.

        Calculates 8-bit checksum by adding the input bytes.
    """
    _width = 8
    _mask = 0xFF
    _check_result = 0x85
    _check_result_littleendian = _check_result


class ChecksumXorBase(ChecksumBase):
    """ Base class for all XOR checksum classes. """

    def process(self, data):
        """ Process given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.

            Returns:
                self
        """
        dataword = 0
        n = 0
        bigendian = (self._byteorder == 'big')
        width = self._width
        mask = self._mask
        value = self._value
        for byte in data:
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
        return self


class ChecksumXor32(ChecksumXorBase):
    """ 32-bit XOR checksum.

        Calculates 32-bit checksum by XOR-ing the input bytes in groups of four.
        Input data length must be a multiple of four, otherwise the last bytes are not used.
    """
    _width = 32
    _mask = 0xFFffFFff
    _check_result = 0x74F87C63
    _check_result_littleendian = 0x637CF874


class ChecksumXor16(ChecksumXorBase):
    """ 16-bit XOR checksum.

        Calculates 16-bit checksum by XOR-ing the input bytes in groups of two.
        Input data length must be a multiple of two, otherwise the last byte is not used.
    """
    _width = 16
    _mask = 0xFFff
    _check_result = 0x089B
    _check_result_littleendian = 0x9B08


class ChecksumXor8(ChecksumXorBase):
    """ 8-bit XOR checksum.

        Calculates 8-bit checksum by XOR-ing the input bytes.
    """
    _width = 8
    _mask = 0xFF
    _check_result = 0x93
    _check_result_littleendian = _check_result


ALLCHECKSUMCLASSES = (
    Checksum8, Checksum16, Checksum32,
    ChecksumXor8, ChecksumXor16, ChecksumXor32,
)

