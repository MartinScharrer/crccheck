from crccheck.crc import ALLCRCCLASSES
import crccheck.crc as crcmodule
from dl import aliases, getclassname

head = """\
Supported CRCs
==============

"""


fmts = (
        '{: <{}s}', '{: <{}s}', '{: <{}d}', '0x{: <{}X}', '0x{: <{}X}',
        '{!s: <{}s}', '{!s: <{}s}', '0x{: <{}X}', '0x{: <{}X}', '0x{: <{}X}'
)

table_head = (
    'CRC Name', 'Class', 'Bit width', 'Poly', 'Initvalue', 'Reflect input',
    'Reflect output', 'XOR output', 'Check', 'Residue'
)

table = []

for c in ALLCRCCLASSES:
    c._crcname = c.__doc__.splitlines()[0]
    table.append((
        c._crcname, c.__name__, c._width, c._poly, c._initvalue,
        c._reflect_input, c._reflect_output, c._xor_output,
        c._check_result, c._residue
    ))

# get column width

lengths = list(max(len(fmts[col].format(row[col], 0)) for row in table) for col in range(len(table[0])))
lengths = list(max((a, len(b))) for a, b in zip(lengths, table_head))

tlengths = [l + (2 if fmts[n].startswith('0x') else 0) for n, l in enumerate(lengths)]

print(head)

print('+', end='')
print('+'.join('-' * (tlengths[n] + 2) for n in range(len(table_head))), end='')
print('+')

print('| ', end='')
print(' | '.join('{: <{}s}'.format(content, tlengths[n]) for n, content in enumerate(table_head)), end='')
print(' |')

print('+', end='')
print('+'.join('=' * (tlengths[n] + 2) for n in range(len(table_head))), end='')
print('+')

for row in table:
    print('| ', end='')
    print(' | '.join(fmts[n].format(content, lengths[n]) for n, content in enumerate(row)), end='')
    print(' |')
    print('+', end='')
    print('+'.join('-' * (tlengths[n] + 2) for n in range(len(row))), end='')
    print('+')

#
# print("".join(template.format(c=c) for c in ALLCRCCLASSES))


print("""

Aliases
-------

As some CRCs are also known under different names aliases for the CRC classes are defined.

""")

al = sorted(((name, getclassname(name), getattr(crcmodule, getclassname(name))) for name in aliases.keys()), key=lambda x: x[2]._width)
table = [('CRC', 'Class', 'Alias', 'Alias Classes')]
table.extend((a[0], a[1], ', '.join(aliases[a[0]]), ', '.join(getclassname(name) for name in aliases[a[0]])) for a in al)
lengths = list(max(len(row[col]) for row in table) for col in range(4))

print('+', end='')
print('+'.join('-' * (lengths[n] + 2) for n in range(len(table[0]))), end='')
print('+')

print('| ', end='')
print(' | '.join('{: <{}s}'.format(content, lengths[n]) for n, content in enumerate(table[0])), end='')
print(' |')

print('+', end='')
print('+'.join('=' * (lengths[n] + 2) for n in range(len(table[0]))), end='')
print('+')


for row in table[1:]:
    print('| {: <{}s} | {: <{}s} | {: <{}s} | {: <{}s} |'.format(row[0], lengths[0],
                                                                 row[1], lengths[1],
                                                                 row[2], lengths[2],
                                                                 row[3], lengths[3]))
    print('+', end='')
    print('+'.join('-' * (lengths[n] + 2) for n in range(4)), end='')
    print('+')