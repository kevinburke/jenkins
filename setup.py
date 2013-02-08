#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "jenkins",
    version = "0.1",
    description = "Open Jenkins URLs",
    author = "Kevin Burke",
    author_email = "kev@inburke.com",
    packages = find_packages(),
    py_modules = ['jenkins'],
    entry_points = {
        "console_scripts": [
            "jenkins = jenkins:main",
        ],
    },
    install_requires=[
        'clint',
        'requests'
    ]
)


