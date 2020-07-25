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


class Crc8(CrcBase):
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


class Crc16(CrcBase):
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


class Crc32(CrcBase):
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


class Crc3Rohc(CrcBase):
    """CRC-3/ROHC"""
    _width = 3
    _poly = 0x3
    _initvalue = 0x7
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x0
    _check_result = 0x6


class Crc4Itu(CrcBase):
    """CRC-4/ITU"""
    _width = 4
    _poly = 0x3
    _initvalue = 0x0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x0
    _check_result = 0x7


class Crc5Epc(CrcBase):
    """CRC-5/EPC"""
    _width = 5
    _poly = 0x09
    _initvalue = 0x09
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00
    _check_result = 0x00


class Crc5Itu(CrcBase):
    """CRC-5/ITU"""
    _width = 5
    _poly = 0x15
    _initvalue = 0x00
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x00
    _check_result = 0x07


class Crc5Usb(CrcBase):
    """CRC-5/USB"""
    _width = 5
    _poly = 0x05
    _initvalue = 0x1F
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x1F
    _check_result = 0x19


class Crc6Cdma2000A(CrcBase):
    """CRC-6/CDMA2000-A"""
    _width = 6
    _poly = 0x27
    _initvalue = 0x3F
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00
    _check_result = 0x0D


class Crc6Cdma2000B(CrcBase):
    """CRC-6/CDMA2000-B"""
    _width = 6
    _poly = 0x07
    _initvalue = 0x3F
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00
    _check_result = 0x3B


class Crc6Darc(CrcBase):
    """CRC-6/DARC"""
    _width = 6
    _poly = 0x19
    _initvalue = 0x00
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x00
    _check_result = 0x26


class Crc6Itu(CrcBase):
    """CRC-6/ITU"""
    _width = 6
    _poly = 0x03
    _initvalue = 0x00
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x00
    _check_result = 0x06


class Crc7(CrcBase):
    """CRC-7"""
    _width = 7
    _poly = 0x09
    _initvalue = 0x00
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00
    _check_result = 0x75


class Crc7Rohc(CrcBase):
    """CRC-7/ROHC"""
    _width = 7
    _poly = 0x4F
    _initvalue = 0x7F
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x00
    _check_result = 0x53


class Crc8Cdma2000(Crc8):
    """CRC-8/CDMA2000"""
    _width = 8
    _poly = 0x9B
    _initvalue = 0xFF
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00
    _check_result = 0xDA


class Crc8Darc(Crc8):
    """CRC-8/DARC"""
    _width = 8
    _poly = 0x39
    _initvalue = 0x00
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x00
    _check_result = 0x15


class Crc8DvbS2(Crc8):
    """CRC-8/DVB-S2"""
    _width = 8
    _poly = 0xD5
    _initvalue = 0x00
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00
    _check_result = 0xBC


class Crc8Ebu(Crc8):
    """CRC-8/EBU"""
    _width = 8
    _poly = 0x1D
    _initvalue = 0xFF
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x00
    _check_result = 0x97


class Crc8ICode(Crc8):
    """CRC-8/I-CODE"""
    _width = 8
    _poly = 0x1D
    _initvalue = 0xFD
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00
    _check_result = 0x7E


class Crc8Itu(Crc8):
    """CRC-8/ITU"""
    _width = 8
    _poly = 0x07
    _initvalue = 0x00
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x55
    _check_result = 0xA1


class Crc8Maxim(Crc8):
    """CRC-8/MAXIM"""
    _width = 8
    _poly = 0x31
    _initvalue = 0x00
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x00
    _check_result = 0xA1


class Crc8Rohc(Crc8):
    """CRC-8/ROHC"""
    _width = 8
    _poly = 0x07
    _initvalue = 0xFF
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x00
    _check_result = 0xD0


class Crc8Wcdma(Crc8):
    """CRC-8/WCDMA"""
    _width = 8
    _poly = 0x9B
    _initvalue = 0x00
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x00
    _check_result = 0x25


class Crc10(CrcBase):
    """CRC-10"""
    _width = 10
    _poly = 0x233
    _initvalue = 0x000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x000
    _check_result = 0x199


class Crc10Cdma2000(CrcBase):
    """CRC-10/CDMA2000"""
    _width = 10
    _poly = 0x3D9
    _initvalue = 0x3FF
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x000
    _check_result = 0x233


class Crc11(CrcBase):
    """CRC-11"""
    _width = 11
    _poly = 0x385
    _initvalue = 0x01A
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x000
    _check_result = 0x5A3


