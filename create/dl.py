import urllib.request
import re
import sys


aliases = {
    'Crc4G704': ('Crc4Itu',),
    'Crc5EpcC1G2': ('Crc5Epc',),
    'Crc5G704': ('Crc5Itu',),
    'Crc6G704': ('Crc6Itu',),
    'Crc7Mmc': ('Crc7',),
    'Crc8I4321': ('Crc8Itu',),
    'Crc8MaximDow': ('Crc8Maxim', 'CrcDow'),
    'Crc8Smbus': ('Crc8',),
    'Crc8Tech3250': ('Crc8Aes', 'Crc8Ebu'),
    'Crc10Atm': ('Crc10', 'Crc10I610'),
    'Crc11Flexray': ('Crc11',),
    'Crc12Dect': ('Crc12X',),
    'Crc12Umts': ('Crc123Gpp',),
    'Crc15Can': ('Crc15',),
    'Crc16Arc': ('CrcArc', 'Crc16Lha', 'CrcIbm'),  # Crc16, but not used for backward compatibility
    'Crc16Genibus': ('Crc16Darc', 'Crc16Epc', 'CrcEpsC1g2', 'Crc16ICode'),
    'Crc16Ibm3740': ('Crc16Autosar', 'Crc16CcittFalse'),
    'Crc16IbmSdlc': ('Crc16IsoHdlc', 'Crc16IsoIec144433B', 'Crc16X25', 'CrcB', 'CrcX25'),
    'Crc16IsoIec144433A': ('CrcA',),
    'Crc16Kermit': ('Crc16Ccitt', 'Crc16CcittTrue', 'Crc16V41Lsb', 'CrcCcitt', 'CrcKermit'),
    'Crc16MaximDow': ('Crc16Maxim',),
    'Crc16Mcrf4Xx': ('Crc16Mcrf4xx', 'Crcc16Mcrf4xx'),
    'Crc16Modbus': ('CrcModbus',),
    'Crc16Profibus': ('Crc16Iec611582',),
    'Crc16SpiFujitsu': ('Crc16AugCcitt',),
    'Crc16Umts': ('Crc16Buypass', 'Crc16Verifone'),
    'Crc16Xmodem': ('Crc16Acorn', 'Crc16Lte', 'Crc16V41Msb', 'CrcXmodem', 'CrcZmodem', 'Crc16'),  # Crc16 only for backward compatibility
    'Crc24Openpgp': ('Crc24OpenPgp', 'Crc24'),
    'Crc32Aixm': ('Crc32Q', 'Crc32q'),
    'Crc32Base91D': ('Crc32D', 'Crc32d'),
    'Crc32Bzip2': ('Crc32Aal5', 'Crc32DectB', 'Crc32B'),
    'Crc32Cksum': ('CrcCksum', 'Crc32Posix'),
    'Crc32Iscsi': ('Crc32Base91C', 'Crc32Castagnoli', 'Crc32Interlaken', 'Crc32C', 'Crc32c'),
    'Crc32IsoHdlc': ('Crc32Adccp', 'Crc32V42', 'Crc32Xz', 'CrcPkzip', 'Crc32'),
    'Crc32Jamcrc': ('CrcJamcrc',),
    'Crc32Xfer': ('CrcXfer',),
    'Crc64Ecma182': ('Crc64', ),
    'Crc64Xz': ('CrcGoEcma',),
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
    \"\"\"{8}\"\"\"
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


if __name__ == "__main__":

    crcs = list()

    for url in urls:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
        for crc in rCRC.findall(data):
            crc = list(crc)
            crc[3] = crc[3].capitalize()
            crc[4] = crc[4].capitalize()
            base = {8: 'Crc8Base', 16: 'Crc16Base', 32: 'Crc32Base'}.get(int(crc[0]), 'CrcBase')
            classname = crc[8].replace('-', ' ').replace('/', ' ').title().replace(' ', '')
            crc.append(base)
            crc.append(classname)
            crcs.append(crc)

    crcs.sort(key=lambda x: (int(x[0]), x[10]))

    with OutFile(sys.argv, 1) as outfh:
        crcallaliases = []

        with open('crc_head.py', 'r') as infh:
            outfh.write(infh.read())

        outfh.write('\n')

        for crc in crcs:
            outfh.write(template.format(*crc))

            name = crc[10]
            crcallaliases.append(name)
            if name in aliases:
                outfh.write('\n')
                for alias in aliases.get(name, ()):
                    outfh.write('{} = {}\n'.format(alias, name))
                    crcallaliases.append(alias)
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
