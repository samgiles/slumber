import os
from setuptools import setup

install_requires = ["requests"]
tests_require = ["mock"]

base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name = "slumber",
    version = "0.6.1",
    description = "A library that makes consuming a REST API easier and more convenient",
    long_description="\n\n".join([
        open(os.path.join(base_dir, "README.rst"), "r").read(),
        open(os.path.join(base_dir, "CHANGELOG.rst"), "r").read()
    ]),
    url = "http://github.com/samgiles/slumber",
    author = "Donald Stufft",
    author_email = "donald.stufft@gmail.com",
    maintainer = "Samuel Giles",
    maintainer_email = "sam.e.giles@gmail.com",
    packages = ["slumber"],
    zip_safe = False,
    install_requires = install_requires,
    tests_require = tests_require,
    test_suite = "tests.get_tests",
)
