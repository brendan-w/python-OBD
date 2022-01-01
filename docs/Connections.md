
After installing the library, simply `import obd`, and create a new OBD connection object. By default, python-OBD will scan for Bluetooth and USB serial ports (in that order), and will pick the first connection it finds. The port can also be specified manually by passing a connection string to the OBD constructor. You can also use the `scan_serial` helper retrieve a list of connected ports.

```python
import obd

connection = obd.OBD() # auto connect

# OR

connection = obd.OBD("/dev/ttyUSB0") # create connection with USB 0

# OR

ports = obd.scan_serial()      # return list of valid USB or RF ports
print ports                    # ['/dev/ttyUSB0', '/dev/ttyUSB1']
connection = obd.OBD(ports[0]) # connect to the first port in the list
```


<br>

### OBD(portstr=None, baudrate=None, protocol=None, fast=True, timeout=0.1, check_voltage=True, start_low_power=False):

`portstr`: The UNIX device file or Windows COM Port for your adapter. The default value (`None`) will auto select a port.

`baudrate`: The baudrate at which to set the serial connection. This can vary from adapter to adapter. Typical values are: 9600, 38400, 19200, 57600, 115200. The default value (`None`) will auto select a baudrate.

`protocol`: Forces python-OBD to use the given protocol when communicating with the adapter. See [protocol_id()](#protocol_id) for possible values. The default value (`None`) will auto select a protocol.

`fast`: Allows commands to be optimized before being sent to the car. Python-OBD currently makes two such optimizations:

- Sends carriage returns to repeat the previous command.
- Appends a response limit to the end of the command, telling the adapter to return after it receives *N* responses (rather than waiting and eventually timing out). This feature can be enabled and disabled for individual commands.

Disabling fast mode will guarantee that python-OBD outputs the unaltered command for every request.

`timeout`: Specifies the connection timeout in seconds.

`check_voltage`: Optional argument that is `True` by default and when set to `False` disables the detection of the car supply voltage on OBDII port (which should be about 12V). This control assumes that, if the voltage is lower than 6V, the OBDII port is disconnected from the car. If the option is enabled, it adds the `OBDStatus.OBD_CONNECTED` status, which is set when enough voltage is returned (socket connected to the car) but the ignition is off (no communication with the vehicle). Setting the option to `False` should be needed when the adapter does not support the voltage pin or more generally when the hardware provides unreliable results, or if the pin reads the switched ignition voltage rather than the battery positive (this depends on the car).

`start_low_power`: Optional argument that defaults to `False`. If set to `True` the initial connection will take longer (roughly 1 more second) but will support waking the ELM327 from low power mode before starting the connection. It does this by sending a space to the chip to trigger a charecter being received on the RS232 input line. This is sent before the baud rate is setup, to ensure the device is awake to detect the baud rate.

<br>

---

### query(command, force=False)

Sends an `OBDCommand` to the car, and returns an `OBDResponse` object. This function will block until a response is received from the car. This function will also check whether the given command is supported by your car. If a command is not marked as supported, it will not be sent, and an empty `OBDResponse` will be returned. To force an unsupported command to be sent, there is an optional `force` parameter for your convenience.

*For non-blocking querying, see [Async Querying](Async Connections.md)*

```python
import obd
connection = obd.OBD()

r = connection.query(obd.commands.RPM) # returns the response from the car
```

---

### status()

Returns a string value reflecting the status of the connection after OBD() or Async() methods are executed. These values should be compared against the `OBDStatus` class. The fact that they are strings is for human readability only. There are currently 4 possible states:

```python
from obd import OBDStatus

# no connection is made
OBDStatus.NOT_CONNECTED # "Not Connected"

# successful communication with the ELM327 adapter
OBDStatus.ELM_CONNECTED # "ELM Connected"

# successful communication with the ELM327 adapter,
# OBD port connected to the car, ignition off
# (not available with argument "check_voltage=False")
OBDStatus.OBD_CONNECTED # "OBD Connected"

# successful communication with the ELM327 and the
# vehicle; ignition on
OBDStatus.CAR_CONNECTED # "Car Connected"
```

The status is set by `OBD()` or `Async()` methods and remains unmodified during the connection. `status()` shall not be checked after the queries to verify that the connection is kept active.

`ELM_CONNECTED` and `OBD_CONNECTED` are mostly for diagnosing errors. When a proper connection is established with the vehicle, you will never encounter these values.

The ELM327 controller allows OBD Commands and AT Commands. In general, OBD Commands (which interact with the car) can be succesfully performed when the ignition is on, while AT Commands (which generally interact with the ELM327 controller) are always accepted. As the connection phase (for both `OBD` and `Async` objects) also performs OBD protocol commands (after the initial set of AT Commands) and returns the “Car Connected” status (“CAR_CONNECTED”) if the overall connection phase is successful, this status means that the serial communication is valid, that the ELM327 adapter is appropriately responding, that the OBDII socket is connected to the car and also that the ignition is on. “OBD Connected” status (“OBD_CONNECTED”) is returned when the OBDII socket is connected and the ignition is off, while the "ELM Connected" status (“ELM_CONNECTED”) means that the ELM327 processor is reached but the OBDII socket is not connected to the car. “OBD Connected” is controlled by the `check_voltage` option that by default is set to `True` and gets the ignition status when the socket is connected. If the OBDII socket does not support the unswitched battery positive supply, or the OBDII adapter cannot detect it, then the `check_voltage` option should be set to `False`; in such case, the "ELM Connected" status is returned when the socket is not connected or when the ignition is off, with no differentiation.

---

### is_connected()

Returns a boolean for whether a connection was established with the vehicle. It is identical to writing:

```python
connection.status() == OBDStatus.CAR_CONNECTED
```

---

### port_name()

Returns the string name for the currently connected port (`"/dev/ttyUSB0"`). If no connection was made, this function returns an empty string.

---

### supports(command)

Returns a boolean for whether a command is supported by both the car and python-OBD

---

### protocol_id()
### protocol_name()

Both functions return string names for the protocol currently being used by the adapter. Protocol *ID's* are the short values used by your adapter, whereas protocol *names* are the human-readable versions. The `protocol_id()` function is a good way to lookup which value to pass in the `protocol` field of the OBD constructor (though, this is mainly for advanced usage). These functions do not make any serial requests. When no connection has been made, these functions will return empty strings. The possible values are:

|ID | Name                     |
|---|--------------------------|
| "1" | SAE J1850 PWM            |
| "2" | SAE J1850 VPW            |
| "3" | AUTO, ISO 9141-2         |
| "4" | ISO 14230-4 (KWP 5BAUD)  |
| "5" | ISO 14230-4 (KWP FAST)   |
| "6" | ISO 15765-4 (CAN 11/500) |
| "7" | ISO 15765-4 (CAN 29/500) |
| "8" | ISO 15765-4 (CAN 11/250) |
| "9" | ISO 15765-4 (CAN 29/250) |
| "A" | SAE J1939 (CAN 29/250)   |

*Note the quotations around the possible IDs*

---

<!--

### ecus()

Returns a list of identified "Engine Control Units" visible to the adapter. Each value in the list is a constant representing that ECU's function. These constants are found in the `ECU` class:

```python
from obd import ECU

ECU.UNKNOWN
ECU.ENGINE
```

Python-OBD can currently only detect the engine computer, but future versions may extend this capability.

-->

### close()

Closes the connection.

---

### supported_commands

Property containing a `set` of commands that are supported by the car.

If you wish to manually mark a command as supported (prevents having to use `query(force=True)`), add the command to this set. This is not necessary when using python-OBD's builtin commands, but is useful if you create [custom commands](Custom Commands.md).

```python
import obd
connection = obd.OBD()

# manually mark the given command as supported
connection.supported_commands.add(<OBDCommand>)
```
---

<br>
