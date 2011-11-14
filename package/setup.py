#!/usr/bin/env python

from distutils.core import setup

setup(name='django-easyextjs4',
      version='1.0',
      description='Django extension for ExtJS 4',
      author='Christophe Braud',
      author_email='chbperso@gmail.com',
      url='https://github.com/TofPlay/django-easyextjs4',
      packages=['EasyExtJS4'],
      package_dir={'EasyExtJS4':'easyextjs4'},
     classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Web Environment',
              'Intended Audience :: Developers',
              'Operating System :: MacOS :: MacOS X',
              'Operating System :: POSIX',
              'Programming Language :: Python',
              ],
)
