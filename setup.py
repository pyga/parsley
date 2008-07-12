#!/usr/bin/env python

"""Setup script for the PyMeta distribution."""
from distutils.core import setup
setup(
    name = "PyMeta",
    version = "0.3.0",
    url = "http://launchpad.net/pymeta",
    description = "Pattern-matching language based on OMeta",
    author = "Allen Short",
    author_email = "washort@divmod.com",
    license = "MIT License",
    packages = ["pymeta"]
    )
