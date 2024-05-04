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
# decoders.py                                                          #
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

import math
import functools
from .utils import *
from .codes import *
from .OBDResponse import Status, StatusTest, Monitor, MonitorTest
from .UnitsAndScaling import Unit, UAS_IDS

import logging

logger = logging.getLogger(__name__)

'''
All decoders take the form:

def <name>(<list_of_messages>):
    ...
    return <value>

'''


# drop all messages, return None
def drop(_):
    return None


# data in, data out
def noop(messages):
    return messages[0].data


# hex in, bitstring out
def pid(messages):
    d = messages[0].data[2:]
    return BitArray(d)


# returns the raw strings from the ELM
def raw_string(messages):
    return "\n".join([m.raw() for m in messages])


"""
Some decoders are simple and are already implemented in the Units And Scaling
tables (used mainly for Mode 06). The uas() decoder is a wrapper for any
Unit/Scaling in that table, simply to avoid redundant code.
"""


def uas(id_):
    """ get the corresponding decoder for this UAS ID """
    return functools.partial(decode_uas, id_=id_)


def decode_uas(messages, id_):
    d = messages[0].data[2:]  # chop off mode and PID bytes
    return UAS_IDS[id_](d)


"""
General sensor decoders
Return pint Quantities
"""

def count(messages):
    d = messages[0].data[2:]
    v = bytes_to_int(d)
    return v * Unit.count

# 0 to 100 %
def percent(messages):
    d = messages[0].data[2:]
    v = d[0]
    v = v * 100.0 / 255.0
    return v * Unit.percent


# -100 to 100 %
def percent_centered(messages):
    d = messages[0].data[2:]
    v = d[0]
    v = (v - 128) * 100.0 / 128.0
    return v * Unit.percent


# -40 to 215 C
def temp(messages):
    d = messages[0].data[2:]
    v = bytes_to_int(d)
    v = v - 40
    return Unit.Quantity(v, Unit.celsius)  # non-multiplicative unit


# -128 to 128 mA
def current_centered(messages):
    d = messages[0].data[2:]
    v = bytes_to_int(d[2:4])
    v = (v / 256.0) - 128
    return v * Unit.milliampere


# 0 to 1.275 volts
def sensor_voltage(messages):
    d = messages[0].data[2:]
    v = d[0] / 200.0
    return v * Unit.volt


# 0 to 8 volts
def sensor_voltage_big(messages):
    d = messages[0].data[2:]
    v = bytes_to_int(d[2:4])
    v = (v * 8.0) / 65535
    return v * Unit.volt


# 0 to 765 kPa
def fuel_pressure(messages):
    d = messages[0].data[2:]
    v = d[0]
    v = v * 3
    return v * Unit.kilopascal


# 0 to 255 kPa
def pressure(messages):
    d = messages[0].data[2:]
    v = d[0]
    return v * Unit.kilopascal


# -8192 to 8192 Pa
def evap_pressure(messages):
    # decode the twos complement
    d = messages[0].data[2:]
    a = twos_comp(d[0], 8)
    b = twos_comp(d[1], 8)
    v = ((a * 256.0) + b) / 4.0
    return v * Unit.pascal


# 0 to 327.675 kPa
def abs_evap_pressure(messages):
    d = messages[0].data[2:]
    v = bytes_to_int(d)
    v = v / 200.0
    return v * Unit.kilopascal


# -32767 to 32768 Pa
def evap_pressure_alt(messages):
    d = messages[0].data[2:]
    v = bytes_to_int(d)
    v = v - 32767
    return v * Unit.pascal


# -64 to 63.5 degrees
def timing_advance(messages):
    d = messages[0].data[2:]
    v = d[0]
    v = (v - 128) / 2.0
    return v * Unit.degree


# -210 to 301 degrees
def inject_timing(messages):
    d = messages[0].data[2:]
    v = bytes_to_int(d)
    v = (v - 26880) / 128.0
    return v * Unit.degree


# 0 to 2550 grams/sec
def max_maf(messages):
    d = messages[0].data[2:]
    v = d[0]
    v = v * 10
    return v * Unit.gps


# 0 to 3212 Liters/hour
def fuel_rate(messages):
    d = messages[0].data[2:]
    v = bytes_to_int(d)
    v = v * 0.05
    return v * Unit.liters_per_hour


