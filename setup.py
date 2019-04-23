# -*- coding: utf-8 -*-

from os.path import join, dirname
from setuptools import setup, find_packages
import sys
import re

version = ""
with open("nos/client/utils.py", "r") as fd:
    version = re.search(r"^VERSION\s*=\s*[\"']([^\"']*)[\"']", fd.read(),
                        re.MULTILINE).group(1)

long_description = ""
with open(join(dirname(__file__), "README.rst"),encoding='utf8') as fd:
    long_description = fd.read().strip()

install_requires = [
    "urllib3>=1.8, <2.0",
    "certifi",
]
tests_require = [
    "nose",
    "coverage",
    "mock",
    "pyaml",
    "nosexcover"
]

setup(
    name="nos-python3-sdk",
    description="NetEase Object Storage SDK For Python3",
    license="MIT License",
    url="https://c.163.com/",
    long_description=long_description,
    version=version,
    author="nos-dev-new",
    author_email="nos-dev@hz.netease.com",
    packages=find_packages(
        where=".",
        exclude=("test_nos*", )
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
    install_requires=install_requires,

    test_suite="test_nos.run_tests.run_all",
    tests_require=tests_require,
)
