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
# OBDCommand.py                                                        #
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

from .utils import *
from .protocols import ECU, ECU_HEADER
from .OBDResponse import OBDResponse

import logging

logger = logging.getLogger(__name__)


class OBDCommand():
    def __init__(self,
                 name,
                 desc,
                 command,
                 _bytes,
                 decoder,
                 ecu=ECU.ALL,
                 fast=False,
                 header=ECU_HEADER.ENGINE):
        # human readable name (also used as key in commands dict)
        self.name = name
        self.desc = desc        # human readable description
        self.command = command     # command string
        self.bytes = _bytes      # number of bytes expected in return
        self.decode = decoder     # decoding function
        self.ecu = ecu         # ECU ID from which this command expects messages from
        # can an extra digit be added to the end of the command? (to make the ELM return early)
        self.fast = fast
        self.header = header      # ECU header used for the queries

    def clone(self):
        return OBDCommand(self.name,
                          self.desc,
                          self.command,
                          self.bytes,
                          self.decode,
                          self.ecu,
                          self.fast)

    @property
    def mode(self):
        if len(self.command) >= 2 and \
           isHex(self.command.decode()):
            return int(self.command[:2], 16)
        else:
            return None

    @property
    def pid(self):
        if len(self.command) > 2 and \
           isHex(self.command.decode()):
            return int(self.command[2:], 16)
        else:
            return None

    def __call__(self, messages):

        # filter for applicable messages (from the right ECU(s))
        def for_us(m): return (self.ecu & m.ecu) > 0
        messages = list(filter(for_us, messages))

        # guarantee data size for the decoder
        for m in messages:
            self.__constrain_message_data(m)

        # create the response object with the raw data recieved
        # and reference to original command
        r = OBDResponse(self, messages)
        if messages:
            r.value = self.decode(messages)
        else:
            logger.info(str(self) + " did not recieve any acceptable messages")

        return r

    def __constrain_message_data(self, message):
        """ pads or chops the data field to the size specified by this command """
        if self.bytes > 0:
            if len(message.data) > self.bytes:
                # chop off the right side
                message.data = message.data[:self.bytes]
                logger.debug(
                    "Message was longer than expected. Trimmed message: " + repr(message.data))
            elif len(message.data) < self.bytes:
                # pad the right with zeros
                message.data += (b'\x00' * (self.bytes - len(message.data)))
                logger.debug(
                    "Message was shorter than expected. Padded message: " + repr(message.data))

    def __str__(self):
        return "%s: %s" % (self.command, self.desc)

    def __hash__(self):
        # needed for using commands as keys in a dict (see async.py)
        return hash(self.command)

    def __eq__(self, other):
        if isinstance(other, OBDCommand):
            return (self.command == other.command)
        else:
            return False