# special bit encoding for PID 13
def o2_sensors(messages):
    d = messages[0].data[2:]
    bits = BitArray(d)
    return (
        (),  # bank 0 is invalid
        tuple(bits[:4]),  # bank 1
        tuple(bits[4:]),  # bank 2
    )


def aux_input_status(messages):
    d = messages[0].data[2:]
    return ((d[0] >> 7) & 1) == 1  # first bit indicate PTO status


# special bit encoding for PID 1D
def o2_sensors_alt(messages):
    d = messages[0].data[2:]
    bits = BitArray(d)
    return (
        (),  # bank 0 is invalid
        tuple(bits[:2]),  # bank 1
        tuple(bits[2:4]),  # bank 2
        tuple(bits[4:6]),  # bank 3
        tuple(bits[6:]),  # bank 4
    )


# 0 to 25700 %
def absolute_load(messages):
    d = messages[0].data[2:]
    v = bytes_to_int(d)
    v *= 100.0 / 255.0
    return v * Unit.percent


def elm_voltage(messages):
    # doesn't register as a normal OBD response,
    # so access the raw frame data
    v = messages[0].frames[0].raw
    # Some ELMs provide float V (for example messages[0].frames[0].raw => u'12.3V'
    v = v.lower()
    v = v.replace('v', '')

    try:
        return float(v) * Unit.volt
    except ValueError:
        logger.warning("Failed to parse ELM voltage")
        return None


'''
Special decoders
Return objects, lists, etc
'''


def status(messages):
    d = messages[0].data[2:]
    bits = BitArray(d)

    #            ┌Components not ready
    #            |┌Fuel not ready
    #            ||┌Misfire not ready
    #            |||┌Spark vs. Compression
    #            ||||┌Components supported
    #            |||||┌Fuel supported
    #  ┌MIL      ||||||┌Misfire supported
    #  |         |||||||
    #  10000011 00000111 11111111 00000000
    #   [# DTC] X        [supprt] [~ready]

    output = Status()
    output.MIL = bits[0]
    output.DTC_count = bits.value(1, 8)
    output.ignition_type = IGNITION_TYPE[int(bits[12])]

    # load the 3 base tests that are always present
    for i, name in enumerate(BASE_TESTS[::-1]):
        t = StatusTest(name, bits[13 + i], not bits[9 + i])
        output.__dict__[name] = t

    # different tests for different ignition types
    if bits[12]:  # compression
        for i, name in enumerate(COMPRESSION_TESTS[::-1]):  # reverse to correct for bit vs. indexing order
            t = StatusTest(name, bits[(2 * 8) + i],
                           not bits[(3 * 8) + i])
            output.__dict__[name] = t

    else:  # spark
        for i, name in enumerate(SPARK_TESTS[::-1]):  # reverse to correct for bit vs. indexing order
            t = StatusTest(name, bits[(2 * 8) + i],
                           not bits[(3 * 8) + i])
            output.__dict__[name] = t

    return output


def fuel_status(messages):
    d = messages[0].data[2:]
    bits = BitArray(d)

    status_1 = ""
    status_2 = ""

    if bits[0:8].count(True) == 1:
        if 7 - bits[0:8].index(True) < len(FUEL_STATUS):
            status_1 = FUEL_STATUS[7 - bits[0:8].index(True)]
        else:
            logger.debug("Invalid response for fuel status (high bits set)")
    else:
        logger.debug("Invalid response for fuel status (multiple/no bits set)")

    if bits[8:16].count(True) == 1:
        if 7 - bits[8:16].index(True) < len(FUEL_STATUS):
            status_2 = FUEL_STATUS[7 - bits[8:16].index(True)]
        else:
            logger.debug("Invalid response for fuel status (high bits set)")
    else:
        logger.debug("Invalid response for fuel status (multiple/no bits set)")

    if not status_1 and not status_2:
        return None
    else:
        return (status_1, status_2)


def air_status(messages):
    d = messages[0].data[2:]
    bits = BitArray(d)

    status = None
    if bits.num_set() == 1:
        status = AIR_STATUS[7 - bits[0:8].index(True)]
    else:
        logger.debug("Invalid response for fuel status (multiple/no bits set)")

    return status


