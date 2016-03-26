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

from checksum.base import ChecksumError
from checksum.checksum import ALLCHECKSUMCLASSES

for crcclass in ALLCHECKSUMCLASSES:
    try:
        crcclass.selftest()
    except ChecksumError as e:
        print("FAILED:    BigEndian: {}: {!s:s} != 0x{:x}".format(crcclass.__name__, e, crcclass._check_result))
    else:
        print("OK:    BigEndian: " + crcclass.__name__)
    try:
        crcclass.selftest(bigendian=False)
    except ChecksumError as e:
        print("FAILED: LittleEndian: {}: {!s:s} != 0x{:x}".format(crcclass.__name__, e,
                                                                  crcclass._check_result_littleendian))
    else:
        print("OK: LittleEndian: " + crcclass.__name__)
