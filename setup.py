#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'Eve',
    'bcrypt',
    'pycrypto',
    'requests',
    'bleach',
    'boto3',
    'flask-cors',
    'bucketstore',
    'gunicorn',
    'jinja2',
    'cloudinary',
    'ansible',
    # TODO: Put package requirements here
]

setup_requirements = [
    # TODO(spbrien): Put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: Put package test requirements here
]

setup(
    name='mir',
    version='0.1.0',
    description="Mir API Framework",
    long_description=readme + '\n\n' + history,
    author="Steven Brien",
    author_email='spbrien@gmail.com',
    url='https://github.com/spbrien/mir',
    packages=find_packages(include=['mir']),
    entry_points={
        'console_scripts': [
            'mir=mir.cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.*', '.*', '**/*.*', '**/.*'],
    },
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='mir',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
