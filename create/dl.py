import urllib.request
import re
import sys

renames = {
    'ARC': 'CrcArc',
    'DOW-CRC': 'CrcDow',
    'R-CRC-16': 'Crc16R',
    'X-CRC-16': 'Crc16X',
    'X-25': 'CrcX25',
    'KERMIT': 'CrcKermit',
    'MODBUS': 'CrcModbus',
    'XMODEM': 'CrcXmodem',
    'ZMODEM': 'CrcZmodem',
    'B-CRC-32': 'Crc32B',
    'CKSUM': 'CrcCksum',
    'PKZIP': 'CrcPkzip',
    'JAMCRC': 'CrcJamcrc',
    'XFER': 'CrcXfer',
}

aliases = {
    'CRC-4/G-704': ('CRC-4/ITU',),
    'CRC-5/EPC-C1G2': ('CRC-5/EPC',),
    'CRC-5/G-704': ('CRC-5/ITU',),
    'CRC-6/G-704': ('CRC-6/ITU',),
    'CRC-7/MMC': ('CRC-7',),
    'CRC-8/I-432-1': ('CRC-8/ITU',),
    'CRC-8/MAXIM-DOW': ('CRC-8/MAXIM', 'DOW-CRC'),
    'CRC-8/SMBUS': ('CRC-8',),
    'CRC-8/TECH-3250': ('CRC-8/AES', 'CRC-8/EBU'),
    'CRC-10/ATM': ('CRC-10', 'CRC-10/I-610'),
    'CRC-11/FLEXRAY': ('CRC-11',),
    'CRC-12/DECT': ('CRC-12-X',),
    'CRC-12/UMTS': ('CRC-12/3GPP',),
    'CRC-15/CAN': ('CRC-15',),
    'CRC-16/ARC': ('ARC', 'CRC-16/LHA', 'CRC-IBM'),  # Crc16, but not used for backward compatibility
    'CRC-16/DECT-R': ('R-CRC-16',),
    'CRC-16/DECT-X': ('X-CRC-16',),
    'CRC-16/GENIBUS': ('CRC-16/DARC', 'CRC-16/EPC', 'CRC-16/EPC-C1G2', 'CRC-16/I-CODE'),
    'CRC-16/IBM-3740': ('CRC-16/AUTOSAR', 'CRC-16/CCITT-FALSE'),
    'CRC-16/IBM-SDLC': ('CRC-16/ISO-HDLC', 'CRC-16/ISO-IEC-14443-3-B', 'CRC-16/X-25', 'CRC-B', 'X-25'),
    'CRC-16/ISO-IEC-14443-3-A': ('CRC-A',),
    'CRC-16/KERMIT': ('CRC-16/CCITT', 'CRC-16/CCITT-TRUE', 'CRC-16/V-41-LSB', 'CRC-CCITT', 'KERMIT'),
    'CRC-16/MAXIM-DOW': ('CRC-16/MAXIM',),
    'CRC-16/MODBUS': ('MODBUS',),
    'CRC-16/PROFIBUS': ('CRC-16/IEC-61158-2',),
    'CRC-16/SPI-FUJITSU': ('CRC-16/AUG-CCITT',),
    'CRC-16/UMTS': ('CRC-16/BUYPASS', 'CRC-16/VERIFONE'),
    'CRC-16/XMODEM': ('CRC-16/ACORN', 'CRC-16/LTE', 'CRC-16/V-41-MSB',  'XMODEM', 'ZMODEM'),  # Crc16 only for backward compatibility
    'CRC-24/OPENPGP': ('CRC-24',),
    'CRC-32/AIXM': ('CRC-32Q',),
    'CRC-32/BASE91-D': ('CRC-32D',),
    'CRC-32/BZIP2': ('CRC-32/AAL5', 'CRC-32/DECT-B', 'B-CRC-32'),
    'CRC-32/CKSUM': ('CKSUM', 'CRC-32/POSIX'),
    'CRC-32/ISCSI': ('CRC-32/BASE91-C', 'CRC-32/CASTAGNOLI', 'CRC-32/INTERLAKEN', 'CRC-32C'),
    'CRC-32/ISO-HDLC': ('CRC-32', 'CRC-32/ADCCP', 'CRC-32/V-42', 'CRC-32/XZ', 'PKZIP'),
    'CRC-32/JAMCRC': ('JAMCRC',),
    'CRC-32/XFER': ('XFER',),
    'CRC-64/ECMA-182': ('CRC-64', ),
    'CRC-64/XZ': ('CRC-64/GO-ECMA',),
}

extra_class_aliases = {
    'CRC-16/MCRF4XX': ('Crc16Mcrf4XX', 'Crcc16Mcrf4xx'),
    'CRC-24/OPENPGP': ('Crc24OpenPgp',),
    'CRC-32/AIXM': ('Crc32q',),
    'CRC-32/BASE91-D': ('Crc32d',),
    'CRC-32/ISCSI': ('Crc32c',),
    'CRC-16/XMODEM': ('Crc16',)
}

