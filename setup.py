from setuptools import setup, find_packages
#import os

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
        name='MLOPS_HOTEL_RESERVATION_PROJECT',
        version='0.1',
        author='oluchi',
        packages=find_packages(),
        install_requires=requirements,

    )
