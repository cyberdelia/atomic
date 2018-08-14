# -*- coding: utf-8 -*-
import io
import os

from setuptools.dist import Distribution
from setuptools import setup, find_packages

try:
    from atomic import ffi
except ImportError:
    ext_modules=[]
else:
    ext_modules=[ffi.verifier.get_extension()]

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

with io.open('README.rst', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='atomic',
    version='0.7.3',
    description='An atomic class that guarantees atomic updates to its contained value.',
    long_description=readme,
    author='Timothée Peignier',
    author_email='timothee.peignier@tryphon.org',
    url='https://github.com/cyberdelia/atomic',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    setup_requires=['cffi'],
    install_requires=['cffi'],
    test_suite="tests",
    ext_modules=ext_modules,
    distclass=BinaryDistribution,
)
