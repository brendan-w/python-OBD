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
# commands.py                                                          #
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

import logging

from .OBDCommand import OBDCommand
from .decoders import *
from .protocols import ECU

logger = logging.getLogger(__name__)

# flake8: noqa
'''
Define command tables
'''

# NOTE: the NAME field will be used as the dict key for that sensor
# NOTE: commands MUST be in PID order, one command per PID (for fast lookup using __mode1__[pid])

# see OBDCommand.py for descriptions & purposes for each of these fields

__mode1__ = [
    #                      name                             description                    cmd  bytes       decoder           ECU       fast
    OBDCommand("PIDS_A"                     , "Supported PIDs [01-20]"                  , b"0100", 6, pid,                   ECU.ENGINE, True),
    OBDCommand("STATUS"                     , "Status since DTCs cleared"               , b"0101", 6, status,                ECU.ENGINE, True),
    OBDCommand("FREEZE_DTC"                 , "DTC that triggered the freeze frame"     , b"0102", 4, single_dtc,            ECU.ENGINE, True),
    OBDCommand("FUEL_STATUS"                , "Fuel System Status"                      , b"0103", 4, fuel_status,           ECU.ENGINE, True),
    OBDCommand("ENGINE_LOAD"                , "Calculated Engine Load"                  , b"0104", 3, percent,               ECU.ENGINE, True),
    OBDCommand("COOLANT_TEMP"               , "Engine Coolant Temperature"              , b"0105", 3, temp,                  ECU.ENGINE, True),
    OBDCommand("SHORT_FUEL_TRIM_1"          , "Short Term Fuel Trim - Bank 1"           , b"0106", 3, percent_centered,      ECU.ENGINE, True),
    OBDCommand("LONG_FUEL_TRIM_1"           , "Long Term Fuel Trim - Bank 1"            , b"0107", 3, percent_centered,      ECU.ENGINE, True),
    OBDCommand("SHORT_FUEL_TRIM_2"          , "Short Term Fuel Trim - Bank 2"           , b"0108", 3, percent_centered,      ECU.ENGINE, True),
    OBDCommand("LONG_FUEL_TRIM_2"           , "Long Term Fuel Trim - Bank 2"            , b"0109", 3, percent_centered,      ECU.ENGINE, True),
    OBDCommand("FUEL_PRESSURE"              , "Fuel Pressure"                           , b"010A", 3, fuel_pressure,         ECU.ENGINE, True),
    OBDCommand("INTAKE_PRESSURE"            , "Intake Manifold Pressure"                , b"010B", 3, pressure,              ECU.ENGINE, True),
    OBDCommand("RPM"                        , "Engine RPM"                              , b"010C", 4, uas(0x07),             ECU.ENGINE, True),
    OBDCommand("SPEED"                      , "Vehicle Speed"                           , b"010D", 3, uas(0x09),             ECU.ENGINE, True),
    OBDCommand("TIMING_ADVANCE"             , "Timing Advance"                          , b"010E", 3, timing_advance,        ECU.ENGINE, True),
    OBDCommand("INTAKE_TEMP"                , "Intake Air Temp"                         , b"010F", 3, temp,                  ECU.ENGINE, True),
    OBDCommand("MAF"                        , "Air Flow Rate (MAF)"                     , b"0110", 4, uas(0x27),             ECU.ENGINE, True),
    OBDCommand("THROTTLE_POS"               , "Throttle Position"                       , b"0111", 3, percent,               ECU.ENGINE, True),
    OBDCommand("AIR_STATUS"                 , "Secondary Air Status"                    , b"0112", 3, air_status,            ECU.ENGINE, True),
    OBDCommand("O2_SENSORS"                 , "O2 Sensors Present"                      , b"0113", 3, o2_sensors,            ECU.ENGINE, True),
    OBDCommand("O2_B1S1"                    , "O2: Bank 1 - Sensor 1 Voltage"           , b"0114", 4, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B1S2"                    , "O2: Bank 1 - Sensor 2 Voltage"           , b"0115", 4, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B1S3"                    , "O2: Bank 1 - Sensor 3 Voltage"           , b"0116", 4, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B1S4"                    , "O2: Bank 1 - Sensor 4 Voltage"           , b"0117", 4, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B2S1"                    , "O2: Bank 2 - Sensor 1 Voltage"           , b"0118", 4, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B2S2"                    , "O2: Bank 2 - Sensor 2 Voltage"           , b"0119", 4, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B2S3"                    , "O2: Bank 2 - Sensor 3 Voltage"           , b"011A", 4, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B2S4"                    , "O2: Bank 2 - Sensor 4 Voltage"           , b"011B", 4, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("OBD_COMPLIANCE"             , "OBD Standards Compliance"                , b"011C", 3, obd_compliance,        ECU.ENGINE, True),
    OBDCommand("O2_SENSORS_ALT"             , "O2 Sensors Present (alternate)"          , b"011D", 3, o2_sensors_alt,        ECU.ENGINE, True),
    OBDCommand("AUX_INPUT_STATUS"           , "Auxiliary input status (power take off)" , b"011E", 3, aux_input_status,      ECU.ENGINE, True),
    OBDCommand("RUN_TIME"                   , "Engine Run Time"                         , b"011F", 4, uas(0x12),             ECU.ENGINE, True),

    #                      name                             description                    cmd  bytes       decoder           ECU       fast
    OBDCommand("PIDS_B"                     , "Supported PIDs [21-40]"                  , b"0120", 6, pid,                   ECU.ENGINE, True),
    OBDCommand("DISTANCE_W_MIL"             , "Distance Traveled with MIL on"           , b"0121", 4, uas(0x25),             ECU.ENGINE, True),
    OBDCommand("FUEL_RAIL_PRESSURE_VAC"     , "Fuel Rail Pressure (relative to vacuum)" , b"0122", 4, uas(0x19),             ECU.ENGINE, True),
    OBDCommand("FUEL_RAIL_PRESSURE_DIRECT"  , "Fuel Rail Pressure (direct inject)"      , b"0123", 4, uas(0x1B),             ECU.ENGINE, True),
    OBDCommand("O2_S1_WR_VOLTAGE"           , "02 Sensor 1 WR Lambda Voltage"           , b"0124", 6, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S2_WR_VOLTAGE"           , "02 Sensor 2 WR Lambda Voltage"           , b"0125", 6, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S3_WR_VOLTAGE"           , "02 Sensor 3 WR Lambda Voltage"           , b"0126", 6, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S4_WR_VOLTAGE"           , "02 Sensor 4 WR Lambda Voltage"           , b"0127", 6, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S5_WR_VOLTAGE"           , "02 Sensor 5 WR Lambda Voltage"           , b"0128", 6, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S6_WR_VOLTAGE"           , "02 Sensor 6 WR Lambda Voltage"           , b"0129", 6, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S7_WR_VOLTAGE"           , "02 Sensor 7 WR Lambda Voltage"           , b"012A", 6, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S8_WR_VOLTAGE"           , "02 Sensor 8 WR Lambda Voltage"           , b"012B", 6, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("COMMANDED_EGR"              , "Commanded EGR"                           , b"012C", 3, percent,               ECU.ENGINE, True),
    OBDCommand("EGR_ERROR"                  , "EGR Error"                               , b"012D", 3, percent_centered,      ECU.ENGINE, True),
    OBDCommand("EVAPORATIVE_PURGE"          , "Commanded Evaporative Purge"             , b"012E", 3, percent,               ECU.ENGINE, True),
    OBDCommand("FUEL_LEVEL"                 , "Fuel Level Input"                        , b"012F", 3, percent,               ECU.ENGINE, True),
    OBDCommand("WARMUPS_SINCE_DTC_CLEAR"    , "Number of warm-ups since codes cleared"  , b"0130", 3, uas(0x01),             ECU.ENGINE, True),
    OBDCommand("DISTANCE_SINCE_DTC_CLEAR"   , "Distance traveled since codes cleared"   , b"0131", 4, uas(0x25),             ECU.ENGINE, True),
    OBDCommand("EVAP_VAPOR_PRESSURE"        , "Evaporative system vapor pressure"       , b"0132", 4, evap_pressure,         ECU.ENGINE, True),
    OBDCommand("BAROMETRIC_PRESSURE"        , "Barometric Pressure"                     , b"0133", 3, pressure,              ECU.ENGINE, True),
    OBDCommand("O2_S1_WR_CURRENT"           , "02 Sensor 1 WR Lambda Current"           , b"0134", 6, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S2_WR_CURRENT"           , "02 Sensor 2 WR Lambda Current"           , b"0135", 6, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S3_WR_CURRENT"           , "02 Sensor 3 WR Lambda Current"           , b"0136", 6, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S4_WR_CURRENT"           , "02 Sensor 4 WR Lambda Current"           , b"0137", 6, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S5_WR_CURRENT"           , "02 Sensor 5 WR Lambda Current"           , b"0138", 6, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S6_WR_CURRENT"           , "02 Sensor 6 WR Lambda Current"           , b"0139", 6, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S7_WR_CURRENT"           , "02 Sensor 7 WR Lambda Current"           , b"013A", 6, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S8_WR_CURRENT"           , "02 Sensor 8 WR Lambda Current"           , b"013B", 6, current_centered,      ECU.ENGINE, True),
    OBDCommand("CATALYST_TEMP_B1S1"         , "Catalyst Temperature: Bank 1 - Sensor 1" , b"013C", 4, uas(0x16),             ECU.ENGINE, True),
    OBDCommand("CATALYST_TEMP_B2S1"         , "Catalyst Temperature: Bank 2 - Sensor 1" , b"013D", 4, uas(0x16),             ECU.ENGINE, True),
    OBDCommand("CATALYST_TEMP_B1S2"         , "Catalyst Temperature: Bank 1 - Sensor 2" , b"013E", 4, uas(0x16),             ECU.ENGINE, True),
    OBDCommand("CATALYST_TEMP_B2S2"         , "Catalyst Temperature: Bank 2 - Sensor 2" , b"013F", 4, uas(0x16),             ECU.ENGINE, True),

    #                      name                             description                    cmd  bytes       decoder           ECU       fast
    OBDCommand("PIDS_C"                     , "Supported PIDs [41-60]"                  , b"0140", 6, pid,                   ECU.ENGINE, True),
    OBDCommand("STATUS_DRIVE_CYCLE"         , "Monitor status this drive cycle"         , b"0141", 6, status,                ECU.ENGINE, True),
    OBDCommand("CONTROL_MODULE_VOLTAGE"     , "Control module voltage"                  , b"0142", 4, uas(0x0B),             ECU.ENGINE, True),
    OBDCommand("ABSOLUTE_LOAD"              , "Absolute load value"                     , b"0143", 4, absolute_load,         ECU.ENGINE, True),
    OBDCommand("COMMANDED_EQUIV_RATIO"      , "Commanded equivalence ratio"             , b"0144", 4, uas(0x1E),             ECU.ENGINE, True),
    OBDCommand("RELATIVE_THROTTLE_POS"      , "Relative throttle position"              , b"0145", 3, percent,               ECU.ENGINE, True),
    OBDCommand("AMBIANT_AIR_TEMP"           , "Ambient air temperature"                 , b"0146", 3, temp,                  ECU.ENGINE, True),
    OBDCommand("THROTTLE_POS_B"             , "Absolute throttle position B"            , b"0147", 3, percent,               ECU.ENGINE, True),
    OBDCommand("THROTTLE_POS_C"             , "Absolute throttle position C"            , b"0148", 3, percent,               ECU.ENGINE, True),
    OBDCommand("ACCELERATOR_POS_D"          , "Accelerator pedal position D"            , b"0149", 3, percent,               ECU.ENGINE, True),
    OBDCommand("ACCELERATOR_POS_E"          , "Accelerator pedal position E"            , b"014A", 3, percent,               ECU.ENGINE, True),
    OBDCommand("ACCELERATOR_POS_F"          , "Accelerator pedal position F"            , b"014B", 3, percent,               ECU.ENGINE, True),
    OBDCommand("THROTTLE_ACTUATOR"          , "Commanded throttle actuator"             , b"014C", 3, percent,               ECU.ENGINE, True),
    OBDCommand("RUN_TIME_MIL"               , "Time run with MIL on"                    , b"014D", 4, uas(0x34),             ECU.ENGINE, True),
    OBDCommand("TIME_SINCE_DTC_CLEARED"     , "Time since trouble codes cleared"        , b"014E", 4, uas(0x34),             ECU.ENGINE, True),
    OBDCommand("MAX_VALUES"                 , "Various Max values"                      , b"014F", 6, drop,                  ECU.ENGINE, True), # todo: decode this
    OBDCommand("MAX_MAF"                    , "Maximum value for mass air flow sensor"  , b"0150", 6, max_maf,               ECU.ENGINE, True),
    OBDCommand("FUEL_TYPE"                  , "Fuel Type"                               , b"0151", 3, fuel_type,             ECU.ENGINE, True),
    OBDCommand("ETHANOL_PERCENT"            , "Ethanol Fuel Percent"                    , b"0152", 3, percent,               ECU.ENGINE, True),
    OBDCommand("EVAP_VAPOR_PRESSURE_ABS"    , "Absolute Evap system Vapor Pressure"     , b"0153", 4, abs_evap_pressure,     ECU.ENGINE, True),
    OBDCommand("EVAP_VAPOR_PRESSURE_ALT"    , "Evap system vapor pressure"              , b"0154", 4, evap_pressure_alt,     ECU.ENGINE, True),
    OBDCommand("SHORT_O2_TRIM_B1"           , "Short term secondary O2 trim - Bank 1"   , b"0155", 4, percent_centered,      ECU.ENGINE, True), # todo: decode seconds value for banks 3 and 4
    OBDCommand("LONG_O2_TRIM_B1"            , "Long term secondary O2 trim - Bank 1"    , b"0156", 4, percent_centered,      ECU.ENGINE, True),
    OBDCommand("SHORT_O2_TRIM_B2"           , "Short term secondary O2 trim - Bank 2"   , b"0157", 4, percent_centered,      ECU.ENGINE, True),
    OBDCommand("LONG_O2_TRIM_B2"            , "Long term secondary O2 trim - Bank 2"    , b"0158", 4, percent_centered,      ECU.ENGINE, True),
    OBDCommand("FUEL_RAIL_PRESSURE_ABS"     , "Fuel rail pressure (absolute)"           , b"0159", 4, uas(0x1B),             ECU.ENGINE, True),
    OBDCommand("RELATIVE_ACCEL_POS"         , "Relative accelerator pedal position"     , b"015A", 3, percent,               ECU.ENGINE, True),
    OBDCommand("HYBRID_BATTERY_REMAINING"   , "Hybrid battery pack remaining life"      , b"015B", 3, percent,               ECU.ENGINE, True),
    OBDCommand("OIL_TEMP"                   , "Engine oil temperature"                  , b"015C", 3, temp,                  ECU.ENGINE, True),
    OBDCommand("FUEL_INJECT_TIMING"         , "Fuel injection timing"                   , b"015D", 4, inject_timing,         ECU.ENGINE, True),
    OBDCommand("FUEL_RATE"                  , "Engine fuel rate"                        , b"015E", 4, fuel_rate,             ECU.ENGINE, True),
    OBDCommand("EMISSION_REQ"               , "Designed emission requirements"          , b"015F", 3, drop,                  ECU.ENGINE, True),
    OBDCommand("CUSTOM_ABS"                 , "Anti-Lock Breaking System"               , b"213D", 4, count,                 ECU.ENGINE, True),
]

# mode 2 is the same as mode 1, but returns values from when the DTC occured
__mode2__ = []
for c in __mode1__:
    c = c.clone()
    c.command = b"02" + c.command[2:]  # change the mode: 0100 ---> 0200
    c.name = "DTC_" + c.name
    c.desc = "DTC " + c.desc
    if c.decode == pid:
        c.decode = drop  # Never send mode 02 pid requests (use mode 01 instead)
    __mode2__.append(c)

__mode3__ = [
    OBDCommand("GET_DTC", "Get DTCs", b"03", 0, dtc, ECU.ALL, False),
]

__mode4__ = [
    OBDCommand("CLEAR_DTC", "Clear DTCs and Freeze data", b"04", 0, drop, ECU.ALL, False),
]

__mode6__ = [
    # Mode 06 calls PID's MID's (Monitor ID)
    # This is for CAN only
    #                      name                             description                            cmd     bytes       decoder           ECU        fast
    OBDCommand("MIDS_A"                      , "Supported MIDs [01-20]"                         , b"0600",   0, pid,                   ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B1S1"             , "O2 Sensor Monitor Bank 1 - Sensor 1"            , b"0601",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B1S2"             , "O2 Sensor Monitor Bank 1 - Sensor 2"            , b"0602",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B1S3"             , "O2 Sensor Monitor Bank 1 - Sensor 3"            , b"0603",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B1S4"             , "O2 Sensor Monitor Bank 1 - Sensor 4"            , b"0604",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B2S1"             , "O2 Sensor Monitor Bank 2 - Sensor 1"            , b"0605",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B2S2"             , "O2 Sensor Monitor Bank 2 - Sensor 2"            , b"0606",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B2S3"             , "O2 Sensor Monitor Bank 2 - Sensor 3"            , b"0607",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B2S4"             , "O2 Sensor Monitor Bank 2 - Sensor 4"            , b"0608",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B3S1"             , "O2 Sensor Monitor Bank 3 - Sensor 1"            , b"0609",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B3S2"             , "O2 Sensor Monitor Bank 3 - Sensor 2"            , b"060A",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B3S3"             , "O2 Sensor Monitor Bank 3 - Sensor 3"            , b"060B",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B3S4"             , "O2 Sensor Monitor Bank 3 - Sensor 4"            , b"060C",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B4S1"             , "O2 Sensor Monitor Bank 4 - Sensor 1"            , b"060D",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B4S2"             , "O2 Sensor Monitor Bank 4 - Sensor 2"            , b"060E",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B4S3"             , "O2 Sensor Monitor Bank 4 - Sensor 3"            , b"060F",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_B4S4"             , "O2 Sensor Monitor Bank 4 - Sensor 4"            , b"0610",   0, monitor,               ECU.ALL,     False),
] + ([None] * 15) + [ # 11 - 1F Reserved
    OBDCommand("MIDS_B"                      , "Supported MIDs [21-40]"                         , b"0620",   0, pid,                   ECU.ALL,     False),
    OBDCommand("MONITOR_CATALYST_B1"         , "Catalyst Monitor Bank 1"                        , b"0621",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_CATALYST_B2"         , "Catalyst Monitor Bank 2"                        , b"0622",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_CATALYST_B3"         , "Catalyst Monitor Bank 3"                        , b"0623",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_CATALYST_B4"         , "Catalyst Monitor Bank 4"                        , b"0624",   0, monitor,               ECU.ALL,     False),
] + ([None] * 12) + [ # 25 - 30 Reserved
    OBDCommand("MONITOR_EGR_B1"              , "EGR Monitor Bank 1"                             , b"0631",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_EGR_B2"              , "EGR Monitor Bank 2"                             , b"0632",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_EGR_B3"              , "EGR Monitor Bank 3"                             , b"0633",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_EGR_B4"              , "EGR Monitor Bank 4"                             , b"0634",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_VVT_B1"              , "VVT Monitor Bank 1"                             , b"0635",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_VVT_B2"              , "VVT Monitor Bank 2"                             , b"0636",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_VVT_B3"              , "VVT Monitor Bank 3"                             , b"0637",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_VVT_B4"              , "VVT Monitor Bank 4"                             , b"0638",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_EVAP_150"            , "EVAP Monitor (Cap Off / 0.150\")"               , b"0639",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_EVAP_090"            , "EVAP Monitor (0.090\")"                         , b"063A",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_EVAP_040"            , "EVAP Monitor (0.040\")"                         , b"063B",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_EVAP_020"            , "EVAP Monitor (0.020\")"                         , b"063C",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_PURGE_FLOW"          , "Purge Flow Monitor"                             , b"063D",   0, monitor,               ECU.ALL,     False),
] + ([None] * 2) + [ # 3E - 3F Reserved
    OBDCommand("MIDS_C"                      , "Supported MIDs [41-60]"                         , b"0640",   0, pid,                   ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B1S1"      , "O2 Sensor Heater Monitor Bank 1 - Sensor 1"     , b"0641",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B1S2"      , "O2 Sensor Heater Monitor Bank 1 - Sensor 2"     , b"0642",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B1S3"      , "O2 Sensor Heater Monitor Bank 1 - Sensor 3"     , b"0643",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B1S4"      , "O2 Sensor Heater Monitor Bank 1 - Sensor 4"     , b"0644",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B2S1"      , "O2 Sensor Heater Monitor Bank 2 - Sensor 1"     , b"0645",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B2S2"      , "O2 Sensor Heater Monitor Bank 2 - Sensor 2"     , b"0646",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B2S3"      , "O2 Sensor Heater Monitor Bank 2 - Sensor 3"     , b"0647",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B2S4"      , "O2 Sensor Heater Monitor Bank 2 - Sensor 4"     , b"0648",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B3S1"      , "O2 Sensor Heater Monitor Bank 3 - Sensor 1"     , b"0649",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B3S2"      , "O2 Sensor Heater Monitor Bank 3 - Sensor 2"     , b"064A",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B3S3"      , "O2 Sensor Heater Monitor Bank 3 - Sensor 3"     , b"064B",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B3S4"      , "O2 Sensor Heater Monitor Bank 3 - Sensor 4"     , b"064C",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B4S1"      , "O2 Sensor Heater Monitor Bank 4 - Sensor 1"     , b"064D",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B4S2"      , "O2 Sensor Heater Monitor Bank 4 - SeDTC occurednsor 2"     , b"064E",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B4S3"      , "O2 Sensor Heater Monitor Bank 4 - Sensor 3"     , b"064F",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_O2_HEATER_B4S4"      , "O2 Sensor Heater Monitor Bank 4 - Sensor 4"     , b"0650",   0, monitor,               ECU.ALL,     False),
] + ([None] * 15) + [ # 51 - 5F Reserved
    OBDCommand("MIDS_D"                      , "Supported MIDs [61-80]"                         , b"0660",   0, pid,                   ECU.ALL,     False),
    OBDCommand("MONITOR_HEATED_CATALYST_B1"  , "Heated Catalyst Monitor Bank 1"                 , b"0661",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_HEATED_CATALYST_B2"  , "Heated Catalyst Monitor Bank 2"                 , b"0662",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_HEATED_CATALYST_B3"  , "Heated Catalyst Monitor Bank 3"                 , b"0663",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_HEATED_CATALYST_B4"  , "Heated Catalyst Monitor Bank 4"                 , b"0664",   0, monitor,               ECU.ALL,     False),
] + ([None] * 12) + [ # 65 - 70 Reserved
    OBDCommand("MONITOR_SECONDARY_AIR_1"     , "Secondary Air Monitor 1"                        , b"0671",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_SECONDARY_AIR_2"     , "Secondary Air Monitor 2"                        , b"0672",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_SECONDARY_AIR_3"     , "Secondary Air Monitor 3"                        , b"0673",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_SECONDARY_AIR_4"     , "Secondary Air Monitor 4"                        , b"0674",   0, monitor,               ECU.ALL,     False),
] + ([None] * 11) + [ # 75 - 7F Reserved
    OBDCommand("MIDS_E"                      , "Supported MIDs [81-A0]"                         , b"0680",   0, pid,                   ECU.ALL,     False),
    OBDCommand("MONITOR_FUEL_SYSTEM_B1"      , "Fuel System Monitor Bank 1"                     , b"0681",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_FUEL_SYSTEM_B2"      , "Fuel System Monitor Bank 2"                     , b"0682",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_FUEL_SYSTEM_B3"      , "Fuel System Monitor Bank 3"                     , b"0683",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_FUEL_SYSTEM_B4"      , "Fuel System Monitor Bank 4"                     , b"0684",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_BOOST_PRESSURE_B1"   , "Boost Pressure Control Monitor Bank 1"          , b"0685",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_BOOST_PRESSURE_B2"   , "Boost Pressure Control Monitor Bank 1"          , b"0686",   0, monitor,               ECU.ALL,     False),
] + ([None] * 9) + [ # 87 - 8F Reserved
    OBDCommand("MONITOR_NOX_ABSORBER_B1"     , "NOx Absorber Monitor Bank 1"                    , b"0690",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_NOX_ABSORBER_B2"     , "NOx Absorber Monitor Bank 2"                    , b"0691",   0, monitor,               ECU.ALL,     False),
] + ([None] * 6) + [ # 92 - 97 Reserved
    OBDCommand("MONITOR_NOX_CATALYST_B1"     , "NOx Catalyst Monitor Bank 1"                    , b"0698",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_NOX_CATALYST_B2"     , "NOx Catalyst Monitor Bank 2"                    , b"0699",   0, monitor,               ECU.ALL,     False),
] + ([None] * 6) + [ # 9A - 9F Reserved
    OBDCommand("MIDS_F"                      , "Supported MIDs [A1-C0]"                         , b"06A0",   0, pid,                   ECU.ALL,     False),
    OBDCommand("MONITOR_MISFIRE_GENERAL"     , "Misfire Monitor General Data"                   , b"06A1",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_MISFIRE_CYLINDER_1"  , "Misfire Cylinder 1 Data"                        , b"06A2",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_MISFIRE_CYLINDER_2"  , "Misfire Cylinder 2 Data"                        , b"06A3",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_MISFIRE_CYLINDER_3"  , "Misfire Cylinder 3 Data"                        , b"06A4",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_MISFIRE_CYLINDER_4"  , "Misfire Cylinder 4 Data"                        , b"06A5",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_MISFIRE_CYLINDER_5"  , "Misfire Cylinder 5 Data"                        , b"06A6",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_MISFIRE_CYLINDER_6"  , "Misfire Cylinder 6 Data"                        , b"06A7",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_MISFIRE_CYLINDER_7"  , "Misfire Cylinder 7 Data"                        , b"06A8",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_MISFIRE_CYLINDER_8"  , "Misfire Cylinder 8 Data"                        , b"06A9",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_MISFIRE_CYLINDER_9"  , "Misfire Cylinder 9 Data"                        , b"06AA",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_MISFIRE_CYLINDER_10" , "Misfire Cylinder 10 Data"                       , b"06AB",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_MISFIRE_CYLINDER_11" , "Misfire Cylinder 11 Data"                       , b"06AC",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_MISFIRE_CYLINDER_12" , "Misfire Cylinder 12 Data"                       , b"06AD",   0, monitor,               ECU.ALL,     False),
] + ([None] * 2) + [ # AE - AF Reserved
    OBDCommand("MONITOR_PM_FILTER_B1"        , "PM Filter Monitor Bank 1"                       , b"06B0",   0, monitor,               ECU.ALL,     False),
    OBDCommand("MONITOR_PM_FILTER_B2"        , "PM Filter Monitor Bank 2"                       , b"06B1",   0, monitor,               ECU.ALL,     False),
]

__mode7__ = [
    OBDCommand("GET_CURRENT_DTC", "Get DTCs from the current/last driving cycle", b"07", 0, dtc, ECU.ALL, False),
]


__mode9__ = [
    #                      name                             description                            cmd     bytes       decoder       ECU        fast
    OBDCommand("PIDS_9A"                    , "Supported PIDs [01-20]"                            , b"0900",  7, pid,                ECU.ALL,     True),
    OBDCommand("VIN_MESSAGE_COUNT"          , "VIN Message Count"                                 , b"0901",  3, count,              ECU.ENGINE,  True),
    OBDCommand("VIN"                        , "Vehicle Identification Number"                     , b"0902", 22, encoded_string(17), ECU.ENGINE,  True),
    OBDCommand("CALIBRATION_ID_MESSAGE_COUNT","Calibration ID message count for PID 04"           , b"0903",  3, count,              ECU.ALL,     True),
    OBDCommand("CALIBRATION_ID"             , "Calibration ID"                                    , b"0904", 18, encoded_string(16), ECU.ALL,     True),
    OBDCommand("CVN_MESSAGE_COUNT"          , "CVN Message Count for PID 06"                      , b"0905",  3, count,              ECU.ALL,     True),
    OBDCommand("CVN"                        , "Calibration Verification Numbers"                  , b"0906", 10, cvn,                ECU.ALL,     True),

#
# NOTE: The following are untested
#
#    OBDCommand("PERF_TRACKING_MESSAGE_COUNT", "Performance tracking message count"                , b"0907",  3, count,              ECU.ALL,     True),
#    OBDCommand("PERF_TRACKING_SPARK"        , "In-use performance tracking (spark ignition)"      , b"0908",  4, raw_string,         ECU.ALL,     True),
#    OBDCommand("ECU_NAME_MESSAGE_COUNT"     , "ECU Name Message Count for PID 0A"                 , b"0909",  3, count,              ECU.ALL,     True),
#    OBDCommand("ECU_NAME"                   , "ECU Name"                                          , b"090a", 20, raw_string,         ECU.ALL,     True),
#    OBDCommand("PERF_TRACKING_COMPRESSION"  , "In-use performance tracking (compression ignition)", b"090b",  4, raw_string,         ECU.ALL,     True),
]

__misc__ = [
    OBDCommand("ELM_VERSION", "ELM327 version string", b"ATI", 0, raw_string, ECU.UNKNOWN, False),
    OBDCommand("ELM_VOLTAGE", "Voltage detected by OBD-II adapter", b"ATRV", 0, elm_voltage, ECU.UNKNOWN, False),
]

"""
Assemble the command tables by mode, and allow access by name
"""


class Commands():
    def __init__(self):

        # allow commands to be accessed by mode and PID
        self.modes = [
            [],
            __mode1__,
            __mode2__,
            __mode3__,
            __mode4__,
            [],
            __mode6__,
            __mode7__,
            [],
            __mode9__,
        ]

        # allow commands to be accessed by name
        for m in self.modes:
            for c in m:
                if c is not None:
                    self.__dict__[c.name] = c

        for c in __misc__:
            self.__dict__[c.name] = c

    def __getitem__(self, key):
        """
            commands can be accessed by name, or by mode/pid

            obd.commands.RPM
            obd.commands["RPM"]
            obd.commands[1][12] # mode 1, PID 12 (RPM)
        """

        try:
            basestring
        except NameError:
            basestring = str

        if isinstance(key, int):
            return self.modes[key]
        elif isinstance(key, basestring):
            return self.__dict__[key]
        else:
            logger.warning("OBD commands can only be retrieved by PID value or dict name")

    def __len__(self):
        """ returns the number of commands supported by python-OBD """
        return sum([len(mode) for mode in self.modes])

    def __contains__(self, name):
        """ calls has_name(s) """
        return self.has_name(name)

    def base_commands(self):
        """
            returns the list of commands that should always be
            supported by the ELM327
        """
        return [
            self.PIDS_A,
            self.PIDS_9A,
            self.MIDS_A,
            self.GET_DTC,
            self.CLEAR_DTC,
            self.GET_CURRENT_DTC,
            self.ELM_VERSION,
            self.ELM_VOLTAGE,
        ]

    def pid_getters(self):
        """ returns a list of PID GET commands """
        getters = []
        for mode in self.modes:
            getters += [cmd for cmd in mode if (cmd and cmd.decode == pid)]
        return getters

    def has_command(self, c):
        """ checks for existance of a command by OBDCommand object """
        return c in self.__dict__.values()

    def has_name(self, name):
        """ checks for existance of a command by name """
        # isupper() rejects all the normal properties
        return name.isupper() and name in self.__dict__

    def has_pid(self, mode, pid):
        """ checks for existance of a command by int mode and int pid """
        if (mode < 0) or (pid < 0):
            return False
        if mode >= len(self.modes):
            return False
        if pid >= len(self.modes[mode]):
            return False

        # make sure that the command isn't reserved
        return self.modes[mode][pid] is not None


# export this object
commands = Commands()
