""" Unit tests for checksum module.

  License::
  
    Copyright (C) 2015  Martin Scharrer <martin@scharrer-online.de>

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

from checksum.checksum import ALLCHECKSUMCLASSES, Checksum32


def test_allchecksums():
    for checksumclass in ALLCHECKSUMCLASSES:
        def selftest_bigendian():
            return checksumclass.selftest(bigendian=True)

        selftest_bigendian.description = checksumclass.__name__ + " [bigendian]"
        yield selftest_bigendian

        def selftest_littleendian():
            return checksumclass.selftest(bigendian=True)

        selftest_bigendian.description = checksumclass.__name__ + " [bigendian]"
        yield selftest_bigendian


def test_generator():
    Checksum32.calc((n for n in range(0, 255)))


def test_list1():
    Checksum32.calc([n for n in range(0, 255)])


def test_list2():
    Checksum32.calc([n for n in range(0, 255)], 100)


def test_list3():
    Checksum32.calc([n for n in range(0, 255)], 100, 200)


def test_list4():
    Checksum32.calc([n for n in range(0, 255)], 100, 200, 0)


def test_bytearray1():
    Checksum32.calc(bytearray.fromhex("12345678909876543210"))


def test_bytearray2():
    Checksum32.calc(bytearray.fromhex("12345678909876543210"), 5, -1)


def test_bytes():
    Checksum32.calc(bytes.fromhex("12345678909876543210"))


def test_bytes():
    Checksum32.calc(bytes.fromhex("12345678909876543210"), 5, -1)


def test_string1():
    Checksum32.calc(b"Teststring")


def test_string2():
    Checksum32.calc(b"Teststring", 5, -1)


def test_string3():
    Checksum32.calc("Teststring".encode(), )
