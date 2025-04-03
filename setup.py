from setuptools import find_packages, setup
from os import path

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='power_converter',
    packages=find_packages(include=['power_converter', 'power_converter.*']),
    version='0.1.0',
    description='A GUI to aid component selection for DC-DC power converters.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPL-3.0-or-later',
    data_files=[('', ['LICENSE.txt'])],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    author='Vinesh Patel',
    install_requires=[
        'pillow',
        'matplotlib',
        'customtkinter',
        'PyLTSpice',
        'ltspice'
    ],
    setup_requires=['pytest-runner'],
    extras_require={
        'test': ['pytest'],
    },
    test_suite='tests',
    include_package_data=True,
    package_data={
        'power_converter': ['circuit_diagrams/*', 'ltspice_circuits/*'],
    },
)
