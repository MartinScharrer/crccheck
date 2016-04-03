=========
Changelog
=========

v1.0 - pending
==============
 * Fixed missing storage of initial value for general ``Crc`` class. Before ``reset()`` did not work correctly.
 * Updated tests to achieve 100% code coverage.

v0.6 - 03.04.2016
=================
 * Added compatibility with Python 2.7 and 3.3.

v0.5 - 30.03.2016
=================
 * Added general checksum classes Checksum and ChecksumXor.
 * changed ``process()`` to return ``self`` so that calls can be chained.
 * changed ``init()`` to return ``self`` so that calls can be chained.
 * renamed ``init()`` to ``reset()``.
 * Updated documentation.

v0.4 - 29.03.2016
=================
 * Removed arguments startindex and endindex as they are not required.
 * Optimized reflectbitorder().
 * base: Added ``byteorder`` argument to ``calchex()``.
 * Removed outdated code.
 * Added more unit tests.

v0.3 - 28.03.2016
=================
 * Renamed package to ``crccheck`` as old name was taken in PIP.
 * Changed ``bigendian=True/False`` arguments to ``byteorder='big'/'little'``.
 * Added more docstring documentation.
 * Removed outdated code from repository.

v0.2 - 27.03.2016
=================
 * Changes to support Python 3.
 * Code reformatting.
 * Some smaller fixes.
 * Runtime optimisations.

v0.1 - 23.09.2015
=================
 * First version.
