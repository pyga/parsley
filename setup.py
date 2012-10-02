#!/usr/bin/env python

"""
Setup script for the Parsley distribution.
"""

from distutils.core import setup
setup(
    name="Parsley",
    version="1.0",
    url="http://launchpad.net/parsley",
    description="Parsing and pattern matching made easy.",
    author="Allen Short",
    author_email="washort42@gmail.com",
    license="MIT License",
    long_description=open("README").read(),
    packages=["ometa", "terml"],
    py_modules=["parsley"]
    )
