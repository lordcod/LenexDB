import os
from setuptools import setup, find_packages


def create_list_dir(dir: str):
    return [os.path.join(dir, fn) for fn in os.listdir('lenexdb/meta')]


setup(
    name='lenexdb',
    description='A demo package.',
    version='0.0.1',
    # install_requires=[
    #     'lxml==5.3.0',
    #     'openpyxl==3.1.5'
    # ],
    packages=find_packages(),
    package_dir={'spherical_functions': '.'},
    data_files=[('lenexdb/meta', create_list_dir('lenexdb/meta'))]
)
