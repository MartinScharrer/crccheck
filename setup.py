try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Calculation library for CRCs and checksums',
    'author': 'Martin Scharrer',
    'url': 'https://bitbucket.org/martin_scharrer/crccheck',
    'download_url': 'https://bitbucket.org/martin_scharrer/checksum/downloads/',
    'author_email': 'martin@scharrer-online.de',
    'version': '0.5',
    'install_requires': [],
    'packages': ['crccheck'],
    'scripts': [],
    'name': 'crccheck',
    'license': 'GPL v3+',
    'platforms': 'any',
}

setup(**config)