#!/usr/bin/env python

from os.path import exists

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='django-multi-tenant',
    version='1.3',
    author='Cristian Restrepo',
    author_email='cristian.restrepo26@gmail.com',
    packages=[
        'multi_tenant',
        'multi_tenant.migration_executors',
        'multi_tenant.postgresql_backend',
        'multi_tenant.management',
        'multi_tenant.management.commands'
    ],
    scripts=[],
    url='https://smartyapp.co',
    license='MIT',
    description='Tenant support for Django using PostgreSQL schemas.',
    long_description=open('README.rst').read() if exists("README.rst") else "",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=[
        'Django >= 1.8.0',
        'django-tenant-schemas'
    ],
    zip_safe=False,
)
