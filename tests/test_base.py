import unittest
import sys

from crccheck.base import CrccheckBase
from crccheck.crc import ALLCRCCLASSES
import random

def randombytes(length):
    return [random.randint(0, 255) for n in range(0, length)]

class TestBase(unittest.TestCase):

    def test_abstract_method(self):
        """ For coverage """
        with self.assertRaises(NotImplementedError):
            ab = CrccheckBase()
            ab.process(bytearray(10))

    def test_init(self):
        for CrcClass in ALLCRCCLASSES:
            for n in range(0, 16):
                value = random.randint(0, 4294967295)
                assert CrcClass(value).value() == value

    def test_reset(self):
        for CrcClass in ALLCRCCLASSES:
            for n in range(0, 16):
                value = random.randint(0, 4294967295)
                c = CrcClass()
                c.reset(value)
                assert c.value() == value

    def test_final(self):
        """.final() should not change internal value"""
        for CrcClass in ALLCRCCLASSES:
            for n in range(0, 16):
                data = randombytes(16)
                crc = CrcClass()
                crc.process(data)
                assert crc.final() == crc.final()

    def test_finalhex(self):
        """.finalhex() should match .final()"""
        for CrcClass in ALLCRCCLASSES:
            for n in range(0, 16):
                data = randombytes(16)
                crc = CrcClass()
                crc.process(data)
                assert crc.final() == int(crc.finalhex(), 16)

    def test_finalbytes_big(self):
        """.finalbytes() should match .final()"""
        if sys.version_info < (3, 3, 0):
            raise self.skipTest("")
        for CrcClass in ALLCRCCLASSES:
            for n in range(0, 16):
                data = randombytes(16)
                crc = CrcClass()
                crc.process(data)
                assert crc.final() == int.from_bytes(crc.finalbytes('big'), 'big')

    def test_finalbytes_little(self):
        """.finalbytes() should match .final()"""
        if sys.version_info < (3, 3, 0):
            raise self.skipTest("")
        for CrcClass in ALLCRCCLASSES:
            for n in range(0, 16):
                data = randombytes(16)
                crc = CrcClass()
                crc.process(data)
                assert crc.final() == int.from_bytes(crc.finalbytes('little'), 'little')

    def test_calc(self):
        """.calc() must be identical to .process() + .final()"""
        for CrcClass in ALLCRCCLASSES:
            for n in range(0, 16):
                data = randombytes(16)
                crc = CrcClass()
                crc.process(data)
                assert CrcClass.calc(data) == crc.final()

    def test_calchex_big(self):
        """.calchex() must be identical to .process() + .finalhex()"""
        for CrcClass in ALLCRCCLASSES:
            for n in range(0, 16):
                data = randombytes(16)
                crc = CrcClass()
                crc.process(data)
                assert CrcClass.calchex(data, byteorder='big') == crc.finalhex('big')

    def test_calchex_little(self):
        """.calchex() must be identical to .process() + .finalhex()"""
        for CrcClass in ALLCRCCLASSES:
            for n in range(0, 16):
                data = randombytes(16)
                crc = CrcClass()
                crc.process(data)
                assert CrcClass.calchex(data, byteorder='little') == crc.finalhex('little')

    def test_calcbytes_big(self):
        """.calcbytes() must be identical to .process() + .finalbytes()"""
        for CrcClass in ALLCRCCLASSES:
            for n in range(0, 16):
                data = randombytes(16)
                crc = CrcClass()
                crc.process(data)
                assert CrcClass.calcbytes(data, byteorder='big') == crc.finalbytes('big')

    def test_calcbytes_little(self):
        """.calcbytes() must be identical to .process() + .finalbytes()"""
        for CrcClass in ALLCRCCLASSES:
            for n in range(0, 16):
                data = randombytes(16)
                crc = CrcClass()
                crc.process(data)
                assert CrcClass.calcbytes(data, byteorder='little') == crc.finalbytes('little')
