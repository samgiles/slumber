import os.path
from setuptools import setup, find_packages
import sys

install_requires = ["requests"]

if sys.version_info < (2, 6):
    install_requires.append("simplejson")

base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name = "slumber",
    version = "0.4.2",
    description = "A library that makes consuming a REST API easier and more convenient",
    long_description="\n\n".join([
        open(os.path.join(base_dir, "README.rst"), "r").read(),
        open(os.path.join(base_dir, "CHANGELOG.rst"), "r").read()
    ]),
    url = "http://slumber.in/",
    author = "Donald Stufft",
    author_email = "donald.stufft@gmail.com",
    packages = find_packages(),
    zip_safe = False,
    install_requires = install_requires,
    test_suite = "tests.get_tests",
)
