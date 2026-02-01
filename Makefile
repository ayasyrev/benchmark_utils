.ONESHELL:
SHELL := /bin/bash
# SRC = $(wildcard Nbs/*.ipynb)

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	uv build

clean:
	rm -rf dist
