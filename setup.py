from setuptools import setup, find_packages
from slumber import __version__, __description__, __url__, __author__, __email__
import sys

install_requires = ["httplib2"]

if sys.version_info < (2, 6):
    install_requires.append("simplejson")


setup(
    name = "slumber",
    version = __version__,
    description = __description__,
    url = __url__,
    author = __author__,
    author_email = __email__,
    packages = find_packages(),
    zip_safe = False,
    install_requires = install_requires,
)