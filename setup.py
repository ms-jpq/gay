#!/usr/bin/env python3

from setuptools import setup


def slurp(path: str) -> str:
    with open(path) as fd:
        return fd.read()


setup(
    name="gay",
    python_requires=">=3.7.0",
    version="1.2.8",
    description="Colour your text / terminal to be more gay. 🏳️‍🌈",
    long_description=slurp("README.md"),
    long_description_content_type="text/markdown",
    author="ms-jpq",
    author_email="github@bigly.dog",
    url="https://github.com/ms-jpq/gay",
    scripts=["gay"],
)
