#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='ads1115',
    version='0.0.1',
    description='ads1115 driver',
    author='Blue Robotics',
    url='https://github.com/bluerobotics/ads1115-python',
    packages=['ads1115'],
    install_requires=['smbus2'],
)
