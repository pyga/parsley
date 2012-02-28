#!/usr/bin/env python

"""Setup script for the PyMeta distribution."""
from distutils.core import setup
setup(
    name="PyMeta",
    version="0.5.0",
    url="http://launchpad.net/pymeta",
    description="Pattern-matching language based on OMeta",
    long_description=open('README').read(),
    author="Allen Short",
    author_email="washort42@gmail.com",
    license="MIT License",
    packages=["pymeta"]
    )
