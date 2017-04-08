#!/usr/bin/env python

"""
Setup script for the Parsley distribution.
"""

from distutils.core import setup
setup(
    name="Parsley",
    version="1.3",
    url="http://launchpad.net/parsley",
    description="Parsing and pattern matching made easy.",
    author="Allen Short",
    author_email="washort42@gmail.com",
    license="MIT License",
    long_description=open("README").read(),
    packages=["ometa", "terml", "ometa._generated", "terml._generated",
              "ometa.test", "terml.test"],
    py_modules=["parsley"],
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Interpreters',
        ],
)
