from crccheck.crc import Crc32
from timeit import Timer

data = bytes(1024)

T1 = Timer('Crc32().calc(data)', 'from crccheck.crc import Crc32; data=bytes(1024)')
T2 = Timer('Crc32().calc(data)', 'from crccheck.crc import Crc32; data=bytes(1024); Crc32.generate_table()')
T3 = Timer('Crc32.generate_table(); Crc32().calc(data)', 'from crccheck.crc import Crc32; data=bytes(1024)')

n = 10000
t1 = T1.timeit(n)
t2 = T2.timeit(n)
t3 = T3.timeit(n)

print("t1={0:f}, t2={1:f}, t3={2:f}. t2/t1={3:f}".format(t1, t2, t3, t2/t1))

