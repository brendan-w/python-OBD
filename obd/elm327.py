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
# elm327.py                                                            #
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

import re
import serial
import time
import logging
from .protocols import *
from .utils import OBDStatus

logger = logging.getLogger(__name__)


class ELM327:
    """
        Handles communication with the ELM327 adapter.

        After instantiation with a portname (/dev/ttyUSB0, etc...),
        the following functions become available:

            send_and_parse()
            close()
            status()
            port_name()
            protocol_name()
            ecus()
    """

    # chevron (ELM prompt character)
    ELM_PROMPT = b'>'
    # an 'OK' which indicates we are entering low power state
    ELM_LP_ACTIVE = b'OK'

    _SUPPORTED_PROTOCOLS = {
        # "0" : None,
        # Automatic Mode. This isn't an actual protocol. If the
        # ELM reports this, then we don't have enough
        # information. see auto_protocol()
        "1": SAE_J1850_PWM,
        "2": SAE_J1850_VPW,
        "3": ISO_9141_2,
        "4": ISO_14230_4_5baud,
        "5": ISO_14230_4_fast,
        "6": ISO_15765_4_11bit_500k,
        "7": ISO_15765_4_29bit_500k,
        "8": ISO_15765_4_11bit_250k,
        "9": ISO_15765_4_29bit_250k,
        "A": SAE_J1939,
        # "B" : None, # user defined 1
        # "C" : None, # user defined 2
    }

    # used as a fallback, when ATSP0 doesn't cut it
    _TRY_PROTOCOL_ORDER = [
        "6",  # ISO_15765_4_11bit_500k
        "8",  # ISO_15765_4_11bit_250k
        "1",  # SAE_J1850_PWM
        "7",  # ISO_15765_4_29bit_500k
        "9",  # ISO_15765_4_29bit_250k
        "2",  # SAE_J1850_VPW
        "3",  # ISO_9141_2
        "4",  # ISO_14230_4_5baud
        "5",  # ISO_14230_4_fast
        "A",  # SAE_J1939
    ]

    # 38400, 9600 are the possible boot bauds (unless reprogrammed via
    # PP 0C).  19200, 38400, 57600, 115200, 230400, 500000 are listed on
    # p.46 of the ELM327 datasheet.
    #
    # Once pyserial supports non-standard baud rates on platforms other
    # than Linux, we'll add 500K to this list.
    #
    # We check the two default baud rates first, then go fastest to
    # slowest, on the theory that anyone who's using a slow baud rate is
    # going to be less picky about the time required to detect it.
    _TRY_BAUDS = [38400, 9600, 230400, 115200, 57600, 19200]

    def __init__(self, portname, baudrate, protocol, timeout,
                 check_voltage=True, start_low_power=False):
        """Initializes port by resetting device and gettings supported PIDs. """

        logger.info("Initializing ELM327: PORT=%s BAUD=%s PROTOCOL=%s" %
                    (
                        portname,
                        "auto" if baudrate is None else baudrate,
                        "auto" if protocol is None else protocol,
                    ))

        self.__status = OBDStatus.NOT_CONNECTED
        self.__port = None
        self.__protocol = UnknownProtocol([])
        self.__low_power = False
        self.timeout = timeout

        # ------------- open port -------------
        try:
            self.__port = serial.serial_for_url(portname,
                                                parity=serial.PARITY_NONE,
                                                stopbits=1,
                                                bytesize=8,
                                                timeout=10)  # seconds
        except serial.SerialException as e:
            self.__error(e)
            return
        except OSError as e:
            self.__error(e)
            return

        # If we start with the IC in the low power state we need to wake it up
        if start_low_power:
            self.__write(b" ")
            time.sleep(1)

        # ------------------------ find the ELM's baud ------------------------

        if not self.set_baudrate(baudrate):
            self.__error("Failed to set baudrate")
            return

        # ---------------------------- ATZ (reset) ----------------------------
        try:
            self.__send(b"ATZ", delay=1)  # wait 1 second for ELM to initialize
            # return data can be junk, so don't bother checking
        except serial.SerialException as e:
            self.__error(e)
            return

        # -------------------------- ATE0 (echo OFF) --------------------------
        r = self.__send(b"ATE0")
        if not self.__isok(r, expectEcho=True):
            self.__error("ATE0 did not return 'OK'")
            return

        # ------------------------- ATH1 (headers ON) -------------------------
        r = self.__send(b"ATH1")
        if not self.__isok(r):
            self.__error("ATH1 did not return 'OK', or echoing is still ON")
            return

        # ------------------------ ATL0 (linefeeds OFF) -----------------------
        r = self.__send(b"ATL0")
        if not self.__isok(r):
            self.__error("ATL0 did not return 'OK'")
            return

        # by now, we've successfuly communicated with the ELM, but not the car
        self.__status = OBDStatus.ELM_CONNECTED

        # -------------------------- AT RV (read volt) ------------------------
        if check_voltage:
            r = self.__send(b"AT RV")
            if not r or len(r) != 1 or r[0] == '':
                self.__error("No answer from 'AT RV'")
                return
            try:
                if float(r[0].lower().replace('v', '')) < 6:
                    logger.error("OBD2 socket disconnected")
                    return
            except ValueError as e:
                self.__error("Incorrect response from 'AT RV'")
                return
            # by now, we've successfuly connected to the OBD socket
            self.__status = OBDStatus.OBD_CONNECTED

        # try to communicate with the car, and load the correct protocol parser
        if self.set_protocol(protocol):
            self.__status = OBDStatus.CAR_CONNECTED
            logger.info("Connected Successfully: PORT=%s BAUD=%s PROTOCOL=%s" %
                        (
                            portname,
                            self.__port.baudrate,
                            self.__protocol.ELM_ID,
                        ))
        else:
            if self.__status == OBDStatus.OBD_CONNECTED:
                logger.error("Adapter connected, but the ignition is off")
            else:
                logger.error("Connected to the adapter, "
                             "but failed to connect to the vehicle")

    def set_protocol(self, protocol_):
        if protocol_ is not None:
            # an explicit protocol was specified
            if protocol_ not in self._SUPPORTED_PROTOCOLS:
                logger.error(
                    "{:} is not a valid protocol. ".format(protocol_) +
                    "Please use \"1\" through \"A\"")
                return False
            return self.manual_protocol(protocol_)
        else:
            # auto detect the protocol
            return self.auto_protocol()

    def manual_protocol(self, protocol_):
        r = self.__send(b"ATTP" + protocol_.encode())
        r0100 = self.__send(b"0100")

        if not self.__has_message(r0100, "UNABLE TO CONNECT"):
            # success, found the protocol
            self.__protocol = self._SUPPORTED_PROTOCOLS[protocol_](r0100)
            return True

        return False

    def auto_protocol(self):
        """
            Attempts communication with the car.

            If no protocol is specified, then protocols at tried with `ATTP`

            Upon success, the appropriate protocol parser is loaded,
            and this function returns True
        """

        # -------------- try the ELM's auto protocol mode --------------
        r = self.__send(b"ATSP0", delay=1)

        # -------------- 0100 (first command, SEARCH protocols) --------------
        r0100 = self.__send(b"0100", delay=1)
        if self.__has_message(r0100, "UNABLE TO CONNECT"):
            logger.error("Failed to query protocol 0100: unable to connect")
            return False

        # ------------------- ATDPN (list protocol number) -------------------
        r = self.__send(b"ATDPN")
        if len(r) != 1:
            logger.error("Failed to retrieve current protocol")
            return False

        p = r[0]  # grab the first (and only) line returned
        # suppress any "automatic" prefix
        p = p[1:] if (len(p) > 1 and p.startswith("A")) else p

        # check if the protocol is something we know
        if p in self._SUPPORTED_PROTOCOLS:
            # jackpot, instantiate the corresponding protocol handler
            self.__protocol = self._SUPPORTED_PROTOCOLS[p](r0100)
            return True
        else:
            # an unknown protocol
            # this is likely because not all adapter/car combinations work
            # in "auto" mode. Some respond to ATDPN responded with "0"
            logger.debug("ELM responded with unknown protocol. Trying them one-by-one")

            for p in self._TRY_PROTOCOL_ORDER:
                r = self.__send(b"ATTP" + p.encode())
                r0100 = self.__send(b"0100")
                if not self.__has_message(r0100, "UNABLE TO CONNECT"):
                    # success, found the protocol
                    self.__protocol = self._SUPPORTED_PROTOCOLS[p](r0100)
                    return True

        # if we've come this far, then we have failed...
        logger.error("Failed to determine protocol")
        return False

    def set_baudrate(self, baud):
        if baud is None:
            # when connecting to pseudo terminal, don't bother with auto baud
            if self.port_name().startswith("/dev/pts"):
                logger.debug("Detected pseudo terminal, skipping baudrate setup")
                return True
            else:
                return self.auto_baudrate()
        else:
            self.__port.baudrate = baud
            return True

    def auto_baudrate(self):
        """
        Detect the baud rate at which a connected ELM32x interface is operating.
        Returns boolean for success.
        """

        # before we change the timout, save the "normal" value
        timeout = self.__port.timeout
        self.__port.timeout = self.timeout  # we're only talking with the ELM, so things should go quickly

        for baud in self._TRY_BAUDS:
            self.__port.baudrate = baud
            self.__port.flushInput()
            self.__port.flushOutput()

            # Send a nonsense command to get a prompt back from the scanner
            # (an empty command runs the risk of repeating a dangerous command)
            # The first character might get eaten if the interface was busy,
            # so write a second one (again so that the lone CR doesn't repeat
            # the previous command)

            # All commands should be terminated with carriage return according
            # to ELM327 and STN11XX specifications
            self.__port.write(b"\x7F\x7F\r")
            self.__port.flush()
            response = self.__port.read(1024)
            logger.debug("Response from baud %d: %s" % (baud, repr(response)))

            # watch for the prompt character
            if response.endswith(b">"):
                logger.debug("Choosing baud %d" % baud)
                self.__port.timeout = timeout  # reinstate our original timeout
                return True

        logger.debug("Failed to choose baud")
        self.__port.timeout = timeout  # reinstate our original timeout
        return False

    def __isok(self, lines, expectEcho=False):
        if not lines:
            return False
        if expectEcho:
            # don't test for the echo itself
            # allow the adapter to already have echo disabled
            return self.__has_message(lines, 'OK')
        else:
            return len(lines) == 1 and lines[0] == 'OK'

    def __has_message(self, lines, text):
        for line in lines:
            if text in line:
                return True
        return False

    def __error(self, msg):
        """ handles fatal failures, print logger.info info and closes serial """
        self.close()
        logger.error(str(msg))

    def port_name(self):
        if self.__port is not None:
            return self.__port.portstr
        else:
            return ""

    def status(self):
        return self.__status

    def ecus(self):
        return self.__protocol.ecu_map.values()

    def protocol_name(self):
        return self.__protocol.ELM_NAME

    def protocol_id(self):
        return self.__protocol.ELM_ID

    def low_power(self):
        """
            Enter Low Power mode

            This command causes the ELM327 to shut off all but essential
            services.

            The ELM327 can be woken up by a message to the RS232 bus as
            well as a few other ways. See the Power Control section in
            the ELM327 datasheet for details on other ways to wake up
            the chip.

            Returns the status from the ELM327, 'OK' means low power mode
            is going to become active.
        """

        if self.__status == OBDStatus.NOT_CONNECTED:
            logger.info("cannot enter low power when unconnected")
            return None

        lines = self.__send(b"ATLP", delay=1, end_marker=self.ELM_LP_ACTIVE)

        if 'OK' in lines:
            logger.debug("Successfully entered low power mode")
            self.__low_power = True
        else:
            logger.debug("Failed to enter low power mode")

        return lines

    def normal_power(self):
        """
            Exit Low Power mode

            Send a space to trigger the RS232 to wakeup.

            This will send a space even if we aren't in low power mode as
            we want to ensure that we will be able to leave low power mode.

            See the Power Control section in the ELM327 datasheet for details
            on other ways to wake up the chip.

            Returns the status from the ELM327.
        """
        if self.__status == OBDStatus.NOT_CONNECTED:
            logger.info("cannot exit low power when unconnected")
            return None

        lines = self.__send(b" ")

        # Assume we woke up
        logger.debug("Successfully exited low power mode")
        self.__low_power = False

        return lines

    def close(self):
        """
            Resets the device, and sets all
            attributes to unconnected states.
        """

        self.__status = OBDStatus.NOT_CONNECTED
        self.__protocol = None

        if self.__port is not None:
            logger.info("closing port")
            self.__write(b"ATZ")
            self.__port.close()
            self.__port = None

    def send_and_parse(self, cmd):
        """
            send() function used to service all OBDCommands

            Sends the given command string, and parses the
            response lines with the protocol object.

            An empty command string will re-trigger the previous command

            Returns a list of Message objects
        """

        if self.__status == OBDStatus.NOT_CONNECTED:
            logger.info("cannot send_and_parse() when unconnected")
            return None

        # Check if we are in low power
        if self.__low_power == True:
            self.normal_power()

        lines = self.__send(cmd)
        messages = self.__protocol(lines)
        return messages

    def __send(self, cmd, delay=None, end_marker=ELM_PROMPT):
        """
            unprotected send() function

            will __write() the given string, no questions asked.
            returns result of __read() (a list of line strings)
            after an optional delay, until the end marker (by
            default, the prompt) is seen
        """
        self.__write(cmd)

        delayed = 0.0
        if delay is not None:
            logger.debug("wait: %d seconds" % delay)
            time.sleep(delay)
            delayed += delay

        r = self.__read(end_marker=end_marker)
        while delayed < 1.0 and len(r) <= 0:
            d = 0.1
            logger.debug("no response; wait: %f seconds" % d)
            time.sleep(d)
            delayed += d
            r = self.__read(end_marker=end_marker)
        return r

    def __write(self, cmd):
        """
            "low-level" function to write a string to the port
        """

        if self.__port:
            cmd += b"\r"  # terminate with carriage return in accordance with ELM327 and STN11XX specifications
            logger.debug("write: " + repr(cmd))
            try:
                self.__port.flushInput()  # dump everything in the input buffer
                self.__port.write(cmd)  # turn the string into bytes and write
                self.__port.flush()  # wait for the output buffer to finish transmitting
            except Exception:
                self.__status = OBDStatus.NOT_CONNECTED
                self.__port.close()
                self.__port = None
                logger.critical("Device disconnected while writing")
                return
        else:
            logger.info("cannot perform __write() when unconnected")

    def __read(self, end_marker=ELM_PROMPT):
        """
            "low-level" read function

            accumulates characters until the end marker (by
            default, the prompt character) is seen
            returns a list of [/r/n] delimited strings
        """
        if not self.__port:
            logger.info("cannot perform __read() when unconnected")
            return []

        buffer = bytearray()

        while True:
            # retrieve as much data as possible
            try:
                data = self.__port.read(self.__port.in_waiting or 1)
            except Exception:
                self.__status = OBDStatus.NOT_CONNECTED
                self.__port.close()
                self.__port = None
                logger.critical("Device disconnected while reading")
                return []

            # if nothing was received
            if not data:
                logger.warning("Failed to read port")
                break

            buffer.extend(data)

            # end on specified end-marker sequence
            if end_marker in buffer:
                break

        # log, and remove the "bytearray(   ...   )" part
        logger.debug("read: " + repr(buffer)[10:-1])

        # clean out any null characters
        buffer = re.sub(b"\x00", b"", buffer)

        # remove the prompt character
        if buffer.endswith(self.ELM_PROMPT):
            buffer = buffer[:-1]

        # convert bytes into a standard string
        string = buffer.decode("utf-8", "ignore")

        # splits into lines while removing empty lines and trailing spaces
        lines = [s.strip() for s in re.split("[\r\n]", string) if bool(s)]

        return lines
