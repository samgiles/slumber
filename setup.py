from setuptools import setup, find_packages
import sys

install_requires = ["httplib2"]

if sys.version_info < (2, 6):
    install_requires.append("simplejson")

setup(
    name = "slumber",
    version = "0.1.3",
    description = "A library that makes consuming a ReST API easier and more convenient",
    long_description=open("README.rst", "r").read(),
    url = "http://slumber.in/",
    author = "Donald Stufft",
    author_email = "donald.stufft@gmail.com",
    packages = find_packages(),
    zip_safe = False,
    install_requires = install_requires,
)