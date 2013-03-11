import unittest


class GallifreyTest(type):
    tests = []

    def __init__(cls, name, bases, dct):
        super(GallifreyTest, cls).__init__(name, bases, dct)
        cls.tests.append(cls)


class BaseTest(unittest.TestCase):
    __metaclass__ = GallifreyTest
