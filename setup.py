#!/usr/bin/env python
import os

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []
# https://github.com/PSBPOSAS/dji-asdk-to-python/issues/2
on_rtd = os.environ.get('READTHEDOCS') == 'True'
if not on_rtd:
    with open("requirements.txt", "r") as fh:
        requirements = fh.readlines()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Carlos Tovar",
    author_email='cartovarc@gmail.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    description="Control your DJI drone compatible with DJI Android SDK through Python",
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='dji_asdk_to_python',
    name='dji_asdk_to_python',
    packages=find_packages(include=['dji_asdk_to_python', 'dji_asdk_to_python.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/cartovarc/dji_asdk_to_python',
    version='0.1.0',
    zip_safe=False,
)
