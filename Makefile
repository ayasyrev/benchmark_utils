.ONESHELL:
SHELL := /bin/bash
# SRC = $(wildcard Nbs/*.ipynb)

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist