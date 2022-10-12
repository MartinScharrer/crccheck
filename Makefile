
.PHONY: all test dist sdist bdist bdist_wheel clean upload doc release

all: test

test:
	@echo ""; echo "Running tests:"
	@python -m coverage run -m unittest discover
	@python -m coverage report --omit="*/test*"
	@python -m coverage html --omit="*/test*"
    
dist: sdist bdist_wheel

sdist:
	@python setup.py sdist

bdist: bdist_wheel

bdist_wheel:
	@python setup.py bdist_wheel

clean:
	@${RM} -rf dist bdist build */__pycache__ */*.pyc *.egg-info coverage_html_report


doc:
	@echo ""; echo "Extracting documentation:"
	@cd docs/; export PYTHONPATH=..; python ../create/crctable.py > source/crctable.rst
	@cd docs/; sphinx-apidoc -f -o source ../crccheck
	@cd docs/; sphinx-build -b html source build


update:
	@test -z "$$(git status --porcelain crccheck/crc.py)" || (echo "crccheck/crc.py has uncommitted changes. Aborting!" && exit 1)
	@cd create/; python dl.py > ../crccheck/crc.py
	@test -z "$$(git status --porcelain crccheck/crc.py)" || echo "crccheck/crc.py has been updated."


release: clean test doc dist

