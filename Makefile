
.PHONY: all test dist sdist bdist bdist_wheel clean upload

all: test

test:
	@python -m coverage run -m unittest discover
	@python -m coverage report
	@python -m coverage html
    
dist: sdist bdist_wheel

sdist:
	@python setup.py sdist

bdist: bdist_wheel

bdist_wheel:
	@python setup.py bdist_wheel

clean:
	@${RM} -rf dist bdist build */__pycache__ */*.pyc *.egg-info coverage_html_report
