#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''setup script for imgwrench.'''

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'Pillow>=5.0']

setup_requirements = []

test_requirements = []

setup(
    author='luphord',
    author_email='luphord@protonmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='A command line tool for my image processing needs.',
    entry_points={
        'console_scripts': [
            'imgwrench=imgwrench:cli_imgwrench',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='imgwrench',
    name='imgwrench',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/luphord/imgwrench',
    version='0.7.1',
    zip_safe=False,
)
