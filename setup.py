# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'pyside',
    'mock',
]

dependency_links = [
]

if __name__ == '__main__':
    setup(name='greentree',
          version='0.1.0',
          description="MVC like design pattern for PySide.",
          author='Dominik "Socek" Długajczyk',
          author_email='msocek@gmail.com',
          packages=find_packages(),
          install_requires=install_requires,
          dependency_links=dependency_links,
          test_suite='greentree.tests.get_all_test_suite',
          )
