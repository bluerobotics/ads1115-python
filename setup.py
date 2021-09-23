#!/usr/bin/env python3

from setuptools import setup

setup(
    name='ads1115',
    version='0.0.1',
    description='ads1115 driver',
    author='Blue Robotics',
    url='https://github.com/bluerobotics/ads1115-python',
    packages=['ads1115'],
    entry_points={
        'console_scripts': [
            'ads1115-test=ads1115.test:main',
            'ads1115-report=ads1115.report:main'
        ],
    },
    package_data={ "ads1115": ["ads1115.meta"]},
    install_requires=['smbus2'],
)
