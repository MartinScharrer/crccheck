try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'crccheck',
    'description': 'Calculation library for CRCs and checksums',
    'author': 'Martin Scharrer',
    'license': 'GPL v3+',
    'packages': ['crccheck', 'tests'],
    'version': '0.5',
    'url': 'https://bitbucket.org/martin_scharrer/crccheck',
    'download_url': 'https://bitbucket.org/martin_scharrer/checksum/downloads/',
    'author_email': 'martin@scharrer-online.de',
    'install_requires': [],
    'tests_require': ['nose', ],
    'classifiers': [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience:: Developers",
        "Intended Audience:: Information Technology",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Utilities",
    ],
}

setup(**config)