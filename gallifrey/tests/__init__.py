import logging
import os.path
import pkgutil
import unittest
from PySide.QtGui import QApplication
from .base import GallifreyTest

QT_APP = None


def create_qt_app():
    global QT_APP
    QT_APP = QApplication([])
    return QT_APP


def import_all_tests():
    from gallifrey import tests
    pkgpath = os.path.dirname(tests.__file__)
    modules = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]
    for module in modules:
        __import__('gallifrey.tests.%s' % (module))


def get_all_test_suite():
    create_qt_app()
    import_all_tests()

    logging.basicConfig(level=logging.INFO, format="%(asctime)-15s:%(message)s", filename='test.log')
    logging.getLogger('pymk').info('\n\t*** TESTING STARTED ***')
    suite = unittest.TestLoader()
    prepered_all_test_cases = []
    for test_case in GallifreyTest.tests:
        prepered_all_test_cases.append(
            suite.loadTestsFromTestCase(test_case)
        )
    return unittest.TestSuite(prepered_all_test_cases)
