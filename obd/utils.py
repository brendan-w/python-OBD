
########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2009 Peter J. Creath                                       #
# Copyright 2015 Brendan Whitfield (bcw7044@rit.edu)                   #
#                                                                      #
########################################################################
#                                                                      #
# utils.py                                                             #
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

import serial
import errno
import string
import time
import glob
import sys
from .debug import debug


class Unit:
    NONE = None
    RATIO = "Ratio"
    COUNT = "Count"
    PERCENT = "%"
    RPM = "RPM"
    VOLT = "Volt"
    F = "F"
    C = "C"
    SEC = "Second"
    MIN = "Minute"
    PA = "Pa"
    KPA = "kPa"
    PSI = "psi"
    KPH = "kph"
    MPH = "mph"
    DEGREES = "Degrees"
    GPS = "Grams per Second"
    MA = "mA"
    KM = "km"
    LPH = "Liters per Hour"


class Response():

    def __init__(self, command=None, raw_data=None):
        self.command = command
        self.raw_data = raw_data
        self.value = None
        self.unit = Unit.NONE
        self.time = time.time()

    def is_null(self):
        return (self.raw_data == None) or (self.value == None)

    def __str__(self):
        return "%s %s" % (str(self.value), str(self.unit))


class Test():

    def __init__(self, name, available, incomplete):
        self.name = name
        self.available = available
        self.incomplete = incomplete

    def __str__(self):
        a = "Available" if self.available else "Unavailable"
        c = "Incomplete" if self.incomplete else "Complete"
        return "Test %s: %s, %s" % (self.name, a, c)


def ascii_to_bytes(a):
    b = []
    for i in range(0, len(a), 2):
        b.append(int(a[i:i + 2], 16))
    return b


def numBitsSet(n):
    # TODO: there must be a better way to do this...
    total = 0
    ref = 1
    for b in range(8):
        total += int(bool(n & ref))
        ref = ref << 1
    return total


def unhex(_hex):
    _hex = "0" if _hex == "" else _hex
    return int(_hex, 16)


def unbin(_bin):
    return int(_bin, 2)


def bitstring(_hex, bits=None):
    b = bin(unhex(_hex))[2:]
    if bits is not None:
        b = ('0' * (bits - len(b))) + b
    return b


def bitToBool(_bit):
    return (_bit == '1')


def twos_comp(val, num_bits):
    """compute the 2's compliment of int value val"""
    if((val & (1 << (num_bits - 1))) != 0):
        val = val - (1 << num_bits)
    return val


def isHex(_hex):
    return all(c in string.hexdigits for c in _hex)


def constrainHex(_hex, b):
    """pads or chops hex to the requested number of bytes"""
    diff = (b * 2) - len(_hex)  # length discrepency in number of hex digits

    if diff > 0:
        debug("Receieved less data than expected, trying to parse anyways...")
        _hex += ('0' * diff)  # pad the right side with zeros
    elif diff < 0:
        debug("Receieved more data than expected, trying to parse anyways...")
        _hex = _hex[:diff]  # chop off the right side to fit

    return _hex


def try_port(portStr):
    """returns boolean for port availability"""
    try:
        s = serial.Serial(portStr)
        s.close()  # explicit close 'cause of delayed GC in java
        return True

    except serial.SerialException:
        pass
    except OSError as e:
        # permit "no such file or directory" errors
        if e.errno != errno.ENOENT:
            raise e

    return False


def scanSerial():
    """scan for available ports. return a list of serial names"""
    available = []

    possible_ports = []

    if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        possible_ports += glob.glob("/dev/rfcomm[0-9]*")
        possible_ports += glob.glob("/dev/ttyUSB[0-9]*")

    elif sys.platform.startswith('win'):
        possible_ports += ["\\.\COM%d" % i for i in range(256)]

    elif sys.platform.startswith('darwin'):
        exclude = [
            '/dev/tty.Bluetooth-Incoming-Port',
            '/dev/tty.Bluetooth-Modem'
        ]
        possible_ports += [
            port for port in glob.glob('/dev/tty.*') if port not in exclude]

    # possible_ports += glob.glob('/dev/pts/[0-9]*') # for obdsim

    for port in possible_ports:
        if try_port(port):
            available.append(port)

    return available
