#!/usr/bin/env python

"""
Setup script for the Parsley distribution.
"""

from distutils.core import setup
setup(
    name="Parsley",
    version="1.0pre2",
    url="http://launchpad.net/parsley",
    description="Pattern-matching language based on OMeta",
    long_description=open('README').read(),
    author="Allen Short",
    author_email="washort42@gmail.com",
    license="MIT License",
    packages=["ometa", "terml"],
    py_modules=["parsley"]
    )
