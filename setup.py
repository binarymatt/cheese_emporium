from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='cheese_emporium',
      version=version,
      description="static PyPi clone",
      long_description=""" """,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Distribution, pip',
      author='Matt George',
      author_email='matt.george@gmail.com',
      url='',
      license='BSD',
      packages=find_packages(exclude=[]),
      include_package_data=True,
      zip_safe=False,
      install_requires=["flask", "pip", "path.py"],
      entry_points="""
      [console_scripts]
      cheesectl = cheese_emporium.runserver:main

      [paste.app_factory]
      main = cheese_emporium.runserver:make_app
      """,
      )
