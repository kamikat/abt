#!/usr/bin/env python

from setuptools import setup

setup(name="abt",
      version="0.1.0",
      description="BitTorrent workflow with aria2.",
      author="Kamikat",
      author_email="kamikat@banana.moe",
      url="https://github.com/kamikat/abt",
      install_requires=['jsonrpclib', 'better-bencode', 'humanize'],
      packages=["abt"],
      entry_points={
          'console_scripts': [ 'abt = abt:main' ] },
      license="MIT")
