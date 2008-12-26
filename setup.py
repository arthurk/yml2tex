#!/usr/bin/env python

from distutils.core import setup

setup(name='yml2tex',
      version='1.2',
      description='Transforms a YAML file into a LaTeX Beamer presentation',
      author='Arthur Koziel',
      author_email='arthur@arthurkoziel.com',
      url='http://code.google.com/p/yml2tex/',
      packages=['yml2tex'],
      scripts=['scripts/yml2tex'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Topic :: Utilities',
          ],
     )