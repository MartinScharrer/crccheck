""" Classes to calculate CRCs and checksums from binary data
    ========================================================

    The :mod:`crccheck.crc` module implements all CRCs listed in the
    `Catalogue of parametrised CRC algorithms <http://reveng.sourceforge.net/crc-catalogue/>`_:

    CRC-3/ROHC, CRC-4/ITU, CRC-5/EPC, CRC-5/ITU, CRC-5/USB, CRC-6/CDMA2000-A, CRC-6/CDMA2000-B, CRC-6/DARC, CRC-6/ITU,
    CRC-7, CRC-7/ROHC, CRC-8, CRC-8/CDMA2000, CRC-8/DARC, CRC-8/DVB-S2, CRC-8/EBU, CRC-8/I-CODE, CRC-8/ITU, CRC-8/MAXIM,
    CRC-8/ROHC, CRC-8/WCDMA, CRC-10, CRC-10/CDMA2000, CRC-11, CRC-12/3GPP, CRC-12/CDMA2000, CRC-12/DECT, CRC-13/BBC,
    CRC-14/DARC, CRC-15, CRC-15/MPT1327, CRC-16, ARC, CRC-16/AUG-CCITT, CRC-16/BUYPASS, CRC-16/CCITT-FALSE,
    CRC-16/CDMA2000, CRC-16/DDS-110, CRC-16/DECT-R, CRC-16/DECT-X, CRC-16/DNP, CRC-16/EN-13757, CRC-16/GENIBUS,
    CRC-16/MAXIM, CRC-16/MCRF4XX, CRC-16/RIELLO, CRC-16/T10-DIF, CRC-16/TELEDISK, CRC-16/TMS37157, CRC-16/USB, CRC-A,
    CRC-16 CCITT, KERMIT, MODBUS, X-25, XMODEM, CRC-24, CRC-24/FLEXRAY-A, CRC-24/FLEXRAY-B, CRC-31/PHILIPS, CRC-32,
    CRC-32/BZIP2, CRC-32C, CRC-32D, CRC-32/MPEG-2, CRC-32/POSIX, CRC-32Q, JAMCRC, XFER, CRC-40/GSM, CRC-64, CRC-64/WE,
    CRC-64/XZ, CRC-82/DARC.

    For the class names simply remove all dashes and slashes from the above names and apply CamelCase, e.g.
    "CRC-32/MPEG-2" is implemented by :class:`.Crc32Mpeg2`. Other CRC can be calculated by using the general class
    :class:`crccheck.crc.Crc` by providing all required CRC parameters.

    The :mod:`crccheck.checksum` module implements additive and XOR checksums with 8, 16 and 32 bit:
    :class:`.Checksum8`, :class:`.Checksum16`, :class:`.Checksum32` and
    :class:`.ChecksumXor8`, :class:`.ChecksumXor16`, :class:`.ChecksumXor32`.

    Usage example::

        from crccheck.crc import Crc32, CrcXmodem
        from crccheck.checksum import Checksum32

        # Quick calculation
        data = bytearray.fromhex("DEADBEEF")
        crc = Crc32.calc(data)
        checksum = Checksum32.calc(data)

        # Procsss multiple data buffers
        data1 = b"Binary string"  # or use .encode(..) on normal sring - Python 3 only
        data2 = bytes.fromhex("1234567890")  # Python 3 only, use bytearray for older versions
        data3 = (0x0, 255, 12, 99)  # Iterable which returns ints in byte range (0..255)
        crcinst = CrcXmodem()
        crcinst.process(data1)
        crcinst.process(data2)
        crcinst.process(data3[1:-1])
        crcbytes = crcinst.finalbytes()
        crchex = crcinst.finalhex()
        crcint = crcinst.final()


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
from crccheck import crc, checksum

