#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(name="roundrobin",
      version="0.1",
      description="Round Robin library for python",
      license="MIT",
      author="Mathieu Lecarme",
      url="http://github.com/athoune/roundrobin",
      packages=['roundrobin'],
      package_dir={'': 'src/'},
      keywords= "rrd",
      zip_safe = True)