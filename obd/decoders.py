
########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2014 Brendan Whitfield (bcw7044@rit.edu)                   #
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
from utils import *
from codes import *

'''
All decoders take the form:

def <name>(_hex):
	...
	return (<value>, <unit>)

'''


# todo
def todo(_hex):
	return (_hex, Unit.NONE)

# hex in, hex out
def noop(_hex):
	return (_hex, Unit.NONE)

# hex in, bitstring out
def pid(_hex):
	v = bitstring(_hex)
	return (v, Unit.NONE)

'''
Sensor decoders
Return Value object with value and units
'''

def count(_hex):
	v = unhex(_hex)
	return (v, Unit.COUNT)

# 0 to 100 %
def percent(_hex):
	v = unhex(_hex[0:2])
	v = v * 100.0 / 255.0
	return (v, Unit.PERCENT)

# -100 to 100 %
def percent_centered(_hex):
	v = unhex(_hex[0:2])
	v = (v - 128) * 100.0 / 128.0
	return (v, Unit.PERCENT)

# -40 to 215 C
def temp(_hex):
	v = unhex(_hex)
	v = v - 40
	return (v, Unit.C)

# -40 to 6513.5 C
def catalyst_temp(_hex):
	v = unhex(_hex)
	v = (v / 10.0) - 40
	return (v, Unit.C)

# -128 to 128 mA
def current_centered(_hex):
	v = unhex(_hex[4:8])
	v = (v / 256.0) - 128
	return (v, Unit.MA)

# 0 to 1.275 volts
def sensor_voltage(_hex):
	v = unhex(_hex[0:2])
	v = v / 200.0
	return (v, Unit.VOLT)

# 0 to 8 volts
def sensor_voltage_big(_hex):
	v = unhex(_hex[4:8])
	v = (v * 8.0) / 65535
	return (v, Unit.VOLT)

# 0 to 765 kPa
def fuel_pressure(_hex):
	v = unhex(_hex)
	v = v * 3
	return (v, Unit.KPA)

# 0 to 255 kPa
def pressure(_hex):
	v = unhex(_hex)
	return (v, Unit.KPA)

# 0 to 5177 kPa
def fuel_pres_vac(_hex):
	v = unhex(_hex)
	v = v * 0.079
	return (v, Unit.KPA)

# 0 to 655,350 kPa
def fuel_pres_direct(_hex):
	v = unhex(_hex)
	v = v * 10
	return (v, Unit.KPA)

# -8192 to 8192 Pa
def evap_pressure(_hex):
	# decode the twos complement
	a = twos_comp(unhex(_hex[0:2]) 8)
	b = twos_comp(unhex(_hex[2:4]) 8)
	v = ((a * 256.0) + b) / 4.0
	return (v, Unit.PA)

# 0 to 327.675 kPa
def abs_evap_pressure(_hex):
	v = unhex(_hex)
	v = v / 200
	return (v, Unit.KPA)

# -32767 to 32768 Pa
def evap_pressure_alt(_hex):
	v = unhex(_hex)
	v = v - 32767
	return (v, Unit.PA)

# 0 to 16,383.75 RPM
def rpm(_hex):
	v = unhex(_hex)
	v = v / 4.0
	return (v, Unit.RPM)

# 0 to 255 KPH
def speed(_hex):
	v = unhex(_hex)
	return (v, Unit.KPH)

# -64 to 63.5 degrees
def timing_advance(_hex):
	v = unhex(_hex)
	v = (v - 128) / 2.0
	return (v, Unit.DEGREES)

# -210 to 301 degrees
def inject_timing(_hex):
	v = unhex(_hex)
	v = (v - 26880) / 128.0
	return (v, Unit.DEGREES)

# 0 to 655.35 grams/sec
def maf(_hex):
	v = unhex(_hex)
	v = v / 100.0
	return (v, Unit.GPS)

# 0 to 2550 grams/sec
def max_maf(_hex):
	v = unhex(_hex[0:2])
	v = v * 10
	return (v, Unit.GPS)

# 0 to 65535 seconds
def seconds(_hex):
	v = unhex(_hex)
	return (v, Unit.SEC)

