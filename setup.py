#!/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="obd",
    version="0.6.2",
    description=("Serial module for handling live sensor data from a vehicle's OBD-II port"),
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Topic :: System :: Monitoring",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Topic :: System :: Logging",
        "Intended Audience :: Developers",
    ],
    keywords="obd obdii obd-ii obd2 car serial vehicle diagnostic",
    author="Brendan Whitfield",
    author_email="brendanw@windworksdesign.com",
    url="http://github.com/brendan-w/python-OBD",
    license="GNU GPLv2",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["pyserial==3.*", "pint==0.7.*"],
)
