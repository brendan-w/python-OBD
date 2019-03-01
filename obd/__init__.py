# -*- coding: utf-8 -*-

"""
	A serial module for accessing data from a vehicles OBD-II port

	For more documentation, visit:
	http://python-obd.readthedocs.org/en/latest/
"""

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
# __init__.py                                                          #
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

from .__version__ import __version__
from .obd import OBD
from .asynchronous import Async
from .commands import commands
from .OBDCommand import OBDCommand
from .OBDResponse import OBDResponse
from .protocols import ECU
from .utils import scan_serial, OBDStatus
from .UnitsAndScaling import Unit

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

console_handler = logging.StreamHandler()  # sends output to stderr
console_handler.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
logger.addHandler(console_handler)
