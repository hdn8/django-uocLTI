# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-uocLTI',
    version='0.1.0',
    author=u'Nathaniel Finney',
    author_email='nfinney@uoc.edu',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/django-uocLTI',
    license='MIT licence, see LICENCE.txt',
    description='An IMS-LTI provider interface for django apps using the ims_lti_py library, created for use within the Universitat Obert de Catalunya' + \
                ' UOC - nfinney 2013',
    long_description=open('README.txt').read(),
    zip_safe=False,
    install_requires=[
        "Django >= 1.4,< 1.5",
        "ims-lti-py == 0.6",
    ],
)

