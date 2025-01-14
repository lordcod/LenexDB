from setuptools import setup, find_packages


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
    data_files=[('lenexdb', ['FINA_Points_Table_Base_Times.xlsx'])]
)
