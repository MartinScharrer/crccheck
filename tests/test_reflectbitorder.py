from crccheck.base import reflectbitorder


def test_1():
    assert reflectbitorder(8, 0x80) == 0x01


def test_2():
    assert reflectbitorder(16, 0x8000) == 0x0001


def test_3():
    assert reflectbitorder(8, 0x81) == 0x81


def test_4():
    assert reflectbitorder(80, (1 << 79)) == 0x01


def test_5():
    assert reflectbitorder(65, 0x1) == (1 << 64)


def test_6():
    assert reflectbitorder(3, 0b110) == 0b011


def test_7():
    assert reflectbitorder(3, 0b110) == 0b011


def test_8():
    assert reflectbitorder(0, 0) == 0


def expect(w, v, e):
    assert reflectbitorder(w, v) == e


def test_random():
    import random
    random.seed()
    for width in range(1, 125):
        randombitstr = "".join([str(random.randint(0, 1)) for m in range(0, width)])
        value = int(randombitstr, 2)
        expectedresult = int("".join(reversed(randombitstr)), 2)
        yield expect, width, value, expectedresult
