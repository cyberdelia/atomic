# -*- coding: utf-8 -*-
import sys

from setuptools import setup, find_packages, Extension


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

kwargs = {}
if "java" not in sys.version.lower():
    kwargs = dict(ext_modules=[
        Extension("atomic._reference", ["atomic/_reference.c"])
    ])

setup(
    name='atomic',
    version='0.5',
    description='An atomic class that guarantees atomic updates to its contained value.',
    long_description=readme,
    author='Timothée Peignier',
    author_email='timothee.peignier@tryphon.org',
    url='https://github.com/cyberdelia/atomic',
    license=license,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    **kwargs
)