class Crc123Gpp(CrcBase):
    """CRC-12/3GPP"""
    _width = 12
    _poly = 0x80F
    _initvalue = 0x000
    _reflect_input = False
    _reflect_output = True
    _xor_output = 0x000
    _check_result = 0xDAF


class Crc12Cdma2000(CrcBase):
    """CRC-12/CDMA2000"""
    _width = 12
    _poly = 0xF13
    _initvalue = 0xFFF
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x000
    _check_result = 0xD4D


class Crc12Dect(CrcBase):
    """CRC-12/DECT"""
    _width = 12
    _poly = 0x80F
    _initvalue = 0x000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x000
    _check_result = 0xF5B


class Crc13Bbc(CrcBase):
    """CRC-13/BBC"""
    _width = 13
    _poly = 0x1CF5
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0x04FA


class Crc14Darc(CrcBase):
    """CRC-14/DARC"""
    _width = 14
    _poly = 0x0805
    _initvalue = 0x0000
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x0000
    _check_result = 0x082D


class Crc15(CrcBase):
    """CRC-15"""
    _width = 15
    _poly = 0x4599
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0x059E


class Crc15Mpt1327(CrcBase):
    """CRC-15/MPT1327"""
    _width = 15
    _poly = 0x6815
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0001
    _check_result = 0x2566


class CrcArc(Crc16):
    """ARC"""
    _width = 16
    _poly = 0x8005
    _initvalue = 0x0000
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x0000
    _check_result = 0xBB3D


class Crc16AugCcitt(Crc16):
    """CRC-16/AUG-CCITT"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0x1D0F
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0xE5CC


class Crc16Buypass(Crc16):
    """CRC-16/BUYPASS"""
    _width = 16
    _poly = 0x8005
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0xFEE8


class Crc16CcittFalse(Crc16):
    """CRC-16/CCITT-FALSE"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0xFFFF
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0x29B1


class Crc16Cdma2000(Crc16):
    """CRC-16/CDMA2000"""
    _width = 16
    _poly = 0xC867
    _initvalue = 0xFFFF
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0x4C06


class Crc16Dds110(Crc16):
    """CRC-16/DDS-110"""
    _width = 16
    _poly = 0x8005
    _initvalue = 0x800D
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0x9ECF


class Crc16DectR(Crc16):
    """CRC-16/DECT-R"""
    _width = 16
    _poly = 0x0589
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0001
    _check_result = 0x007E


class Crc16DectX(Crc16):
    """CRC-16/DECT-X"""
    _width = 16
    _poly = 0x0589
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0x007F


class Crc16Dnp(Crc16):
    """CRC-16/DNP"""
    _width = 16
    _poly = 0x3D65
    _initvalue = 0x0000
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xFFFF
    _check_result = 0xEA82


class Crc16En13757(Crc16):
    """CRC-16/EN-13757"""
    _width = 16
    _poly = 0x3D65
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0xFFFF
    _check_result = 0xC2B7


class Crc16Genibus(Crc16):
    """CRC-16/GENIBUS"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0xFFFF
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0xFFFF
    _check_result = 0xD64E


class Crc16Maxim(Crc16):
    """CRC-16/MAXIM"""
    _width = 16
    _poly = 0x8005
    _initvalue = 0x0000
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xFFFF
    _check_result = 0x44C2


class Crcc16Mcrf4xx(Crc16):
    """CRC-16/MCRF4XX"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0xFFFF
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x0000
    _check_result = 0x6F91


class Crc16Riello(Crc16):
    """CRC-16/RIELLO"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0xB2AA
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x0000
    _check_result = 0x63D0


class Crc16T10Dif(Crc16):
    """CRC-16/T10-DIF"""
    _width = 16
    _poly = 0x8BB7
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0xD0DB


class Crc16Teledisk(Crc16):
    """CRC-16/TELEDISK"""
    _width = 16
    _poly = 0xA097
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0x0FB3


class Crc16Tms37157(Crc16):
    """CRC-16/TMS37157"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0x89EC
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x0000
    _check_result = 0x26B1


class Crc16Usb(Crc16):
    """CRC-16/USB"""
    _width = 16
    _poly = 0x8005
    _initvalue = 0xFFFF
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xFFFF
    _check_result = 0xB4C8


class CrcA(Crc16):
    """CRC-A"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0xC6C6
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x0000
    _check_result = 0xBF05


class Crc16Ccitt(Crc16):
    """CRC16 CCITT, aka KERMIT"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0x0000
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x0000
    _check_result = 0x2189


CrcKermit = Crc16Ccitt


class CrcModbus(CrcBase):
    """MODBUS"""
    _width = 16
    _poly = 0x8005
    _initvalue = 0xFFFF
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x0000
    _check_result = 0x4B37


