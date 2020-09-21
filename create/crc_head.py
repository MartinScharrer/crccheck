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
    _names = ()
    _width = 0
    _poly = 0x00
    _initvalue = 0x00
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00
    _check_result = None
    _check_data = bytearray(b"123456789")
    _residue = None

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
               self._xor_output == other._xor_output

    def __repr__(self):
        residue = hex(self._residue) if self._residue is not None else 'None'
        check_result = hex(self._check_result) if self._check_result is not None else 'None'
        return ("Crc(width={:d}, poly=0x{:x}, initvalue=0x{:X}, reflect_input={!s:s}, reflect_output={!s:s}, " +
                "xor_output=0x{:x}, check_result={}, residue={})").format(
                self._width, self._poly, self._initvalue, self._reflect_input, self._reflect_output,
                self._xor_output, check_result, residue)


def find(classes=None, width=None, poly=None, initvalue=None, reflect_input=None, reflect_output=None, xor_output=None,
         check_result=None, residue=None):
    """Find CRC classes which the matching properties.

    Args:
        classes (None or list): List of classes to search in. If None the list ALLCRCCLASSES will be used.
        width (None or int): number of bits of the CRC classes to find
        poly (None or int): polygon to find
        initvalue (None or int): initvalue to find
        reflect_input (None or bool): reflect_input to find
        reflect_output (None or bool): reflect_output to find
        xor_output (None or int): xor_output to find
        check_result (None or int): check_result to find
        residue (None or int): residue to find

    Returns:
        List of CRC classes with the selected properties.

    Examples:
        Find all CRC16 classes:
            $ find(width=16)

        Find all CRC32 classes with all-1 init value and XOR output:
            $ find(width=32, initvalue=0xFFFF, xor_output=0xFFFF)
    """
    found = list()
    if classes is None:
        classes = ALLCRCCLASSES
    for cls in classes:
        if width is not None and width != cls._width:
            continue
        if poly is not None and poly != cls._poly:
            continue
        if initvalue is not None and initvalue != cls._initvalue:
            continue
        if reflect_input is not None and reflect_input != cls._reflect_input:
            continue
        if reflect_output is not None and reflect_output != cls._reflect_output:
            continue
        if xor_output is not None and xor_output != cls._xor_output:
            continue
        if check_result is not None and check_result != cls._check_result:
            continue
        if residue is not None and residue != cls._residue:
            continue
        found.append(cls)
    return found


def identify(data, crc, width=None, classes=None, one=True):
    """
    Identify the used CRC algorithm which was used to calculate the CRC from some data.

    This function can be used to identify a suitable CRC class if the exact CRC algorithm/parameters
    are not known, but a CRC value is known from some data. Note that this function can be quite
    time consuming on large data, especially if the given width is not known.

    Args:
        data (bytes): Data to compare with the `crc`.
        crc (int): Known CRC of the given `data`.
        width (int or None): Known bit width of given `crc`.
            Providing the width will speed up the identification of the CRC algorithm.
        classes (iterable or None): Listing of classes to check. If None then ALLCRCCLASSES is used.
        one (bool): If True then only the first found CRC class is retunred.
            Otherwise a list of all suitable CRC classes.

    Returns:
        If `one` is True:
            CRC class which instances produce the given CRC from the given data.
            If no CRC class could be found `None` is returned.
        If `one` is False:
            List of CRC classes which instances produce the given CRC from the given data.
            The list may be empty.
    """
    if classes is None:
        classes = ALLCRCCLASSES
    if width is not None:
        classes = (cls for cls in classes if cls._width == width)

    found = []
    for cls in classes:
        if cls().calc(data) == crc:
            if one:
                return cls
            found.append(cls)
    if one:
        return None
    return found


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
            residue (int): The residue expected after calculating the CRC over the original data followed by the
                CRC of the original data. With initvalue=0 and xor_output=0 the residue calculates always to 0.
    """
    _width = 0
    _poly = 0x00
    _initvalue = 0x00
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00
    _check_result = None
    _residue = None

    def __init__(self, width, poly, initvalue=0x00, reflect_input=False, reflect_output=False, xor_output=0x00,
                 check_result=0x00, residue=0x00):
        super(Crc, self).__init__(initvalue)
        self._initvalue = int(initvalue)
        self._width = int(width)
        self._poly = int(poly)
        self._reflect_input = bool(reflect_input)
        self._reflect_output = bool(reflect_output)
        self._xor_output = int(xor_output)
        self._check_result = int(check_result) if check_result is not None else None
        self._residue = int(residue) if residue is not None else None

    def calc(self, data, initvalue=None, **kwargs):
        """ Fully calculate CRC/checksum over given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.
                initvalue (int): Initial value. If None then the default value for the class is used.

            Return:
                int: final value
        """
        self.reset()
        self.process(data)
        return self.final()

    def calchex(self, data, initvalue=None, byteorder='big', **kwargs):
        """Fully calculate checksum over given data. Return result as hex string.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.
                initvalue (int): Initial value. If None then the default value for the class is used.
                byteorder ('big' or 'little'): order (endianness) of returned bytes.

            Return:
                str: final value as hex string without leading '0x'.
        """
        self.reset()
        self.process(data)
        return self.finalhex()

    def calcbytes(self, data, initvalue=None, byteorder='big', **kwargs):
        """Fully calculate checksum over given data. Return result as bytearray.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.
                initvalue (int): Initial value. If None then the default value for the class is used.
                byteorder ('big' or 'little'): order (endianness) of returned bytes.

            Return:
                bytes: final value as bytes
        """
        self.reset()
        self.process(data)
        return self.finalbytes(byteorder)

    def selftest(self, data=None, expectedresult=None, **kwargs):
        if data is None:
            data = self._check_data
            expectedresult = self._check_result
        result = self.calc(data)
        if result != expectedresult:
            raise CrccheckError("{:s}: expected {:s}, got {:s}".format(
                self.__class__.__name__, hex(expectedresult), hex(result)))


class Crc8Base(CrcBase):
    """CRC-8.
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
    """CRC-16.
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
    """CRC-32.
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
