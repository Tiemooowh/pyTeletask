"""Setup for PyTeletask python package."""
from os import path
from setuptools import find_packages, setup

REQUIRES = []

THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with open(path.join(THIS_DIRECTORY, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

VERSION = {}
# pylint: disable=exec-used
with open(path.join(THIS_DIRECTORY, "teletask/__version__.py"), encoding="utf-8") as fp:
    exec(fp.read(), VERSION)

setup(
    name='pyteletask',
    description='An Asynchronous Library for the Teletask protocol.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    version=VERSION["__version__"],
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
    keywords='teletask ip teletaskdoip doip home automation',
    zip_safe=False)
