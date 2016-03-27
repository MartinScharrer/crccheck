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

from checksum.crc import ALLCRCCLASSES


def test_allcrc():
    for crcclass in ALLCRCCLASSES:
        crcclass.selftest.__dict__['description'] = crcclass.__name__
        yield crcclass.selftest


def res(crcclass):
    import random
    random.seed()
    length = 1020
    databytes = bytearray((random.randint(0, 255) for n in range(0, length)))
    crc = crcclass()
    crc.process(databytes)
    crcbytes = crc.finalbytes(bigendian=False)
    crc.process(crcbytes)
    residue = crc.final()
    if residue != crcclass._residue:
        raise Exception("Expected residue==0, got {0:d} (0x{0:08X})".format(residue))


def test_check():
    for crcclass in ALLCRCCLASSES:
        res.__dict__['description'] = "Residue of " + crcclass.__name__
        yield res, crcclass
