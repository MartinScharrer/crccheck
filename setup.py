try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Calculation library for checksums and CRCs',
    'author': 'Martin Scharrer',
    'url': 'https://bitbucket.org/martin_scharrer/checksum',
    'download_url': 'https://bitbucket.org/martin_scharrer/checksum/downloads/checksum.zip',
    'author_email': 'martin@scharrer-online.de',
    'version': '0.1',
    'install_requires': [],
    'packages': ['checksum'],
    'scripts': [],
    'name': 'checksum'
}

setup(**config)