from crccheck.crc import ALLCRCCLASSES
import crccheck.crc as crcmodule
from dl import aliases

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


al = sorted(((clsname, getattr(crcmodule, clsname)) for clsname in aliases.keys()), key=lambda x: x[1]._width)
table = [('Class', 'Alias Classes')]
table.extend((a[0], ', '.join(aliases[a[0]])) for a in al)
lengths = list(max(len(row[col]) for row in table) for col in range(2))

print('+', end='')
print('+'.join('-' * (lengths[n] + 2) for n in range(len(table[0]))), end='')
print('+')

print('| ', end='')
print(' | '.join('{: <{}s}'.format(content, lengths[n]) for n, content in enumerate(table[0])), end='')
print(' |')

print('+', end='')
print('+'.join('=' * (lengths[n] + 2) for n in range(len(table[0]))), end='')
print('+')

for a in al:
    name = a[0]
    sal = ', '.join(aliases[name])
    print('| {: <{}s} | {: <{}s} |'.format(name, lengths[0], sal, lengths[1]))
    print('+', end='')
    print('+'.join('-' * (lengths[n] + 2) for n in range(2)), end='')
    print('+')