class CrcX25(CrcBase):
    """X-25"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0xFFFF
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xFFFF
    _check_result = 0x906E


class CrcXmodem(CrcBase):
    """XMODEM"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0x31C3


class Crc16Cms(Crc16):
    """CRC-16/CMS"""
    _width = 16
    _poly = 0x8005
    _initvalue = 0xffff
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0xaee7
    _residue = 0x0000


class Crc16Gsm(Crc16):
    """CRC-16/GSM"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0xffff
    _check_result = 0xce3c
    _residue = 0x1d0f


class Crc16Ibm3740(Crc16):
    """CRC-16/IBM-3740"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0xffff
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0x29b1
    _residue = 0x0000


class Crc16IbmSdlc(Crc16):
    """CRC-16/IBM-SDLC"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0xffff
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xffff
    _check_result = 0x906e
    _residue = 0xf0b8


class Crc16IsoIec144433A(Crc16):
    """CRC-16/ISO-IEC-14443-3-A"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0xc6c6
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x0000
    _check_result = 0xbf05
    _residue = 0x0000


class Crc16Lj1200(Crc16):
    """CRC-16/LJ1200"""
    _width = 16
    _poly = 0x6f63
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0xbdf4
    _residue = 0x0000


class Crc16Mcrf4Xx(Crc16):
    """CRC-16/MCRF4XX"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0xffff
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x0000
    _check_result = 0x6f91
    _residue = 0x0000


class Crc16Nrsc5(Crc16):
    """CRC-16/NRSC-5"""
    _width = 16
    _poly = 0x080b
    _initvalue = 0xffff
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x0000
    _check_result = 0xa066
    _residue = 0x0000


class Crc16OpensafetyA(Crc16):
    """CRC-16/OPENSAFETY-A"""
    _width = 16
    _poly = 0x5935
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0x5d38
    _residue = 0x0000


class Crc16OpensafetyB(Crc16):
    """CRC-16/OPENSAFETY-B"""
    _width = 16
    _poly = 0x755b
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0x20fe
    _residue = 0x0000


class Crc16Profibus(Crc16):
    """CRC-16/PROFIBUS"""
    _width = 16
    _poly = 0x1dcf
    _initvalue = 0xffff
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0xffff
    _check_result = 0xa819
    _residue = 0xe394


class Crc16SpiFujitsu(Crc16):
    """CRC-16/SPI-FUJITSU"""
    _width = 16
    _poly = 0x1021
    _initvalue = 0x1d0f
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0xe5cc
    _residue = 0x0000


class Crc16Umts(Crc16):
    """CRC-16/UMTS"""
    _width = 16
    _poly = 0x8005
    _initvalue = 0x0000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0xfee8
    _residue = 0x0000


class Crc17CanFd(CrcBase):
    """CRC-17/CAN-FD"""
    _width = 17
    _poly = 0x1685b
    _initvalue = 0x00000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000
    _check_result = 0x04f03


class Crc21CanFd(CrcBase):
    """CRC-21/CAN-FD"""
    _width = 21
    _poly = 0x102899
    _initvalue = 0x00000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x000000
    _check_result = 0x0ed841


class Crc24(CrcBase):
    """CRC-24"""
    _width = 24
    _poly = 0x864CFB
    _initvalue = 0xB704CE
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x000000
    _check_result = 0x21CF02


class Crc24FlexrayA(CrcBase):
    """CRC-24/FLEXRAY-A"""
    _width = 24
    _poly = 0x5D6DCB
    _initvalue = 0xFEDCBA
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x000000
    _check_result = 0x7979BD


class Crc24FlexrayB(CrcBase):
    """CRC-24/FLEXRAY-B"""
    _width = 24
    _poly = 0x5D6DCB
    _initvalue = 0xABCDEF
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x000000
    _check_result = 0x1F23B8


class Crc24Ble(CrcBase):
    """CRC-24/BLE"""
    _width = 24
    _poly = 0x00065b
    _initvalue = 0x555555
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x000000
    _check_result = 0xc25a56


class Crc24LteA(CrcBase):
    """CRC-24/LTE-A"""
    _width = 24
    _poly = 0x864cfb
    _initvalue = 0x000000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x000000
    _check_result = 0xcde703


class Crc24LteB(CrcBase):
    """CRC-24/LTE-B"""
    _width = 24
    _poly = 0x800063
    _initvalue = 0x000000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x000000
    _check_result = 0x23ef52


class Crc24Interlaken(CrcBase):
    """CRC-24/INTERLAKEN"""
    _width = 24
    _poly = 0x328b63
    _initvalue = 0xffffff
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0xffffff
    _check_result = 0xb4f3e6
    _residue = 0x144e63


class Crc24OpenPgp(CrcBase):
    """CRC-24/OPENPGP"""
    _width = 24
    _poly = 0x864cfb
    _initvalue = 0xb704ce
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x000000
    _check_result = 0x21cf02
    _residue = 0x000000


class Crc24Os9(CrcBase):
    """CRC-24/OS-9"""
    _width = 24
    _poly = 0x800063
    _initvalue = 0xffffff
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0xffffff
    _check_result = 0x200fa5
    _residue = 0x800fe3


class Crc30Cdma(CrcBase):
    """CRC-30/CDMA"""
    _width = 30
    _poly = 0x2030b9c7
    _initvalue = 0x3fffffff
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x3fffffff
    _check_result = 0x04c34abf
    _residue = 0x34efa55a


class Crc31Philips(CrcBase):
    """CRC-31/PHILIPS"""
    _width = 31
    _poly = 0x04C11DB7
    _initvalue = 0x7FFFFFFF
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x7FFFFFFF
    _check_result = 0x0CE9E46C


class Crc32Bzip2(Crc32):
    """CRC-32/BZIP2"""
    _width = 32
    _poly = 0x04C11DB7
    _initvalue = 0xFFFFFFFF
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0xFFFFFFFF
    _check_result = 0xFC891918


class Crc32c(Crc32):
    """CRC-32C"""
    _width = 32
    _poly = 0x1EDC6F41
    _initvalue = 0xFFFFFFFF
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xFFFFFFFF
    _check_result = 0xE3069283


class Crc32d(Crc32):
    """CRC-32D"""
    _width = 32
    _poly = 0xA833982B
    _initvalue = 0xFFFFFFFF
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xFFFFFFFF
    _check_result = 0x87315576


class Crc32Mpeg2(Crc32):
    """CRC-32/MPEG-2"""
    _width = 32
    _poly = 0x04C11DB7
    _initvalue = 0xFFFFFFFF
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00000000
    _check_result = 0x0376E6E7


class Crc32Posix(Crc32):
    """CRC-32/POSIX"""
    _width = 32
    _poly = 0x04C11DB7
    _initvalue = 0x00000000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0xFFFFFFFF
    _check_result = 0x765E7680


class Crc32q(Crc32):
    """CRC-32Q"""
    _width = 32
    _poly = 0x814141AB
    _initvalue = 0x00000000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00000000
    _check_result = 0x3010BF7F


class CrcJamcrc(Crc32):
    """JAMCRC"""
    _width = 32
    _poly = 0x04C11DB7
    _initvalue = 0xFFFFFFFF
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x00000000
    _check_result = 0x340BC6D9


class CrcXfer(Crc32):
    """XFER"""
    _width = 32
    _poly = 0x000000AF
    _initvalue = 0x00000000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00000000
    _check_result = 0xBD0BE338


class Crc32Aixm(Crc32):
    """CRC-32/AIXM"""
    _width = 32
    _poly = 0x814141ab
    _initvalue = 0x00000000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x00000000
    _check_result = 0x3010bf7f
    _residue = 0x00000000


class Crc32Autosar(Crc32):
    """CRC-32/AUTOSAR"""
    _width = 32
    _poly = 0xf4acfb13
    _initvalue = 0xffffffff
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xffffffff
    _check_result = 0x1697d06a
    _residue = 0x904cddbf


class Crc32Base91D(Crc32):
    """CRC-32/BASE91-D"""
    _width = 32
    _poly = 0xa833982b
    _initvalue = 0xffffffff
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xffffffff
    _check_result = 0x87315576
    _residue = 0x45270551


class Crc32CdRomEdc(Crc32):
    """CRC-32/CD-ROM-EDC"""
    _width = 32
    _poly = 0x8001801b
    _initvalue = 0x00000000
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x00000000
    _check_result = 0x6ec2edc4
    _residue = 0x00000000


class Crc32Cksum(Crc32):
    """CRC-32/CKSUM"""
    _width = 32
    _poly = 0x04c11db7
    _initvalue = 0x00000000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0xffffffff
    _check_result = 0x765e7680
    _residue = 0xc704dd7b


class Crc32Iscsi(Crc32):
    """CRC-32/ISCSI"""
    _width = 32
    _poly = 0x1edc6f41
    _initvalue = 0xffffffff
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xffffffff
    _check_result = 0xe3069283
    _residue = 0xb798b438


class Crc32IsoHdlc(Crc32):
    """CRC-32/ISO-HDLC"""
    _width = 32
    _poly = 0x04c11db7
    _initvalue = 0xffffffff
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xffffffff
    _check_result = 0xcbf43926
    _residue = 0xdebb20e3


class Crc40Gsm(CrcBase):
    """CRC-40/GSM"""
    _width = 40
    _poly = 0x0004820009
    _initvalue = 0x0000000000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0xFFFFFFFFFF
    _check_result = 0xD4164FC646


class Crc64(CrcBase):
    """CRC-64"""
    _width = 64
    _poly = 0x42F0E1EBA9EA3693
    _initvalue = 0x0000000000000000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000000000000000
    _check_result = 0x6C40DF5F0B497347


class Crc64We(CrcBase):
    """CRC-64/WE"""
    _width = 64
    _poly = 0x42F0E1EBA9EA3693
    _initvalue = 0xFFFFFFFFFFFFFFFF
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0xFFFFFFFFFFFFFFFF
    _check_result = 0x62EC59E3F1A4F00A


class Crc64Xz(CrcBase):
    """CRC-64/XZ"""
    _width = 64
    _poly = 0x42F0E1EBA9EA3693
    _initvalue = 0xFFFFFFFFFFFFFFFF
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xFFFFFFFFFFFFFFFF
    _check_result = 0x995DC9BBDF1939FA


class Crc64Ecma182(CrcBase):
    """CRC-64/ECMA-182"""
    _width = 64
    _poly = 0x42f0e1eba9ea3693
    _initvalue = 0x0000000000000000
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0x0000000000000000
    _check_result = 0x6c40df5f0b497347
    _residue = 0x0000000000000000


class Crc64GoIso(CrcBase):
    """CRC-64/GO-ISO"""
    _width = 64
    _poly = 0x000000000000001b
    _initvalue = 0xffffffffffffffff
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0xffffffffffffffff
    _check_result = 0xb90956c775a41001
    _residue = 0x5300000000000000


class Crc82Darc(CrcBase):
    """CRC-82/DARC"""
    _width = 82
    _poly = 0x0308C0111011401440411
    _initvalue = 0x000000000000000000000
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0x000000000000000000000
    _check_result = 0x09EA83F625023801FD612


ALLCRCCLASSES = (
    Crc3Rohc, Crc4Itu, Crc5Epc, Crc5Itu, Crc5Usb, Crc6Cdma2000A, Crc6Cdma2000B, Crc6Darc, Crc6Itu, Crc7, Crc7Rohc,
    Crc8, Crc8Cdma2000, Crc8Darc, Crc8DvbS2, Crc8Ebu, Crc8ICode, Crc8Itu, Crc8Maxim, Crc8Rohc, Crc8Wcdma, Crc10,
    Crc10Cdma2000, Crc11, Crc123Gpp, Crc12Cdma2000, Crc12Dect, Crc13Bbc, Crc14Darc, Crc15, Crc15Mpt1327, Crc16, CrcArc,
    Crc16AugCcitt, Crc16Buypass, Crc16CcittFalse, Crc16Cdma2000, Crc16Dds110, Crc16DectR, Crc16DectX, Crc16Dnp,
    Crc16En13757, Crc16Genibus, Crc16Maxim, Crcc16Mcrf4xx, Crc16Riello, Crc16T10Dif, Crc16Teledisk, Crc16Tms37157,
    Crc16Usb, CrcA, Crc16Ccitt, CrcKermit, CrcModbus, CrcX25, CrcXmodem,
    Crc16Cms, Crc16Gsm, Crc16Ibm3740, Crc16IbmSdlc, Crc16IsoIec144433A, Crc16Lj1200,
    Crc16Mcrf4Xx, Crc16Nrsc5, Crc16OpensafetyA, Crc16OpensafetyB, Crc16Profibus,
    Crc16SpiFujitsu, Crc16Umts, Crc17CanFd, Crc21CanFd, Crc24, Crc24FlexrayA,
    Crc24FlexrayB, Crc24Ble, Crc24Interlaken, Crc24LteA, Crc24LteB, Crc24OpenPgp, Crc24Os9, Crc30Cdma, Crc31Philips,
    Crc32, Crc32Bzip2, Crc32c, Crc32d, Crc32Mpeg2, Crc32Posix, Crc32q, CrcJamcrc, CrcXfer,
    Crc32CdRomEdc, Crc32Cksum, Crc32Iscsi, Crc32IsoHdlc, Crc32Aixm, Crc32Autosar, Crc32Base91D, Crc40Gsm,
    Crc64, Crc64We, Crc64Xz, Crc64Ecma182, Crc64GoIso, Crc82Darc
)
