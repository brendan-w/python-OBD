# OBD-II adapter (ELM327 commands)

|PID  | Name        | Description                             | Response Value        |
|-----|-------------|-----------------------------------------|-----------------------|
| N/A | ELM_VERSION | OBD-II adapter version string           | string                |
| N/A | ELM_VOLTAGE | Voltage detected by OBD-II adapter      | Unit.volt             |

<br>

# Mode 01

|PID | Name                      | Description                             | Response Value        |
|----|---------------------------|-----------------------------------------|-----------------------|
| 00 | PIDS_A                    | Supported PIDs [01-20]                  | BitArray              |
| 01 | STATUS                    | Status since DTCs cleared               | [special](Responses.md#status) |
| 02 | FREEZE_DTC                | DTC that triggered the freeze frame     | [special](Responses.md#diagnostic-trouble-codes-dtcs) |
| 03 | FUEL_STATUS               | Fuel System Status                      | [(string, string)](Responses.md#fuel-status) |
| 04 | ENGINE_LOAD               | Calculated Engine Load                  | Unit.percent          |
| 05 | COOLANT_TEMP              | Engine Coolant Temperature              | Unit.celsius          |
| 06 | SHORT_FUEL_TRIM_1         | Short Term Fuel Trim - Bank 1           | Unit.percent          |
| 07 | LONG_FUEL_TRIM_1          | Long Term Fuel Trim - Bank 1            | Unit.percent          |
| 08 | SHORT_FUEL_TRIM_2         | Short Term Fuel Trim - Bank 2           | Unit.percent          |
| 09 | LONG_FUEL_TRIM_2          | Long Term Fuel Trim - Bank 2            | Unit.percent          |
| 0A | FUEL_PRESSURE             | Fuel Pressure                           | Unit.kilopascal       |
| 0B | INTAKE_PRESSURE           | Intake Manifold Pressure                | Unit.kilopascal       |
| 0C | RPM                       | Engine RPM                              | Unit.rpm              |
| 0D | SPEED                     | Vehicle Speed                           | Unit.kph              |
| 0E | TIMING_ADVANCE            | Timing Advance                          | Unit.degree           |
| 0F | INTAKE_TEMP               | Intake Air Temp                         | Unit.celsius          |
| 10 | MAF                       | Air Flow Rate (MAF)                     | Unit.grams_per_second |
| 11 | THROTTLE_POS              | Throttle Position                       | Unit.percent          |
| 12 | AIR_STATUS                | Secondary Air Status                    | [string](Responses.md#air-status) |
| 13 | O2_SENSORS                | O2 Sensors Present                      | [special](Responses.md#oxygen-sensors-present) |
| 14 | O2_B1S1                   | O2: Bank 1 - Sensor 1 Voltage           | Unit.volt             |
| 15 | O2_B1S2                   | O2: Bank 1 - Sensor 2 Voltage           | Unit.volt             |
| 16 | O2_B1S3                   | O2: Bank 1 - Sensor 3 Voltage           | Unit.volt             |
| 17 | O2_B1S4                   | O2: Bank 1 - Sensor 4 Voltage           | Unit.volt             |
| 18 | O2_B2S1                   | O2: Bank 2 - Sensor 1 Voltage           | Unit.volt             |
| 19 | O2_B2S2                   | O2: Bank 2 - Sensor 2 Voltage           | Unit.volt             |
| 1A | O2_B2S3                   | O2: Bank 2 - Sensor 3 Voltage           | Unit.volt             |
| 1B | O2_B2S4                   | O2: Bank 2 - Sensor 4 Voltage           | Unit.volt             |
| 1C | OBD_COMPLIANCE            | OBD Standards Compliance                | string                |
| 1D | O2_SENSORS_ALT            | O2 Sensors Present (alternate)          | [special](Responses.md#oxygen-sensors-present) |
| 1E | AUX_INPUT_STATUS          | Auxiliary input status (power take off) | boolean               |
| 1F | RUN_TIME                  | Engine Run Time                         | Unit.second           |
| 20 | PIDS_B                    | Supported PIDs [21-40]                  | BitArray              |
| 21 | DISTANCE_W_MIL            | Distance Traveled with MIL on           | Unit.kilometer        |
| 22 | FUEL_RAIL_PRESSURE_VAC    | Fuel Rail Pressure (relative to vacuum) | Unit.kilopascal       |
| 23 | FUEL_RAIL_PRESSURE_DIRECT | Fuel Rail Pressure (direct inject)      | Unit.kilopascal       |
| 24 | O2_S1_WR_VOLTAGE          | 02 Sensor 1 WR Lambda Voltage           | Unit.volt             |
| 25 | O2_S2_WR_VOLTAGE          | 02 Sensor 2 WR Lambda Voltage           | Unit.volt             |
| 26 | O2_S3_WR_VOLTAGE          | 02 Sensor 3 WR Lambda Voltage           | Unit.volt             |
| 27 | O2_S4_WR_VOLTAGE          | 02 Sensor 4 WR Lambda Voltage           | Unit.volt             |
| 28 | O2_S5_WR_VOLTAGE          | 02 Sensor 5 WR Lambda Voltage           | Unit.volt             |
| 29 | O2_S6_WR_VOLTAGE          | 02 Sensor 6 WR Lambda Voltage           | Unit.volt             |
| 2A | O2_S7_WR_VOLTAGE          | 02 Sensor 7 WR Lambda Voltage           | Unit.volt             |
| 2B | O2_S8_WR_VOLTAGE          | 02 Sensor 8 WR Lambda Voltage           | Unit.volt             |
| 2C | COMMANDED_EGR             | Commanded EGR                           | Unit.percent          |
| 2D | EGR_ERROR                 | EGR Error                               | Unit.percent          |
| 2E | EVAPORATIVE_PURGE         | Commanded Evaporative Purge             | Unit.percent          |
| 2F | FUEL_LEVEL                | Fuel Level Input                        | Unit.percent          |
| 30 | WARMUPS_SINCE_DTC_CLEAR   | Number of warm-ups since codes cleared  | Unit.count            |
| 31 | DISTANCE_SINCE_DTC_CLEAR  | Distance traveled since codes cleared   | Unit.kilometer        |
| 32 | EVAP_VAPOR_PRESSURE       | Evaporative system vapor pressure       | Unit.pascal           |
| 33 | BAROMETRIC_PRESSURE       | Barometric Pressure                     | Unit.kilopascal       |
| 34 | O2_S1_WR_CURRENT          | 02 Sensor 1 WR Lambda Current           | Unit.milliampere      |
| 35 | O2_S2_WR_CURRENT          | 02 Sensor 2 WR Lambda Current           | Unit.milliampere      |
| 36 | O2_S3_WR_CURRENT          | 02 Sensor 3 WR Lambda Current           | Unit.milliampere      |
| 37 | O2_S4_WR_CURRENT          | 02 Sensor 4 WR Lambda Current           | Unit.milliampere      |
| 38 | O2_S5_WR_CURRENT          | 02 Sensor 5 WR Lambda Current           | Unit.milliampere      |
| 39 | O2_S6_WR_CURRENT          | 02 Sensor 6 WR Lambda Current           | Unit.milliampere      |
| 3A | O2_S7_WR_CURRENT          | 02 Sensor 7 WR Lambda Current           | Unit.milliampere      |
| 3B | O2_S8_WR_CURRENT          | 02 Sensor 8 WR Lambda Current           | Unit.milliampere      |
| 3C | CATALYST_TEMP_B1S1        | Catalyst Temperature: Bank 1 - Sensor 1 | Unit.celsius          |
| 3D | CATALYST_TEMP_B2S1        | Catalyst Temperature: Bank 2 - Sensor 1 | Unit.celsius          |
| 3E | CATALYST_TEMP_B1S2        | Catalyst Temperature: Bank 1 - Sensor 2 | Unit.celsius          |
| 3F | CATALYST_TEMP_B2S2        | Catalyst Temperature: Bank 2 - Sensor 2 | Unit.celsius          |
| 40 | PIDS_C                    | Supported PIDs [41-60]                  | BitArray              |
| 41 | STATUS_DRIVE_CYCLE        | Monitor status this drive cycle         | [special](Responses.md#status) |
| 42 | CONTROL_MODULE_VOLTAGE    | Control module voltage                  | Unit.volt             |
| 43 | ABSOLUTE_LOAD             | Absolute load value                     | Unit.percent          |
| 44 | COMMANDED_EQUIV_RATIO     | Commanded equivalence ratio             | Unit.ratio            |
| 45 | RELATIVE_THROTTLE_POS     | Relative throttle position              | Unit.percent          |
| 46 | AMBIANT_AIR_TEMP          | Ambient air temperature                 | Unit.celsius          |
| 47 | THROTTLE_POS_B            | Absolute throttle position B            | Unit.percent          |
| 48 | THROTTLE_POS_C            | Absolute throttle position C            | Unit.percent          |
| 49 | ACCELERATOR_POS_D         | Accelerator pedal position D            | Unit.percent          |
| 4A | ACCELERATOR_POS_E         | Accelerator pedal position E            | Unit.percent          |
| 4B | ACCELERATOR_POS_F         | Accelerator pedal position F            | Unit.percent          |
| 4C | THROTTLE_ACTUATOR         | Commanded throttle actuator             | Unit.percent          |
| 4D | RUN_TIME_MIL              | Time run with MIL on                    | Unit.minute           |
| 4E | TIME_SINCE_DTC_CLEARED    | Time since trouble codes cleared        | Unit.minute           |
| 4F | *unsupported*             | *unsupported*                           |                       |
| 50 | MAX_MAF                   | Maximum value for mass air flow sensor  | Unit.grams_per_second |
| 51 | FUEL_TYPE                 | Fuel Type                               | string                |
| 52 | ETHANOL_PERCENT           | Ethanol Fuel Percent                    | Unit.percent          |
| 53 | EVAP_VAPOR_PRESSURE_ABS   | Absolute Evap system Vapor Pressure     | Unit.kilopascal       |
| 54 | EVAP_VAPOR_PRESSURE_ALT   | Evap system vapor pressure              | Unit.pascal           |
| 55 | SHORT_O2_TRIM_B1          | Short term secondary O2 trim - Bank 1   | Unit.percent          |
| 56 | LONG_O2_TRIM_B1           | Long term secondary O2 trim - Bank 1    | Unit.percent          |
| 57 | SHORT_O2_TRIM_B2          | Short term secondary O2 trim - Bank 2   | Unit.percent          |
| 58 | LONG_O2_TRIM_B2           | Long term secondary O2 trim - Bank 2    | Unit.percent          |
| 59 | FUEL_RAIL_PRESSURE_ABS    | Fuel rail pressure (absolute)           | Unit.kilopascal       |
| 5A | RELATIVE_ACCEL_POS        | Relative accelerator pedal position     | Unit.percent          |
| 5B | HYBRID_BATTERY_REMAINING  | Hybrid battery pack remaining life      | Unit.percent          |
| 5C | OIL_TEMP                  | Engine oil temperature                  | Unit.celsius          |
| 5D | FUEL_INJECT_TIMING        | Fuel injection timing                   | Unit.degree           |
| 5E | FUEL_RATE                 | Engine fuel rate                        | Unit.liters_per_hour  |
| 5F | *unsupported*             | *unsupported*                           |                       |

<br>

# Mode 02

Mode 02 commands are the same as mode 01, but are metrics from when the last DTC occurred (the freeze frame). To access them by name, simple prepend `DTC_` to the Mode 01 command name.

```python
import obd

obd.commands.RPM # the Mode 01 command
# vs.
obd.commands.DTC_RPM # the Mode 02 command
```

<br>

# Mode 03

Mode 03 contains a single command `GET_DTC` which requests all diagnostic trouble codes from the vehicle. The response will contain the codes themselves, as well as a description (if python-OBD has one). See the [DTC Responses](Responses.md#diagnostic-trouble-codes-dtcs) section for more details.

|PID  | Name    | Description                             | Response Value        |
|-----|---------|-----------------------------------------|-----------------------|
| N/A | GET_DTC | Get Diagnostic Trouble Codes            | [special](Responses.md#diagnostic-trouble-codes-dtcs) |


<br>

# Mode 04

|PID  | Name      | Description                             | Response Value        |
|-----|-----------|-----------------------------------------|-----------------------|
| N/A | CLEAR_DTC | Clear DTCs and Freeze data              | N/A                   |

<br>

# Mode 06

<span style="color:red">*WARNING: mode 06 is experimental. While it passes software tests, it has not been tested on a real vehicle. Any debug output for this mode would be greatly appreciated.*</span>

Mode 06 commands are used to monitor various test results from the vehicle. All commands in this mode return the same datatype, as described in the [Monitor Response](Responses.md#monitors-mode-06-responses) section. Currently, mode 06 commands are only implemented for CAN protocols (ISO 15765-4).

|PID    | Name                        | Description                                | Response Value        |
|-------|-----------------------------|--------------------------------------------|-----------------------|
| 00    | MIDS_A                      | Supported MIDs [01-20]                     | BitArray              |
| 01    | MONITOR_O2_B1S1             | O2 Sensor Monitor Bank 1 - Sensor 1        | [monitor](Responses.md#monitors-mode-06-responses) |
| 02    | MONITOR_O2_B1S2             | O2 Sensor Monitor Bank 1 - Sensor 2        | [monitor](Responses.md#monitors-mode-06-responses) |
| 03    | MONITOR_O2_B1S3             | O2 Sensor Monitor Bank 1 - Sensor 3        | [monitor](Responses.md#monitors-mode-06-responses) |
| 04    | MONITOR_O2_B1S4             | O2 Sensor Monitor Bank 1 - Sensor 4        | [monitor](Responses.md#monitors-mode-06-responses) |
| 05    | MONITOR_O2_B2S1             | O2 Sensor Monitor Bank 2 - Sensor 1        | [monitor](Responses.md#monitors-mode-06-responses) |
| 06    | MONITOR_O2_B2S2             | O2 Sensor Monitor Bank 2 - Sensor 2        | [monitor](Responses.md#monitors-mode-06-responses) |
| 07    | MONITOR_O2_B2S3             | O2 Sensor Monitor Bank 2 - Sensor 3        | [monitor](Responses.md#monitors-mode-06-responses) |
| 08    | MONITOR_O2_B2S4             | O2 Sensor Monitor Bank 2 - Sensor 4        | [monitor](Responses.md#monitors-mode-06-responses) |
| 09    | MONITOR_O2_B3S1             | O2 Sensor Monitor Bank 3 - Sensor 1        | [monitor](Responses.md#monitors-mode-06-responses) |
| 0A    | MONITOR_O2_B3S2             | O2 Sensor Monitor Bank 3 - Sensor 2        | [monitor](Responses.md#monitors-mode-06-responses) |
| 0B    | MONITOR_O2_B3S3             | O2 Sensor Monitor Bank 3 - Sensor 3        | [monitor](Responses.md#monitors-mode-06-responses) |
| 0C    | MONITOR_O2_B3S4             | O2 Sensor Monitor Bank 3 - Sensor 4        | [monitor](Responses.md#monitors-mode-06-responses) |
| 0D    | MONITOR_O2_B4S1             | O2 Sensor Monitor Bank 4 - Sensor 1        | [monitor](Responses.md#monitors-mode-06-responses) |
| 0E    | MONITOR_O2_B4S2             | O2 Sensor Monitor Bank 4 - Sensor 2        | [monitor](Responses.md#monitors-mode-06-responses) |
| 0F    | MONITOR_O2_B4S3             | O2 Sensor Monitor Bank 4 - Sensor 3        | [monitor](Responses.md#monitors-mode-06-responses) |
| 10    | MONITOR_O2_B4S4             | O2 Sensor Monitor Bank 4 - Sensor 4        | [monitor](Responses.md#monitors-mode-06-responses) |
| *gap* |                             |                                            |
| 20    | MIDS_B                      | Supported MIDs [21-40]                     | BitArray              |
| 21    | MONITOR_CATALYST_B1         | Catalyst Monitor Bank 1                    | [monitor](Responses.md#monitors-mode-06-responses) |
| 22    | MONITOR_CATALYST_B2         | Catalyst Monitor Bank 2                    | [monitor](Responses.md#monitors-mode-06-responses) |
| 23    | MONITOR_CATALYST_B3         | Catalyst Monitor Bank 3                    | [monitor](Responses.md#monitors-mode-06-responses) |
| 24    | MONITOR_CATALYST_B4         | Catalyst Monitor Bank 4                    | [monitor](Responses.md#monitors-mode-06-responses) |
| *gap* |                             |                                            |
| 31    | MONITOR_EGR_B1              | EGR Monitor Bank 1                         | [monitor](Responses.md#monitors-mode-06-responses) |
| 32    | MONITOR_EGR_B2              | EGR Monitor Bank 2                         | [monitor](Responses.md#monitors-mode-06-responses) |
| 33    | MONITOR_EGR_B3              | EGR Monitor Bank 3                         | [monitor](Responses.md#monitors-mode-06-responses) |
| 34    | MONITOR_EGR_B4              | EGR Monitor Bank 4                         | [monitor](Responses.md#monitors-mode-06-responses) |
| 35    | MONITOR_VVT_B1              | VVT Monitor Bank 1                         | [monitor](Responses.md#monitors-mode-06-responses) |
| 36    | MONITOR_VVT_B2              | VVT Monitor Bank 2                         | [monitor](Responses.md#monitors-mode-06-responses) |
| 37    | MONITOR_VVT_B3              | VVT Monitor Bank 3                         | [monitor](Responses.md#monitors-mode-06-responses) |
| 38    | MONITOR_VVT_B4              | VVT Monitor Bank 4                         | [monitor](Responses.md#monitors-mode-06-responses) |
| 39    | MONITOR_EVAP_150            | EVAP Monitor (Cap Off / 0.150\")           | [monitor](Responses.md#monitors-mode-06-responses) |
| 3A    | MONITOR_EVAP_090            | EVAP Monitor (0.090\")                     | [monitor](Responses.md#monitors-mode-06-responses) |
| 3B    | MONITOR_EVAP_040            | EVAP Monitor (0.040\")                     | [monitor](Responses.md#monitors-mode-06-responses) |
| 3C    | MONITOR_EVAP_020            | EVAP Monitor (0.020\")                     | [monitor](Responses.md#monitors-mode-06-responses) |
| 3D    | MONITOR_PURGE_FLOW          | Purge Flow Monitor                         | [monitor](Responses.md#monitors-mode-06-responses) |
| *gap* |                             |                                            |
| 40    | MIDS_C                      | Supported MIDs [41-60]                     | BitArray              |
| 41    | MONITOR_O2_HEATER_B1S1      | O2 Sensor Heater Monitor Bank 1 - Sensor 1 | [monitor](Responses.md#monitors-mode-06-responses) |
| 42    | MONITOR_O2_HEATER_B1S2      | O2 Sensor Heater Monitor Bank 1 - Sensor 2 | [monitor](Responses.md#monitors-mode-06-responses) |
| 43    | MONITOR_O2_HEATER_B1S3      | O2 Sensor Heater Monitor Bank 1 - Sensor 3 | [monitor](Responses.md#monitors-mode-06-responses) |
| 44    | MONITOR_O2_HEATER_B1S4      | O2 Sensor Heater Monitor Bank 1 - Sensor 4 | [monitor](Responses.md#monitors-mode-06-responses) |
| 45    | MONITOR_O2_HEATER_B2S1      | O2 Sensor Heater Monitor Bank 2 - Sensor 1 | [monitor](Responses.md#monitors-mode-06-responses) |
| 46    | MONITOR_O2_HEATER_B2S2      | O2 Sensor Heater Monitor Bank 2 - Sensor 2 | [monitor](Responses.md#monitors-mode-06-responses) |
| 47    | MONITOR_O2_HEATER_B2S3      | O2 Sensor Heater Monitor Bank 2 - Sensor 3 | [monitor](Responses.md#monitors-mode-06-responses) |
| 48    | MONITOR_O2_HEATER_B2S4      | O2 Sensor Heater Monitor Bank 2 - Sensor 4 | [monitor](Responses.md#monitors-mode-06-responses) |
| 49    | MONITOR_O2_HEATER_B3S1      | O2 Sensor Heater Monitor Bank 3 - Sensor 1 | [monitor](Responses.md#monitors-mode-06-responses) |
| 4A    | MONITOR_O2_HEATER_B3S2      | O2 Sensor Heater Monitor Bank 3 - Sensor 2 | [monitor](Responses.md#monitors-mode-06-responses) |
| 4B    | MONITOR_O2_HEATER_B3S3      | O2 Sensor Heater Monitor Bank 3 - Sensor 3 | [monitor](Responses.md#monitors-mode-06-responses) |
| 4C    | MONITOR_O2_HEATER_B3S4      | O2 Sensor Heater Monitor Bank 3 - Sensor 4 | [monitor](Responses.md#monitors-mode-06-responses) |
| 4D    | MONITOR_O2_HEATER_B4S1      | O2 Sensor Heater Monitor Bank 4 - Sensor 1 | [monitor](Responses.md#monitors-mode-06-responses) |
| 4E    | MONITOR_O2_HEATER_B4S2      | O2 Sensor Heater Monitor Bank 4 - Sensor 2 | [monitor](Responses.md#monitors-mode-06-responses) |
| 4F    | MONITOR_O2_HEATER_B4S3      | O2 Sensor Heater Monitor Bank 4 - Sensor 3 | [monitor](Responses.md#monitors-mode-06-responses) |
| 50    | MONITOR_O2_HEATER_B4S4      | O2 Sensor Heater Monitor Bank 4 - Sensor 4 | [monitor](Responses.md#monitors-mode-06-responses) |
| *gap* |                             |                                            |
| 60    | MIDS_D                      | Supported MIDs [61-80]                     | BitArray              |
| 61    | MONITOR_HEATED_CATALYST_B1  | Heated Catalyst Monitor Bank 1             | [monitor](Responses.md#monitors-mode-06-responses) |
| 62    | MONITOR_HEATED_CATALYST_B2  | Heated Catalyst Monitor Bank 2             | [monitor](Responses.md#monitors-mode-06-responses) |
| 63    | MONITOR_HEATED_CATALYST_B3  | Heated Catalyst Monitor Bank 3             | [monitor](Responses.md#monitors-mode-06-responses) |
| 64    | MONITOR_HEATED_CATALYST_B4  | Heated Catalyst Monitor Bank 4             | [monitor](Responses.md#monitors-mode-06-responses) |
| *gap* |                             |                                            |
| 71    | MONITOR_SECONDARY_AIR_1     | Secondary Air Monitor 1                    | [monitor](Responses.md#monitors-mode-06-responses) |
| 72    | MONITOR_SECONDARY_AIR_2     | Secondary Air Monitor 2                    | [monitor](Responses.md#monitors-mode-06-responses) |
| 73    | MONITOR_SECONDARY_AIR_3     | Secondary Air Monitor 3                    | [monitor](Responses.md#monitors-mode-06-responses) |
| 74    | MONITOR_SECONDARY_AIR_4     | Secondary Air Monitor 4                    | [monitor](Responses.md#monitors-mode-06-responses) |
| *gap* |                             |                                            |
| 80    | MIDS_E                      | Supported MIDs [81-A0]                     | BitArray              |
| 81    | MONITOR_FUEL_SYSTEM_B1      | Fuel System Monitor Bank 1                 | [monitor](Responses.md#monitors-mode-06-responses) |
| 82    | MONITOR_FUEL_SYSTEM_B2      | Fuel System Monitor Bank 2                 | [monitor](Responses.md#monitors-mode-06-responses) |
| 83    | MONITOR_FUEL_SYSTEM_B3      | Fuel System Monitor Bank 3                 | [monitor](Responses.md#monitors-mode-06-responses) |
| 84    | MONITOR_FUEL_SYSTEM_B4      | Fuel System Monitor Bank 4                 | [monitor](Responses.md#monitors-mode-06-responses) |
| 85    | MONITOR_BOOST_PRESSURE_B1   | Boost Pressure Control Monitor Bank 1      | [monitor](Responses.md#monitors-mode-06-responses) |
| 86    | MONITOR_BOOST_PRESSURE_B2   | Boost Pressure Control Monitor Bank 1      | [monitor](Responses.md#monitors-mode-06-responses) |
| *gap* |                             |                                            |
| 90    | MONITOR_NOX_ABSORBER_B1     | NOx Absorber Monitor Bank 1                | [monitor](Responses.md#monitors-mode-06-responses) |
| 91    | MONITOR_NOX_ABSORBER_B2     | NOx Absorber Monitor Bank 2                | [monitor](Responses.md#monitors-mode-06-responses) |
| *gap* |                             |                                            |
| 98    | MONITOR_NOX_CATALYST_B1     | NOx Catalyst Monitor Bank 1                | [monitor](Responses.md#monitors-mode-06-responses) |
| 99    | MONITOR_NOX_CATALYST_B2     | NOx Catalyst Monitor Bank 2                | [monitor](Responses.md#monitors-mode-06-responses) |
| *gap* |                             |                                            |
| A0    | MIDS_F                      | Supported MIDs [A1-C0]                     | BitArray              |
| A1    | MONITOR_MISFIRE_GENERAL     | Misfire Monitor General Data               | [monitor](Responses.md#monitors-mode-06-responses) |
| A2    | MONITOR_MISFIRE_CYLINDER_1  | Misfire Cylinder 1 Data                    | [monitor](Responses.md#monitors-mode-06-responses) |
| A3    | MONITOR_MISFIRE_CYLINDER_2  | Misfire Cylinder 2 Data                    | [monitor](Responses.md#monitors-mode-06-responses) |
| A4    | MONITOR_MISFIRE_CYLINDER_3  | Misfire Cylinder 3 Data                    | [monitor](Responses.md#monitors-mode-06-responses) |
| A5    | MONITOR_MISFIRE_CYLINDER_4  | Misfire Cylinder 4 Data                    | [monitor](Responses.md#monitors-mode-06-responses) |
| A6    | MONITOR_MISFIRE_CYLINDER_5  | Misfire Cylinder 5 Data                    | [monitor](Responses.md#monitors-mode-06-responses) |
| A7    | MONITOR_MISFIRE_CYLINDER_6  | Misfire Cylinder 6 Data                    | [monitor](Responses.md#monitors-mode-06-responses) |
| A8    | MONITOR_MISFIRE_CYLINDER_7  | Misfire Cylinder 7 Data                    | [monitor](Responses.md#monitors-mode-06-responses) |
| A9    | MONITOR_MISFIRE_CYLINDER_8  | Misfire Cylinder 8 Data                    | [monitor](Responses.md#monitors-mode-06-responses) |
| AA    | MONITOR_MISFIRE_CYLINDER_9  | Misfire Cylinder 9 Data                    | [monitor](Responses.md#monitors-mode-06-responses) |
| AB    | MONITOR_MISFIRE_CYLINDER_10 | Misfire Cylinder 10 Data                   | [monitor](Responses.md#monitors-mode-06-responses) |
| AC    | MONITOR_MISFIRE_CYLINDER_11 | Misfire Cylinder 11 Data                   | [monitor](Responses.md#monitors-mode-06-responses) |
| AD    | MONITOR_MISFIRE_CYLINDER_12 | Misfire Cylinder 12 Data                   | [monitor](Responses.md#monitors-mode-06-responses) |
| *gap* |                             |                                            |
| B0    | MONITOR_PM_FILTER_B1        | PM Filter Monitor Bank 1                   | [monitor](Responses.md#monitors-mode-06-responses) |
| B1    | MONITOR_PM_FILTER_B2        | PM Filter Monitor Bank 2                   | [monitor](Responses.md#monitors-mode-06-responses) |

<br>

# Mode 07

The return value will be encoded in the same structure as the Mode 03 `GET_DTC` command.

|PID  | Name            | Description                                  | Response Value        |
|-----|-----------------|----------------------------------------------|-----------------------|
| N/A | GET_CURRENT_DTC | Get DTCs from the current/last driving cycle | [special](Responses.md#diagnostic-trouble-codes-dtcs) |

<br>

# Mode 09

<span style="color:red">*WARNING: mode 09 is experimental. While it has been tested on a hardware simulator, only a subset of the supported
commands have (00-06) been tested. Any debug output for this mode, especially for the untested PIDs, would be greatly appreciated.*</span>

|PID | Name                         | Description                                        | Response Value        |
|----|------------------------------|----------------------------------------------------|-----------------------|
| 00 | PIDS_9A                      | Supported PIDs [01-20]                             | BitArray              |
| 01 | VIN_MESSAGE_COUNT            | VIN Message Count                                  | Unit.count            |
| 02 | VIN                          | Get Vehicle Identification Number                  | string                |
| 03 | CALIBRATION_ID_MESSAGE_COUNT | Calibration ID message count for PID 04            | Unit.count            |
| 04 | CALIBRATION_ID               | Calibration ID                                     | string                |
| 05 | CVN_MESSAGE_COUNT            | CVN Message Count for PID 06                       | Unit.count            |
| 06 | CVN                          | Calibration Verification Numbers                   | hex string            |
| 07 | PERF_TRACKING_MESSAGE_COUNT  | Performance tracking message count                 | Unit.count            |
| 08 | PERF_TRACKING_SPARK          | In-use performance tracking (spark ignition)       | TODO                  |
| 09 | ECU_NAME_MESSAGE_COUNT       | ECU Name Message Count for PID 0A                  | Unit.count            |
| 0a | ECU_NAME                     | ECU Name                                           | TODO                  |
| 0b | PERF_TRACKING_COMPRESSION    | In-use performance tracking (compression ignition) | TODO                  |

<br>
