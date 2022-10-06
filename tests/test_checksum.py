""" Unit tests for checksum module.

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
import unittest
import sys
import random
from crccheck import checksum
from crccheck.checksum import ALLCHECKSUMCLASSES, Checksum32, Checksum, ChecksumXor
from crccheck.base import CrccheckError

def randombytes(length):
    return [random.randint(0, 255) for n in range(0, length)]

class TestChecksum(unittest.TestCase):

    def test_allchecksums_bigendian(self):
        def selftest_bigendian(cls):
            return cls.selftest(byteorder='big')

        for checksumclass in ALLCHECKSUMCLASSES:
            with self.subTest(checksumclass=checksumclass):
                selftest_bigendian(checksumclass)

    def test_allchecksums_littleendian(self):
        def selftest_littleendian(cls):
            return cls.selftest(byteorder='little')

        for checksumclass in ALLCHECKSUMCLASSES:
            with self.subTest(checksumclass=checksumclass):
                selftest_littleendian(checksumclass)

    # noinspection PyProtectedMember
    def test_allchecksums_fail(self):
        with self.assertRaises(CrccheckError):
            checksumclass = ALLCHECKSUMCLASSES[0]
            checksumclass.selftest(checksumclass._check_data, ~checksumclass._check_result)

    def test_generator(self):
        Checksum32.calc((n for n in range(0, 255)))

    def test_list1(self):
        Checksum32.calc([n for n in range(0, 255)])

    def test_list2(self):
        Checksum32.calc([n for n in range(0, 255)], 1)

    def test_bytearray1(self):
        Checksum32.calc(bytearray.fromhex("12345678909876543210"))

    def test_bytes(self):
        if sys.version_info < (3, 3, 0):
            raise self.skipTest("")
        Checksum32.calc(bytes.fromhex("12345678909876543210"))

    def test_string1(self):
        if sys.version_info < (3, 3, 0):
            raise self.skipTest("")
        Checksum32.calc(b"Teststring")

    def test_string3(self):
        if sys.version_info < (3, 3, 0):
            raise self.skipTest("")
        Checksum32.calc("Teststring".encode(), )

    def test_general_checksum_valid_width(self):
        """ Checksum()

            Should allow for any positive width
            which is a multiple of 8.
        """
        for n in range(8, 129, 8):
            Checksum(n)

    def test_general_checksum_invalid_width(self):
        for n in (0, 1, 7, 9, 33):
            try:
                Checksum(n)
            except ValueError:
                pass
            else:
                raise Exception

    def test_general_checksum_ident(self):
        data = randombytes(1024)
        assert checksum.Checksum32.calc(data) == checksum.Checksum(32).process(data).final()
        assert checksum.Checksum16.calc(data) == checksum.Checksum(16).process(data).final()
        assert checksum.Checksum8.calc(data) == checksum.Checksum(8).process(data).final()

    def test_general_checksumxor_valid_width(self):
        """ Checksum()

            Should allow for any positive width
            which is a multiple of 8.
        """
        for n in range(8, 129, 8):
            ChecksumXor(n)

    def test_general_checksumxor_invalid_width(self):
        for n in (0, 1, 7, 9, 33):
            try:
                ChecksumXor(n)
            except ValueError:
                pass
            else:
                raise Exception

    def test_general_checksumxor_ident(self):
        data = randombytes(1024)
        assert checksum.ChecksumXor32.calc(data) == checksum.ChecksumXor(32).process(data).final()
        assert checksum.ChecksumXor16.calc(data) == checksum.ChecksumXor(16).process(data).final()
        assert checksum.ChecksumXor8.calc(data) == checksum.ChecksumXor(8).process(data).final()