# 0 to 65535 minutes
def minutes(_hex):
	v = unhex(_hex)
	return (v, Unit.MIN)

# 0 to 65535 km
def distance(_hex):
	v = unhex(_hex)
	return (v, Unit.KM)

# 0 to 3212 Liters/hour
def fuel_rate(_hex):
	v = unhex(_hex)
	v = v * 0.05
	return (v, Unit.LPH)


'''
Special decoders
Return objects, lists, etc
'''



def status(_hex):
	bits = bitstring(_hex, 32)

	output = {}
	output["Check_Engine_Light"] = bitToBool(bits[0])
	output["DTC_Count"]          = unbin(bits[1:8])
	output["Ignition_Type"]      = IGNITION_TYPE[unbin(bits[12])]
	output["Tests"]              = []

	output["Tests"].append(Test("Misfire", \
								bitToBool(bits[15]), \
								bitToBool(bits[11])))

	output["Tests"].append(Test("Fuel System", \
								bitToBool(bits[14]), \
								bitToBool(bits[10])))

	output["Tests"].append(Test("Components", \
								bitToBool(bits[13]), \
								bitToBool(bits[9])))


	# different tests for different ignition types 
	if(output["Ignition_Type"] == IGNITION_TYPE[0]): # spark
		for i in range(8):
			if SPARK_TESTS[i] is not None:

				t = Test(SPARK_TESTS[i], \
						 bitToBool(bits[(2 * 8) + i]), \
						 bitToBool(bits[(3 * 8) + i]))

				output["Tests"].append(t)

	elif(output["Ignition_Type"] == IGNITION_TYPE[1]): # compression
		for i in range(8):
			if COMPRESSION_TESTS[i] is not None:

				t = Test(COMPRESSION_TESTS[i], \
						 bitToBool(bits[(2 * 8) + i]), \
						 bitToBool(bits[(3 * 8) + i]))
				
				output["Tests"].append(t)

	return (output, Unit.NONE)



def fuel_status(_hex):
	v = unhex(_hex[0:2])
	i = int(math.log(v, 2)) # only a single bit should be on

	v = "Error: Unknown fuel status response"

	if i < len(FUEL_STATUS):
		v = FUEL_STATUS[i]

	return (v, Unit.NONE)


def air_status(_hex):
	v = unhex(_hex)
	i = int(math.log(v, 2)) # only a single bit should be on

	v = "Error: Unknown air status response"

	if i < len(AIR_STATUS):
		v = AIR_STATUS[i]

	return (v, Unit.NONE)

def obd_compliance(_hex):
	i = unhex(_hex)

	v = "Error: Unknown OBD compliance response"

	if i < len(OBD_COMPLIANCE):
		v = OBD_COMPLIANCE[i]

	return (v, Unit.NONE) 


def fuel_type(_hex):
	i = unhex(_hex)

	v = "Error: Unknown fuel type response"

	if i < len(FUEL_TYPES):
		v = FUEL_TYPES[i]

	return (v, Unit.NONE)

# Get the description of a DTC
def describeCode(code):
	code.upper()

	v = "Unknown or manufacturer specific code. Consult the internet."

	if DTC.has_key(code):
		v = DTC[code]

	return (v, Unit.NONE)



'''
The following decoders are untested due to lack of a broken car
'''

# converts 2 bytes of hex into a DTC code
def dtc(_hex):
	dtc = ""
	bits = bitstring(_hex[0])

	dtc += ['P', 'C', 'B', 'U'][unbin(bits[0:2])]
	dtc += str(unbin(bits[2:4]))
	dtc += _hex[1:4]

	return (dtc, Unit.NONE)

# converts a frame of 2-byte DTCs into a list of DTCs
def dtc_frame(_hex):
	code_length = 4 # number of hex chars consumed by one code
	size = len(_hex) / code_length # number of codes defined in THIS FRAME (not total)
	codes = []
	for n in range(size):

		start = code_length * n
		end = start + code_length
		
		codes.append(dtc(_hex[start:end]))

	return (codes, Unit.NONE)
