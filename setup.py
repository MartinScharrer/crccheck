#!/usr/bin/python
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='crccheck',
    description='Calculation library for CRCs and checksums',
    long_description=read("README.rst"),
    author='Martin Scharrer',
    author_email='martin@scharrer-online.de',
    license='GPL v3+',
    packages=['crccheck', 'tests'],
    version='1.0',
    url='https://sourceforge.net/projects/crccheck/',
    download_url='https://sourceforge.net/projects/crccheck/files/',
    install_requires=[],
    tests_require=['nose', ],
    test_suite='nose.collector',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Utilities",
    ],
)

