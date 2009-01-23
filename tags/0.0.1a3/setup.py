import os
from setuptools import setup, find_packages

setup(
    name="lovely.jsonrpc",
    version="0.0.1a3",
    packages=find_packages('src'),
    package_dir = {'':'src'},
    zip_safe = True,
    include_package_data = False,
    namespace_packages = ['lovely'],
    install_requires = ['setuptools'],
    extras_require = dict(
                          test=['zope.testing', 'simplejson'],
                          ),
    )
