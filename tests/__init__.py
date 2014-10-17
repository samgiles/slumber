import os.path
import unittest


def get_tests():
    return full_suite()

def full_suite():
    from .resource import ResourceTestCase
    from .serializer import ResourceTestCase as SerializerTestCase
    from .utils import UtilsTestCase

    resourcesuite = unittest.TestLoader().loadTestsFromTestCase(ResourceTestCase)
    serializersuite = unittest.TestLoader().loadTestsFromTestCase(SerializerTestCase)
    utilssuite = unittest.TestLoader().loadTestsFromTestCase(UtilsTestCase)

    return unittest.TestSuite([resourcesuite, serializersuite, utilssuite])

