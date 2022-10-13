=========
Changelog
=========

v1.3.0 - 2022-10-13
===================
 * Updated unit tests to use correct asserts.
 * Some code quality adjustments.
 * Switched license from GPLv3 to MIT.

v1.2.0 - 2022-10-06
===================
 * Updated with newest CRC from catalogue.
 * Changed project repository from Mercurial to Git.

v1.1.1 - 2022-10-06
===================
 * Switched unit tests from nose to unittest module.

v1.1 - 2021-11-25
=================
 * Fixed ignored byteorder in calchex().
 * Updated documentation.

v1.0 - 2020-09-21
=================
 * Added further CRCs.
 * Fixed missing storage of initial value for general ``Crc`` class. Before ``reset()`` did not work correctly.
 * Updated tests to achieve 100% code coverage.

v0.6 - 2016-04-03
=================
 * Added compatibility with Python 2.7 and 3.3.

v0.5 - 2016-03-30
=================
 * Added general checksum classes Checksum and ChecksumXor.
 * changed ``process()`` to return ``self`` so that calls can be chained.
 * changed ``init()`` to return ``self`` so that calls can be chained.
 * renamed ``init()`` to ``reset()``.
 * Updated documentation.

v0.4 - 2016-03-29
=================
 * Removed arguments startindex and endindex as they are not required.
 * Optimized reflectbitorder().
 * base: Added ``byteorder`` argument to ``calchex()``.
 * Removed outdated code.
 * Added more unit tests.

v0.3 - 2016-03-28
=================
 * Renamed package to ``crccheck`` as old name was taken in PIP.
 * Changed ``bigendian=True/False`` arguments to ``byteorder='big'/'little'``.
 * Added more docstring documentation.
 * Removed outdated code from repository.

v0.2 - 2016-03-27
=================
 * Changes to support Python 3.
 * Code reformatting.
 * Some smaller fixes.
 * Runtime optimisations.

v0.1 - 2015-09-23
=================
 * First version.