def obd_compliance(messages):
    d = messages[0].data[2:]
    i = d[0]

    v = None

    if i < len(OBD_COMPLIANCE):
        v = OBD_COMPLIANCE[i]
    else:
        logger.debug("Invalid response for OBD compliance (no table entry)")

    return v


def fuel_type(messages):
    d = messages[0].data[2:]
    i = d[0]  # todo, support second fuel system

    v = None

    if i < len(FUEL_TYPES):
        v = FUEL_TYPES[i]
    else:
        logger.debug("Invalid response for fuel type (no table entry)")

    return v


def parse_dtc(_bytes):
    """ converts 2 bytes into a DTC code """

    # check validity (also ignores padding that the ELM returns)
    if (len(_bytes) != 2) or (_bytes == (0, 0)):
        return None

    # BYTES: (16,      35      )
    # HEX:    4   1    2   3
    # BIN:    01000001 00100011
    #         [][][  in hex   ]
    #         | / /
    # DTC:    C0123

    dtc = ['P', 'C', 'B', 'U'][_bytes[0] >> 6]  # the last 2 bits of the first byte
    dtc += str((_bytes[0] >> 4) & 0b0011)  # the next pair of 2 bits. Mask off the bits we read above
    dtc += bytes_to_hex(_bytes)[1:4]

    # pull a description if we have one
    return (dtc, DTC.get(dtc, ""))


def single_dtc(messages):
    """ parses a single DTC from a message """
    d = messages[0].data[2:]
    return parse_dtc(d)


def dtc(messages):
    """ converts a frame of 2-byte DTCs into a list of DTCs """
    codes = []
    d = []
    for message in messages:
        d += message.data[2:]  # remove the mode and DTC_count bytes

    # look at data in pairs of bytes
    # looping through ENDING indices to avoid odd (invalid) code lengths
    for n in range(1, len(d), 2):

        # parse the code
        dtc = parse_dtc((d[n - 1], d[n]))

        if dtc is not None:
            codes.append(dtc)

    return codes


def parse_monitor_test(d, mon):
    test = MonitorTest()

    tid = d[1]

    if tid in TEST_IDS:
        test.name = TEST_IDS[tid][0]  # lookup the name from the table
        test.desc = TEST_IDS[tid][1]  # lookup the description from the table
    else:
        logger.debug("Encountered unknown Test ID")
        test.name = "Unknown"
        test.desc = "Unknown"

    uas = UAS_IDS.get(d[2], None)

    # if we can't decode the value, abort
    if uas is None:
        logger.debug("Encountered unknown Units and Scaling ID")
        return None

    # load the test results
    test.tid = tid
    test.value = uas(d[3:5])  # convert bytes to actual values
    test.min = uas(d[5:7])
    test.max = uas(d[7:])

    return test


def monitor(messages):
    d = messages[0].data[1:]
    # only dispose of the mode byte. Leave the MID
    # even though we never use the MID byte, it may
    # show up multiple times. Thus, keeping it make
    # for easier parsing.
    mon = Monitor()

    # test that we got the right number of bytes
    extra_bytes = len(d) % 9

    if extra_bytes != 0:
        logger.debug("Encountered monitor message with non-multiple of 9 bytes. Truncating...")
        d = d[:len(d) - extra_bytes]

    # look at data in blocks of 9 bytes (one test result)
    for n in range(0, len(d), 9):
        # extract the 9 byte block, and parse a new MonitorTest
        test = parse_monitor_test(d[n:n + 9], mon)
        if test is not None:
            mon.add_test(test)

    return mon


def encoded_string(length):
    """ Extract an encoded string from multi-part messages """
    return functools.partial(decode_encoded_string, length=length)


def decode_encoded_string(messages, length):
    d = messages[0].data[2:]

    if len(d) < length:
        logger.debug("Invalid string {}. Discarding...", d)
        return None

    # Encoded strings come in bundles of messages with leading null values to
    # pad out the string to the next full message size. We strip off the
    # leading null characters here and return the resulting string.
    return d.strip().strip(b'\x00' b'\x01' b'\x02' b'\\x00' b'\\x01' b'\\x02')


def cvn(messages):
    d = decode_encoded_string(messages, 4)
    if d is None:
        return None
    return bytes_to_hex(d)
