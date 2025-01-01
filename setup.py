from setuptools import setup, find_packages

setup(
    name='lenexdb',
    description='A demo package.',
    version='0.0.1',
    install_requires=[
        'lxml==5.3.0',
        'openpyxl==3.1.5'
    ],
    packages=find_packages()
)
