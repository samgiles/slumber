import os.path
import unittest


def get_tests():
    start_dir = os.path.dirname(__file__)
    return unittest.TestLoader().discover(start_dir, pattern="*.py")
