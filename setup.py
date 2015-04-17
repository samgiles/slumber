import os
import sys
from setuptools import setup

install_requires = ["requests"]
tests_require = ["mock", "unittest2"]

base_dir = os.path.dirname(os.path.abspath(__file__))

version = "0.7.0"

if sys.argv[-1] == 'publish':
    os.system("git tag -a %s -m 'v%s'" % (version, version))
    os.system("python setup.py sdist bdist_wheel upload -r pypi")
    print("Published version %s, do `git push --tags` to push new tag to remote" % version)
    sys.exit()

if sys.argv[-1] == 'syncci':
    os.system("panci --to=tox .travis.yml > tox.ini");
    sys.exit();

setup(
    name = "slumber",
    version = version,
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