rCRC = re.compile(r'\s+'.join((
    r'width=(\d+)',
    r'poly=0x([0-9a-fA-F]+)',
    r'init=0x([0-9a-fA-F]+)',
    r'refin=(\S+)',
    r'refout=(\S+)',
    r'xorout=0x([0-9a-fA-F]+)',
    r'check=0x([0-9a-fA-F]+)',
    r'residue=0x([0-9a-fA-F]+)',
    r'name="([^"]*)"',
)))

template = """
class {10}({9}):
    \"\"\"{8}{11}\"\"\"
    _names = ({12})
    _width = {0}
    _poly = 0x{1}
    _initvalue = 0x{2}
    _reflect_input = {3}
    _reflect_output = {4}
    _xor_output = 0x{5}
    _check_result = 0x{6}
    _residue = 0x{7}

"""

urls = (
    r'https://reveng.sourceforge.io/crc-catalogue/1-15.htm',
    r'https://reveng.sourceforge.io/crc-catalogue/16.htm',
    r'https://reveng.sourceforge.io/crc-catalogue/17plus.htm',
)


class OutFile(object):
    def __init__(self, argv, idx):
        try:
            fname = argv[idx]
        except IndexError:
            fname = '-'
        if fname == '-':
            self.fhandle = sys.stdout
        else:
            self.fhandle = open(fname, 'w')

    def __enter__(self):
        return self.fhandle

    def __exit__(self, type, value, traceback):
        if self.fhandle is not sys.stdout:
            self.fhandle.close()


def linejoin(line, length, indent):
    lines = []
    maxlen = length - len(indent)
    try:
        while len(line) > maxlen:
            idx = line.rindex(', ', 0, maxlen)
            lines.append(indent + line[0:idx+1] + '\n')
            line = line[idx+2:]
    except ValueError:
        pass
    lines.append(indent + line + '\n')  # append rest
    return lines


def getclassname(strname):
    if strname in renames:
        return renames[strname]
    return strname.replace('-', ' ').replace('/', ' ').title().replace(' ', '')


def getbaseclass(width):
    return {8: 'Crc8Base', 16: 'Crc16Base', 32: 'Crc32Base'}.get(int(width), 'CrcBase')


if __name__ == "__main__":

    crcs = list()

    with open('../crccheck/crc.py', 'r') as infh:
        crchead = infh.readlines()

    try:
        marker = "# # # CRC CLASSES # # #\n"
        crchead = crchead[:crchead.index(marker)+1]
    except ValueError:
        pass

    for url in urls:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
        for crc in rCRC.findall(data):
            crc = list(crc)
            crc[3] = crc[3].capitalize()
            crc[4] = crc[4].capitalize()
            crc.append(getbaseclass(crc[0]))
            crc.append(getclassname(crc[8]))
            crcs.append(crc)

    crcs.sort(key=lambda x: (int(x[0]), x[10]))

    with OutFile(sys.argv, 1) as outfh:
        crcallaliases = []

        outfh.writelines(crchead)
        outfh.write('\n')

        for crc in crcs:
            name = crc[8]
            clsname = crc[10]
            othernames = aliases.get(name, ())

            if othernames:
                aliasdoc = '\n\n    Aliases: ' + (', '.join(othernames)) + '\n    '
                namelist = [name]
                namelist.extend(othernames)
                names = "'" + ("', '".join(namelist)) + "'"
            else:
                aliasdoc = ''
                names = "'" + name + "',"

            outfh.write(template.format(*crc, aliasdoc, names))
            crcallaliases.append(clsname)

            if name in aliases:
                outfh.write('\n')
                for alias in aliases.get(name, ()):
                    clsalias = getclassname(alias)
                    outfh.write('{} = {}\n'.format(clsalias, clsname))
                    crcallaliases.append(clsalias)
            if name in extra_class_aliases:
                if name not in aliases:
                    outfh.write('\n')
                for clsalias in extra_class_aliases.get(name, ()):
                    outfh.write('{} = {}\n'.format(clsalias, clsname))
                    crcallaliases.append(clsalias)
            if name in aliases or name in extra_class_aliases:
                outfh.write('\n')

        allcls = ", ".join(crc[10] for crc in crcs)
        lines = ['\n', 'ALLCRCCLASSES = (\n']
        lines.extend(linejoin(allcls, 120, ' ' * 4))
        lines.append(')\n')

        allclsalias = ", ".join(crcallaliases)
        lines.extend(['\n', 'ALLCRCCLASSES_ALIASES = (\n'])
        lines.extend(linejoin(allclsalias, 120, ' ' * 4))
        lines.append(')\n')

        for line in lines:
            outfh.write(line)
