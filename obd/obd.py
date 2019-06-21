# -*- coding: utf-8 -*-

########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2009 Peter J. Creath                                       #
# Copyright 2016 Brendan Whitfield (brendan-w.com)                     #
# Copyright 2019 Adaptant Solutions AG                                 #
#                                                                      #
########################################################################
#                                                                      #
# obd.py                                                               #
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

from .OBDResponse import OBDResponse
from .__version__ import __version__
from .commands import commands
from .elm327 import ELM327
from .protocols import ECU_HEADER
from .utils import scan_serial, OBDStatus

logger = logging.getLogger(__name__)


class OBD(object):
    """
        Class representing an OBD-II connection
        with it's assorted commands/sensors.
    """

    def __init__(self, portstr=None, baudrate=None, protocol=None, fast=True,
                 timeout=0.1, check_voltage=True, start_low_power=False):
        self.interface = None
        self.supported_commands = set(commands.base_commands())
        self.fast = fast  # global switch for disabling optimizations
        self.timeout = timeout
        self.__last_command = b""  # used for running the previous command with a CR
        self.__last_header = ECU_HEADER.ENGINE  # for comparing with the previously used header
        self.__frame_counts = {}  # keeps track of the number of return frames for each command

        logger.info("======================= python-OBD (v%s) =======================" % __version__)
        self.__connect(portstr, baudrate, protocol,
                       check_voltage, start_low_power)  # initialize by connecting and loading sensors
        self.__load_commands()  # try to load the car's supported commands
        logger.info("===================================================================")

    def __connect(self, portstr, baudrate, protocol, check_voltage,
                  start_low_power):
        """
            Attempts to instantiate an ELM327 connection object.
        """

        if portstr is None:
            logger.info("Using scan_serial to select port")
            port_names = scan_serial()
            logger.info("Available ports: " + str(port_names))

            if not port_names:
                logger.warning("No OBD-II adapters found")
                return

            for port in port_names:
                logger.info("Attempting to use port: " + str(port))
                self.interface = ELM327(port, baudrate, protocol,
                                        self.timeout, check_voltage,
                                        start_low_power)

                if self.interface.status() >= OBDStatus.ELM_CONNECTED:
                    break  # success! stop searching for serial
        else:
            logger.info("Explicit port defined")
            self.interface = ELM327(portstr, baudrate, protocol,
                                    self.timeout, check_voltage,
                                    start_low_power)

        # if the connection failed, close it
        if self.interface.status() == OBDStatus.NOT_CONNECTED:
            # the ELM327 class will report its own errors
            self.close()

    def __load_commands(self):
        """
            Queries for available PIDs, sets their support status,
            and compiles a list of command objects.
        """

        if self.status() != OBDStatus.CAR_CONNECTED:
            logger.warning("Cannot load commands: No connection to car")
            return

        logger.info("querying for supported commands")
        pid_getters = commands.pid_getters()
        for get in pid_getters:
            # PID listing commands should sequentially become supported
            # Mode 1 PID 0 is assumed to always be supported
            if not self.test_cmd(get, warn=False):
                continue

            # when querying, only use the blocking OBD.query()
            # prevents problems when query is redefined in a subclass (like Async)
            response = OBD.query(self, get)

            if response.is_null():
                logger.info("No valid data for PID listing command: %s" % get)
                continue

            # loop through PIDs bit-array
            for i, bit in enumerate(response.value):
                if bit:
                    mode = get.mode
                    if mode == 9:
                        pid = get.pid + (i - 7) + 1
                    else:
                        pid = get.pid + i + 1

                    if commands.has_pid(mode, pid):
                        self.supported_commands.add(commands[mode][pid])

                    # set support for mode 2 commands
                    if mode == 1 and commands.has_pid(2, pid):
                        self.supported_commands.add(commands[2][pid])

        logger.info("finished querying with %d commands supported" % len(self.supported_commands))

    def __set_header(self, header):
        if header == self.__last_header:
            return
        r = self.interface.send_and_parse(b'AT SH ' + header + b' ')
        if not r:
            logger.info("Set Header ('AT SH %s') did not return data", header)
            return OBDResponse()
        if "\n".join([m.raw() for m in r]) != "OK":
            logger.info("Set Header ('AT SH %s') did not return 'OK'", header)
            return OBDResponse()
        self.__last_header = header

    def close(self):
        """
            Closes the connection, and clears supported_commands
        """

        self.supported_commands = set()

        if self.interface is not None:
            logger.info("Closing connection")
            self.__set_header(ECU_HEADER.ENGINE)
            self.interface.close()
            self.interface = None

    def status(self):
        """ returns the OBD connection status """
        if self.interface is None:
            return OBDStatus.NOT_CONNECTED
        else:
            return self.interface.status()

    def low_power(self):
        """ Enter low power mode """
        if self.interface is None:
            return OBDStatus.NOT_CONNECTED
        else:
            return self.interface.low_power()

    def normal_power(self):
        """ Exit low power mode """
        if self.interface is None:
            return OBDStatus.NOT_CONNECTED
        else:
            return self.interface.normal_power()

    # not sure how useful this would be

    # def ecus(self):
    #     """ returns a list of ECUs in the vehicle """
    #     if self.interface is None:
    #         return []
    #     else:
    #         return self.interface.ecus()

    def protocol_name(self):
        """ returns the name of the protocol being used by the ELM327 """
        if self.interface is None:
            return ""
        else:
            return self.interface.protocol_name()

    def protocol_id(self):
        """ returns the ID of the protocol being used by the ELM327 """
        if self.interface is None:
            return ""
        else:
            return self.interface.protocol_id()

    def port_name(self):
        """ Returns the name of the currently connected port """
        if self.interface is not None:
            return self.interface.port_name()
        else:
            return ""

    def is_connected(self):
        """
            Returns a boolean for whether a connection with the car was made.

            Note: this function returns False when:
            obd.status = OBDStatus.ELM_CONNECTED
        """
        return self.status() == OBDStatus.CAR_CONNECTED

    def print_commands(self):
        """
            Utility function meant for working in interactive mode.
            Prints all commands supported by the car.
        """
        for c in self.supported_commands:
            print(str(c))

    def supports(self, cmd):
        """
            Returns a boolean for whether the given command
            is supported by the car
        """
        return cmd in self.supported_commands

    def test_cmd(self, cmd, warn=True):
        """
            Returns a boolean for whether a command will
            be sent without using force=True.
        """
        # test if the command is supported
        if not self.supports(cmd):
            if warn:
                logger.warning("'%s' is not supported" % str(cmd))
            return False

        # mode 06 is only implemented for the CAN protocols
        if cmd.mode == 6 and self.interface.protocol_id() not in ["6", "7", "8", "9"]:
            if warn:
                logger.warning("Mode 06 commands are only supported over CAN protocols")
            return False

        return True

    def query(self, cmd, force=False):
        """
            primary API function. Sends commands to the car, and
            protects against sending unsupported commands.
        """

        if self.status() == OBDStatus.NOT_CONNECTED:
            logger.warning("Query failed, no connection available")
            return OBDResponse()

        # if the user forces, skip all checks
        if not force and not self.test_cmd(cmd):
            return OBDResponse()

        self.__set_header(cmd.header)

        logger.info("Sending command: %s" % str(cmd))
        cmd_string = self.__build_command_string(cmd)
        messages = self.interface.send_and_parse(cmd_string)

        # if we're sending a new command, note it
        # first check that the current command WASN'T sent as an empty CR
        # (CR is added by the ELM327 class)
        if cmd_string:
            self.__last_command = cmd_string

        # if we don't already know how many frames this command returns,
        # log it, so we can specify it next time
        if cmd not in self.__frame_counts:
            self.__frame_counts[cmd] = sum([len(m.frames) for m in messages])

        if not messages:
            logger.info("No valid OBD Messages returned")
            return OBDResponse()

        return cmd(messages)  # compute a response object

    def __build_command_string(self, cmd):
        """ assembles the appropriate command string """
        cmd_string = cmd.command

        # if we know the number of frames that this command returns,
        # only wait for exactly that number. This avoids some harsh
        # timeouts from the ELM, thus speeding up queries.
        if self.fast and cmd.fast and (cmd in self.__frame_counts):
            cmd_string += str(self.__frame_counts[cmd]).encode()

        # if we sent this last time, just send a CR
        # (CR is added by the ELM327 class)
        if self.fast and (cmd_string == self.__last_command):
            cmd_string = b""

        return cmd_string
