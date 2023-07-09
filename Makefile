MAKEFLAGS += --jobs
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.DELETE_ON_ERROR:
.ONESHELL:
.SHELLFLAGS := -Eeuo pipefail -O dotglob -O nullglob -O extglob -O failglob -O globstar -c

.DEFAULT_GOAL := help

.PHONY: clean clobber lint test build fmt test

clean:
	rm -rf -- .mypy_cache/ *.egg-info/ build/ dist/

clobber: clean
	rm -rf -- .venv/

.venv/bin/python3:
	python3 -m venv -- .venv

.venv/bin/mypy: .venv/bin/python3
	'$<' -m pip install --requirement requirements.dev.txt

lint: .venv/bin/mypy
	'$<' -- .
	'$<' -- ./gay

fmt: .venv/bin/mypy
	.venv/bin/isort --profile=black --gitignore -- . ./gay
	.venv/bin/black -- . ./gay

test:
	./docker/ci.sh

build: .venv/bin/mypy
	.venv/bin/python3 ./setup.py sdist bdist_wheel
