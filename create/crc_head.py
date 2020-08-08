""" Classes to calculate CRCs (Cyclic Redundancy Check).

  License::

    Copyright (C) 2015-2020 by Martin Scharrer <martin@scharrer-online.de>

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
from crccheck.base import CrccheckBase, reflectbitorder, REFLECT_BIT_ORDER_TABLE, CrccheckError


class CrcBase(CrccheckBase):
    """Abstract base class for all Cyclic Redundancy Checks (CRC) checksums"""
    _width = 0
    _poly = 0x00
    _initvalue = 0x00
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00
    _check_result = None
    _check_data = bytearray(b"123456789")
    _residue = 0

    def process(self, data):
        """ Process given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.

            Returns:
                self
        """
        crc = self._value
        highbit = 1 << (self._width - 1)
        mask = ((highbit - 1) << 1) | 0x1  # done this way to avoid overrun for 64-bit values
        poly = self._poly
        shift = self._width - 8
        diff8 = -shift
        if diff8 > 0:
            # enlarge temporary to fit 8-bit
            mask = 0xFF
            crc <<= diff8
            shift = 0
            highbit = 0x80
            poly = self._poly << diff8

        reflect = self._reflect_input
        for byte in data:
            if reflect:
                byte = REFLECT_BIT_ORDER_TABLE[byte]
            crc ^= (byte << shift)
            for i in range(0, 8):
                if crc & highbit:
                    crc = (crc << 1) ^ poly
                else:
                    crc = (crc << 1)
            crc &= mask
        if diff8 > 0:
            crc >>= diff8
        self._value = crc
        return self

    def final(self):
        """ Return final CRC value.

            Return:
                int: final CRC value
        """
        crc = self._value
        if self._reflect_output:
            crc = reflectbitorder(self._width, crc)
        crc ^= self._xor_output
        return crc

    def __eq__(self, other):
        return self._width == other._width and \
               self._poly == other._poly and \
               self._initvalue == other._initvalue and \
               self._reflect_input == other._reflect_input and \
               self._reflect_output == other._reflect_output and \
               self._xor_output == other._xor_output and \
               self._check_result == other._check_result and \
               self._check_data == other._check_data and \
               self._residue == other._residue


class Crc(CrcBase):
    """ Creates a new general (user-defined) CRC calculator instance.

        Arguments:
            width (int): bit width of CRC.
            poly (int): polynomial of CRC with the top bit omitted.
            initvalue (int): initial value of internal running CRC value. Usually either 0 or (1<<width)-1,
                i.e. "all-1s".
            reflect_input (bool): If true the bit order of the input bytes are reflected first.
                This is to calculate the CRC like least-significant bit first systems will do it.
            reflect_output (bool): If true the bit order of the calculation result will be reflected before
                the XOR output stage.
            xor_output (int): The result is bit-wise XOR-ed with this value. Usually 0 (value stays the same) or
                (1<<width)-1, i.e. "all-1s" (invert value).
            check_result (int): The expected result for the check input "123456789" (= [0x31, 0x32, 0x33, 0x34,
                0x35, 0x36, 0x37, 0x38, 0x39]). This value is used for the selftest() method to verify proper
                operation.
    """
    _width = 0
    _poly = 0x00
    _initvalue = 0x00
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00
    _check_result = None

    def __init__(self, width, poly, initvalue=0x00, reflect_input=False, reflect_output=False, xor_output=0x00,
                 check_result=0x00):
        super(Crc, self).__init__(initvalue)
        self._initvalue = int(initvalue)
        self._width = int(width)
        self._poly = int(poly)
        self._reflect_input = bool(reflect_input)
        self._reflect_output = bool(reflect_output)
        self._xor_output = int(xor_output)
        self._check_result = int(check_result)

    def selftest(self, data=None, expectedresult=None, **kwargs):
        if data is None:
            data = self._check_data
            expectedresult = self._check_result
        self.reset()
        self.process(data, **kwargs)
        result = self.final()
        if result != expectedresult:
            raise CrccheckError("{:s}: expected {:s}, got {:s}".format(
                self.__class__.__name__, hex(expectedresult), hex(result)))


class Crc8Base(CrcBase):
    """CRC-8 base class.
       Has optimised code for 8-bit CRCs and is used as base class for all other CRC with this width.
    """
    _width = 8
    _poly = 0x07
    _initvalue = 0x00
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00
    _check_result = 0xF4

    def process(self, data):
        """ Process given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.

            Returns:
                self
        """
        crc = self._value

        reflect = self._reflect_input
        poly = self._poly
        for byte in data:
            if reflect:
                byte = REFLECT_BIT_ORDER_TABLE[byte]
            crc = crc ^ byte
            for i in range(0, 8):
                if crc & 0x80:
                    crc = (crc << 1) ^ poly
                else:
                    crc = (crc << 1)
            crc &= 0xFF
        self._value = crc
        return self


class Crc16Base(CrcBase):
    """CRC-16 base class.
       Has optimised code for 16-bit CRCs and is used as base class for all other CRC with this width.
    """
    _width = 16
    _poly = 0x1021
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0x31C3

    def process(self, data):
        """ Process given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.

            Returns:
                self
        """
        crc = self._value

        reflect = self._reflect_input
        poly = self._poly
        for byte in data:
            if reflect:
                byte = REFLECT_BIT_ORDER_TABLE[byte]
            crc ^= (byte << 8)
            for i in range(0, 8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ poly
                else:
                    crc = (crc << 1)
            crc &= 0xFFFF
        self._value = crc
        return self


class Crc32Base(CrcBase):
    """CRC-32 base class.
       Has optimised code for 32-bit CRCs and is used as base class for all other CRC with this width.
    """
    _width = 32
    _poly = 0x04C11DB7
    _initvalue = 0xFFFFFFFF
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xFFFFFFFF
    _check_result = 0xCBF43926

    def process(self, data):
        """ Process given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.

            Returns:
                self
        """
        crc = self._value

        reflect = self._reflect_input
        poly = self._poly
        for byte in data:
            if reflect:
                byte = REFLECT_BIT_ORDER_TABLE[byte]
            crc ^= (byte << 24)
            for i in range(0, 8):
                if crc & 0x80000000:
                    crc = (crc << 1) ^ poly
                else:
                    crc = (crc << 1)
            crc &= 0xFFFFFFFF
        self._value = crc
        return self

