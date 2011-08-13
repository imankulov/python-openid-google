#!/usr/bin/env python
from setuptools import setup
setup(
    name='python-openid-google',
    version='0.1',
    description='Python module supporting Google extensions',
    long_description=(
        'Python module supporting Google extensions. Current '
        'implementation supports OpenID and OAuth Hybrid Extension'),
    author='Roman Imankulov',
    author_email='roman.imankulov@gmail.com',
    url='http://imankulov.name',
    py_modules=['openid_google'],
    install_requires=['python-openid', 'oauth'],
)
