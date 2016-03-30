======
How-to
======


How to quickly calculate a CRC/checksum
=======================================
If only one data buffer needs to be processed a CRC/checksum can be generated quickly using the class method
:meth:`.calc`::

    from crccheck.crc import Crc32
    crc = Crc32.calc(data)

If the result is needed as hexstring or bytes use :meth:`.calchex` or :meth:`.calcbytes`, respectively.



How to calculate over multiple data blocks
==========================================
Create an instance and feed all data blocks to :meth:`.process`.
Once done, use :meth:`.final` to get the final result::

    from crccheck.crc import Crc32
    crcinst = Crc32()
    crcinst.process(data1)
    crcinst.process(data2)
    crcinst.process(data3)
    crc = crcinst.final()

The intermediate value can be read using :meth:`.value` and, if required, set again using :meth:`.init`.



How to use a CRC not implemented by the package
===============================================
The package implements all CRCs listed in the
`Catalogue of parametrised CRC algorithms <http://reveng.sourceforge.net/crc-catalogue/>`_.

The general class :class:`crccheck.crc.Crc` can be used for any other CRCs.
You need to provide the CRC parameters. These are described in detail in the publication
`A paninless guide to CRC error detection alogithms <http://www.ross.net/crc/download/crc_v3.txt>`_.

For advanced users is also possible to create an own subclass. See the source code for details.



How to calculate the CRC or checksum of a file
==============================================

You need to provide an interable over all bytes in the file.
For this `mmap <https://docs.python.org/3.5/library/mmap.html>`_ is recommended::

    from mmap import ACCESS_READ, mmap
    from crccheck.crc import Crc32

    with open("somefile.ext", 'rb') as fh, mmap(fh.fileno(), 0, access=ACCESS_READ) as mm:
        crc = Crc32.calc((b[0] for b in mm))
