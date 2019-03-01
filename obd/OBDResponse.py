# -*- coding: utf-8 -*-

########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2009 Peter J. Creath                                       #
# Copyright 2016 Brendan Whitfield (brendan-w.com)                     #
#                                                                      #
########################################################################
#                                                                      #
# OBDResponse.py                                                       #
#                                                                      #
# This file is part of python-OBD (a derivative of pyOBD)              #
#                                                                      #
# python-OBD is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 2 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# python-OBD is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with python-OBD.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                      #
########################################################################


import time
from .codes import *

import logging

logger = logging.getLogger(__name__)


class OBDResponse():
    """ Standard response object for any OBDCommand """

    def __init__(self, command=None, messages=None):
        self.command = command
        self.messages = messages if messages else []
        self.value = None
        self.time = time.time()

    @property
    def unit(self):
        # for backwards compatibility
        if isinstance(self.value, Unit.Quantity):
            return str(self.value.u)
        elif self.value == None:
            return None
        else:
            return str(type(self.value))

    def is_null(self):
        return (not self.messages) or (self.value == None)

    def __str__(self):
        return str(self.value)


"""
    Special value types used in OBDResponses
    instantiated in decoders.py
"""


class Status():
    def __init__(self):
        self.MIL = False
        self.DTC_count = 0
        self.ignition_type = ""

        # make sure each test is available by name
        # until real data comes it. This also prevents things from
        # breaking when the user looks up a standard test that's null.
        null_test = StatusTest()
        for name in BASE_TESTS + SPARK_TESTS + COMPRESSION_TESTS:
            if name:  # filter out None/reserved tests
                self.__dict__[name] = null_test


class StatusTest():
    def __init__(self, name="", available=False, complete=False):
        self.name = name
        self.available = available
        self.complete = complete

    def __str__(self):
        a = "Available" if self.available else "Unavailable"
        c = "Complete" if self.complete else "Incomplete"
        return "Test %s: %s, %s" % (self.name, a, c)


class Monitor():
    def __init__(self):
        self._tests = {}  # tid : MonitorTest

        # make the standard TIDs available as null monitor tests
        # until real data comes it. This also prevents things from
        # breaking when the user looks up a standard test that's null.
        null_test = MonitorTest()

        for tid in TEST_IDS:
            name = TEST_IDS[tid][0]
            self.__dict__[name] = null_test
            self._tests[tid] = null_test

    def add_test(self, test):
        self._tests[test.tid] = test
        if test.name is not None:
            self.__dict__[test.name] = test

    @property
    def tests(self):
        return [test for test in self._tests.values() if not test.is_null()]

    def __str__(self):
        if len(self.tests) > 0:
            return "\n".join([str(t) for t in self.tests])
        else:
            return "No tests to report"

    def __len__(self):
        return len(self.tests)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._tests.get(key, MonitorTest())
        elif isinstance(key, str) or isinstance(key, unicode):
            return self.__dict__.get(key, MonitorTest())
        else:
            logger.warning(
                "Monitor test results can only be retrieved by TID value or property name")


class MonitorTest():
    def __init__(self):
        self.tid = None
        self.name = None
        self.desc = None
        self.value = None
        self.min = None
        self.max = None

    @property
    def passed(self):
        if not self.is_null():
            return (self.value >= self.min) and (self.value <= self.max)
        else:
            return False

    def is_null(self):
        return (self.tid is None or
                self.value is None or
                self.min is None or
                self.max is None)

    def __str__(self):
        return "%s : %s [%s]" % (self.desc,
                                 str(self.value),
                                 "PASSED" if self.passed else "FAILED")
