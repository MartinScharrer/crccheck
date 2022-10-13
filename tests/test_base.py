"""Test modules for base package.

  License::

    MIT License

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
import random
import sys

from crccheck.base import CrccheckBase
from crccheck.crc import ALLCRCCLASSES
from tests import TestCase, randbytes


class TestBase(TestCase):

    def test_abstract_method(self):
        """ For coverage """
        with self.assertRaises(NotImplementedError):
            ab = CrccheckBase()
            ab.process(bytearray(10))

    def test_init(self):
        for CrcClass in ALLCRCCLASSES:
            with self.subTest(CrcClass):
                for n in range(0, 16):
                    value = random.randint(0, 4294967295)
                    self.assertEqual(CrcClass(value).value(), value)

    def test_reset(self):
        for CrcClass in ALLCRCCLASSES:
            with self.subTest(CrcClass):
                for n in range(0, 16):
                    value = random.randint(0, 4294967295)
                    c = CrcClass()
                    c.reset(value)
                    self.assertEqual(c.value(), value)

    def test_final(self):
        """.final() should not change internal value"""
        for CrcClass in ALLCRCCLASSES:
            with self.subTest(CrcClass):
                for n in range(0, 16):
                    data = randbytes(16)
                    crc = CrcClass()
                    crc.process(data)
                    self.assertEqual(crc.final(), crc.final())

    def test_finalhex(self):
        """.finalhex() should match .final()"""
        for CrcClass in ALLCRCCLASSES:
            with self.subTest(CrcClass):
                for n in range(0, 16):
                    data = randbytes(16)
                    crc = CrcClass()
                    crc.process(data)
                    self.assertEqual(crc.final(), int(crc.finalhex(), 16))

    def test_finalbytes_big(self):
        """.finalbytes() should match .final()"""
        if sys.version_info < (3, 3, 0):  # pragma: no cover
            raise self.skipTest("")
        for CrcClass in ALLCRCCLASSES:
            with self.subTest(CrcClass):
                for n in range(0, 16):
                    data = randbytes(16)
                    crc = CrcClass()
                    crc.process(data)
                    self.assertEqual(crc.final(), int.from_bytes(crc.finalbytes('big'), 'big'))

    def test_finalbytes_little(self):
        """.finalbytes() should match .final()"""
        if sys.version_info < (3, 3, 0):  # pragma: no cover
            raise self.skipTest("")
        for CrcClass in ALLCRCCLASSES:
            with self.subTest(CrcClass):
                for n in range(0, 16):
                    data = randbytes(16)
                    crc = CrcClass()
                    crc.process(data)
                    self.assertEqual(crc.final(), int.from_bytes(crc.finalbytes('little'), 'little'))

    def test_calc(self):
        """.calc() must be identical to .process() + .final()"""
        for CrcClass in ALLCRCCLASSES:
            with self.subTest(CrcClass):
                for n in range(0, 16):
                    data = randbytes(16)
                    crc = CrcClass()
                    crc.process(data)
                    self.assertEqual(CrcClass.calc(data), crc.final())

    def test_calchex_big(self):
        """.calchex() must be identical to .process() + .finalhex()"""
        for CrcClass in ALLCRCCLASSES:
            with self.subTest(CrcClass):
                for n in range(0, 16):
                    data = randbytes(16)
                    crc = CrcClass()
                    crc.process(data)
                    self.assertEqual(CrcClass.calchex(data, byteorder='big'), crc.finalhex('big'))

    def test_calchex_little(self):
        """.calchex() must be identical to .process() + .finalhex()"""
        for CrcClass in ALLCRCCLASSES:
            with self.subTest(CrcClass):
                for n in range(0, 16):
                    data = randbytes(16)
                    crc = CrcClass()
                    crc.process(data)
                    self.assertEqual(CrcClass.calchex(data, byteorder='little'), crc.finalhex('little'))

    def test_calcbytes_big(self):
        """.calcbytes() must be identical to .process() + .finalbytes()"""
        for CrcClass in ALLCRCCLASSES:
            with self.subTest(CrcClass):
                for n in range(0, 16):
                    data = randbytes(16)
                    crc = CrcClass()
                    crc.process(data)
                    self.assertSequenceEqual(CrcClass.calcbytes(data, byteorder='big'), crc.finalbytes('big'))

    def test_calcbytes_little(self):
        """.calcbytes() must be identical to .process() + .finalbytes()"""
        for CrcClass in ALLCRCCLASSES:
            with self.subTest(CrcClass):
                for n in range(0, 16):
                    data = randbytes(16)
                    crc = CrcClass()
                    crc.process(data)
                    self.assertSequenceEqual(CrcClass.calcbytes(data, byteorder='little'), crc.finalbytes('little'))
