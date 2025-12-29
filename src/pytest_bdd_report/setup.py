#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-bdd-report",
    version="1.2.2",
    author="Mattia Monti",
    author_email="mattiamonti2001@gmail.com",
    maintainer="Mattia Monti",
    maintainer_email="mattiamonti2001@gmail.com",
    license="MIT",
    url="https://github.com/mattiamonti/pytest-bdd-report",
    description="A pytest-bdd plugin for generating useful and informative BDD test reports",
    long_description=read("README.rst"),
    py_modules=[
        "pytest_bdd_report",
    ],
    python_requires=">=3.5",
    install_requires=["pytest>=3.5.0", "pytest-bdd"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "pytest11": [
            "bdd-report = pytest_bdd_report",
        ],
    },
)
