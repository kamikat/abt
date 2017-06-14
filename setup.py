#!/usr/bin/env python

from distutils.core import setup

setup(name="a2torrent",
      version="0.1dev",
      description="BitTorrent workflow with aria2.",
      author="Kamikat",
      author_email="kamikat@banana.moe",
      packages=["abt"],
      entry_points={
          'console_scripts': [ 'abt = abt:main' ] },
      license="MIT")
