""" Unit tests for checksum module.

  License::

    License: MIT <https://opensource.org/licenses/MIT>
    Copyright (c) 2015-2022 by Martin Scharrer <martin.scharrer@web.de>

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software
    and associated documentation files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or
    substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
    BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
import sys

from crccheck import checksum
from crccheck.base import CrccheckError
from crccheck.checksum import ALLCHECKSUMCLASSES, Checksum32, Checksum, ChecksumXor
from tests import TestCase, randbytes


class TestChecksum(TestCase):

    def test_allchecksums_bigendian(self):
        for checksumclass in ALLCHECKSUMCLASSES:
            with self.subTest(checksumclass=checksumclass):
                checksumclass.selftest(byteorder='big')

    def test_allchecksums_littleendian(self):
        for checksumclass in ALLCHECKSUMCLASSES:
            with self.subTest(checksumclass=checksumclass):
                checksumclass.selftest(byteorder='little')

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
        if sys.version_info < (3, 3, 0):  # pragma: no cover
            raise self.skipTest("")
        Checksum32.calc(bytes.fromhex("12345678909876543210"))

    def test_string1(self):
        if sys.version_info < (3, 3, 0):  # pragma: no cover
            raise self.skipTest("")
        Checksum32.calc(b"Teststring")

    def test_string3(self):
        if sys.version_info < (3, 3, 0):  # pragma: no cover
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
            with self.assertRaises(ValueError):
                Checksum(n)

    def test_general_checksum_ident(self):
        data = randbytes(1024)
        self.assertEqual(checksum.Checksum32.calc(data), checksum.Checksum(32).process(data).final())
        self.assertEqual(checksum.Checksum16.calc(data), checksum.Checksum(16).process(data).final())
        self.assertEqual(checksum.Checksum8.calc(data), checksum.Checksum(8).process(data).final())

    def test_general_checksumxor_valid_width(self):
        """ Checksum()

            Should allow for any positive width
            which is a multiple of 8.
        """
        for n in range(8, 129, 8):
            ChecksumXor(n)

    def test_general_checksumxor_invalid_width(self):
        for n in (0, 1, 7, 9, 33):
            with self.assertRaises(ValueError):
                ChecksumXor(n)

    def test_general_checksumxor_ident(self):
        data = randbytes(1024)
        self.assertEqual(checksum.ChecksumXor32.calc(data), checksum.ChecksumXor(32).process(data).final())
        self.assertEqual(checksum.ChecksumXor16.calc(data), checksum.ChecksumXor(16).process(data).final())
        self.assertEqual(checksum.ChecksumXor8.calc(data), checksum.ChecksumXor(8).process(data).final())
