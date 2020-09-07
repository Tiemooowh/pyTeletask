"""Setup for PyTeletask python package."""
from setuptools import find_packages, setup

REQUIRES = []
VERSION = '1.0.1'

setup(
    name='pyteletask',
    description='An Asynchronous Library for the Teletask protocol.',
    version=VERSION,
    # download_url='https://github.com/edisonn/teletask/archive/{}.zip'.format(VERSION),
    # url='http://edisonn.io/teletask',
    author='Timothy DE MEY',
    author_email='timothy.demey@edisonn.io',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    packages=find_packages(),
    install_requires=REQUIRES,
    # python_requires=">=3.5.2",
    keywords='teletask ip teletaskdoip doip home automation',
    zip_safe=False)