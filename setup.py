#!/usr/bin/env python

from distutils.core import setup

setup(name='yml2tex',
      version='1.1',
      description='Transforms a YAML file into a LaTeX Beamer presentation',
      author='Arthur Koziel',
      author_email='arthur@arthurkoziel.com',
      url='http://code.google.com/p/yml2tex/',
      py_modules=['yml2tex'],
      scripts=['bin/yml2tex'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Topic :: Utilities',
          ],
     )