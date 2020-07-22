set PYTHONPATH=..
python source/crctable.py > source/crctable.rst
sphinx-apidoc -f -o source ../crccheck
sphinx-build -b html source build
