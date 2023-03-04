###################################################################################################
# License:
#  MIT License
#
#  Copyright (c) 2015-2022 by Martin Scharrer <martin.scharrer@web.de>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#  and associated documentation files (the "Software"), to deal in the Software without
#  restriction, including without limitation the rights to use, copy, modify, merge, publish,
#  distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or
#  substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#  BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
###################################################################################################

.PHONY: all test Install plugins dist clean doc release

all: test

test:
	@echo ""; echo "Running tests:"
	@python -m coverage run --branch -m unittest discover
	@python -m coverage report
	@python -m coverage html

coverage: test

dist: test
	@python -m build


clean:
	@${RM} -rf dist bdist build */__pycache__ */*.pyc *.egg-info coverage_html_report


doc:
	@echo ""; echo "Extracting documentation:"
	@cd docs/; export PYTHONPATH=..; python ../create/crctable.py > source/crctable.rst
	@cd docs/; sphinx-apidoc -f -o source ../crccheck
	@cd docs/; sphinx-build -b html source build


update:
	@test -z "$$(git status --porcelain crccheck/crc.py)" || (echo "crccheck/crc.py has uncommitted changes. Aborting!" && exit 1)
	@cd create/; python dl.py ../crccheck/crc.py
	@test -z "$$(git status --porcelain crccheck/crc.py)" || echo "crccheck/crc.py has been updated."


release: clean test doc dist

