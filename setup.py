from setuptools import setup, find_packages
import slumber
import sys

install_requires = ["httplib2"]

if sys.version_info < (2, 6):
    install_requires.append("simplejson")


setup(
    name = "slumber",
    version = slumber.__version__,
    description = slumber.__description__,
    url = slumber.__url__,
    author = slumber.__author__,
    author_email = slumber.__email__,
    packages = find_packages(),
    zip_safe = False,
    install_requires = install_requires,
)