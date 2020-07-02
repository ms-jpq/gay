#!/usr/bin/env python3

from setuptools import setup


def slurp(path: str) -> str:
    with open(path) as fd:
        return fd.read()


setup(
    name="gay",
    version="1.2.0",
    description="Colour your text / terminal to be more gay.",
    long_description=slurp("README.md"),
    long_description_content_type="text/markdown",
    author="ms-jpq",
    author_email="github@bigly.dog",
    url="https://github.com/wrennnnnn/gay",
    scripts=["gay"],
)
