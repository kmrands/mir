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
    'ansible==2.5.0',
    'asn1crypto==0.24.0',
    'bcrypt==3.1.4',
    'bleach==2.1.3',
    'boto3==1.6.18',
    'botocore==1.9.18',
    'Cerberus==0.9.2',
    'certifi==2018.1.18',
    'cffi==1.11.5',
    'chardet==3.0.4',
    'click==6.7',
    'cryptography==2.2.2',
    'docutils==0.14',
    'enum34==1.1.6',
    'Eve==0.7.8',
    'Events==0.2.2',
    'Flask==0.12',
    'Flask-Cors==3.0.3',
    'Flask-PyMongo==0.5.1',
    'funcsigs==1.0.2',
    'futures==3.2.0',
    'gevent==1.2.2',
    'greenlet==0.4.13',
    'gunicorn==19.7.1',
    'html5lib==1.0.1',
    'idna==2.6',
    'ipaddress==1.0.19',
    'itsdangerous==0.24',
    'Jinja2==2.10',
    'jmespath==0.9.3',
    'MarkupSafe==0.23',
    'mock==2.0.0',
    'paramiko==2.4.1',
    'pbr==4.0.0',
    'pyasn1==0.4.2',
    'pycparser==2.18',
    'pycrypto==2.6.1',
    'PyJWT==1.6.1',
    'pymongo==3.6.1',
    'PyNaCl==1.2.1',
    'python-dateutil==2.6.1',
    'PyYAML==3.12',
    'requests==2.18.4',
    's3transfer==0.1.13',
    'simplejson==3.13.2',
    'six==1.11.0',
    'urllib3==1.22',
    'webencodings==0.5.1',
    'Werkzeug==0.11.15',
    'Pillow',
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
    version='1.1.11',
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
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
