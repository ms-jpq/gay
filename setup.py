#!/usr/bin/env python3

from pathlib import Path

from setuptools import setup

setup(
    name="gay",
    python_requires=">=3.7.0",
    version="1.2.10",
    description="Colour your text / terminal to be more gay. 🏳️‍🌈",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="ms-jpq",
    author_email="github@bigly.dog",
    url="https://github.com/ms-jpq/gay",
    packages=[],
    scripts=["gay"],
)
