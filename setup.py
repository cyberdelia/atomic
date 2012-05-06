# -*- coding: utf-8 -*-
from setuptools import setup, find_packages, Extension


setup(
    name='atomic',
    version='0.3.2',
    description='An atomic class that guarantees atomic updates to its contained value.',
    author='Timothée Peignier',
    author_email='timothee.peignier@tryphon.org',
    url='https://github.com/cyberdelia/atomic',
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
    ext_modules=[
        Extension("reference", ["atomic/reference.c"])
    ]
)
