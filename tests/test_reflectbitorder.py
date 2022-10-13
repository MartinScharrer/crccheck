""" Unit tests for reflectbitorder function.

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
from crccheck.base import reflectbitorder
from tests import TestCase


class TestReflectBitOrder(TestCase):

    def test_1(self):
        self.assertEqual(reflectbitorder(8, 0x80), 0x01)

    def test_2(self):
        self.assertEqual(reflectbitorder(16, 0x8000), 0x0001)

    def test_3(self):
        self.assertEqual(reflectbitorder(8, 0x81), 0x81)

    def test_4(self):
        self.assertEqual(reflectbitorder(80, (1 << 79)), 0x01)

    def test_5(self):
        self.assertEqual(reflectbitorder(65, 0x1), (1 << 64))

    def test_6(self):
        self.assertEqual(reflectbitorder(3, 0b110), 0b011)

    def test_7(self):
        self.assertEqual(reflectbitorder(3, 0b110), 0b011)

    def test_8(self):
        self.assertEqual(reflectbitorder(0, 0), 0)

    def expect(self, w, v, e):
        self.assertEqual(reflectbitorder(w, v), e)

    def test_random(self):
        import random
        random.seed()
        for width in range(1, 125):
            randombitstr = "".join([str(random.randint(0, 1)) for m in range(0, width)])
            value = int(randombitstr, 2)
            expectedresult = int("".join(reversed(randombitstr)), 2)
            with self.subTest(width=width):
                self.expect(width, value, expectedresult)
