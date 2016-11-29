# -*- coding: utf-8 -*-

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
# protocols/protocol_legacy.py                                         #
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

from binascii import unhexlify
from obd.utils import contiguous
from .protocol import Protocol, Message, Frame, ECU

import logging

logger = logging.getLogger(__name__)


class LegacyProtocol(Protocol):

    TX_ID_ENGINE = 0x10


    def __init__(self, lines_0100, allow_long_messages):
        Protocol.__init__(self, lines_0100)
        self.__allow_long_messages = allow_long_messages


    def parse_frame(self, frame):

        raw = frame.raw

        # Handle odd size frames and drop
        if len(raw) & 1:
            logger.debug("Dropping frame for being odd")
            return False

        raw_bytes = bytearray(unhexlify(raw))

        if len(raw_bytes) < 6:
            logger.debug("Dropped frame for being too short")
            return False

        if len(raw_bytes) > 11 and not self.__allow_long_messages:
            logger.debug("Dropped frame for being too long")
            return False

        # Ex.
        # [Header] [     Frame     ]
        # 48 6B 10 41 00 BE 7F B8 13 ck
        # ck = checksum byte

        # exclude header and trailing checksum (handled by ELM adapter)
        frame.data = raw_bytes[3:-1]

        # read header information
        frame.priority = raw_bytes[0]
        frame.rx_id    = raw_bytes[1]
        frame.tx_id    = raw_bytes[2]

        return True


    def parse_message(self, message):

        frames = message.frames

        # len(frames) will always be >= 1 (see the caller, protocol.py)
        mode = frames[0].data[0]

        # test that all frames are responses to the same Mode (SID)
        if len(frames) > 1:
            if not all([mode == f.data[0] for f in frames[1:]]):
                logger.debug("Recieved frames from multiple commands")
                return False

        # legacy protocols have different re-assembly
        # procedures for different Modes

        # ~~~~
        # NOTE: THERE ARE HACKS IN HERE to make some output compatible with CAN
        #       since CAN is the standard, and this is considered legacy, I'm
        #       fixing ugly inconsistencies between the two protocols here.
        # ~~~~

        if mode == 0x43:
            # GET_DTC requests return frames with no PID or order bytes
            # accumulate all of the data, minus the Mode bytes of each frame

            # Ex.
            # insert faux-byte to mimic the CAN style DTC requests
            #            |
            #          [ |     Frame      ]
            # 48 6B 10 43 03 00 03 02 03 03 ck
            # 48 6B 10 43 03 04 00 00 00 00 ck
            #             [     Data      ]

            message.data = bytearray([0x43, 0x00]) # forge the mode byte and CAN's DTC_count byte
            for f in frames:
                message.data += f.data[1:]

        else:
            if len(frames) == 1:
                # return data, excluding the mode/pid bytes

                # Ex.
                #          [  Frame/Data   ]
                # 48 6B 10 41 00 BE 7F B8 13 ck

                message.data = frames[0].data

            else: # len(frames) > 1:
                # generic multiline requests carry an order byte

                # Ex.
                #          [      Frame       ]
                # 48 6B 10 49 02 01 00 00 00 31 ck
                # 48 6B 10 49 02 02 44 34 47 50 ck
                # 48 6B 10 49 02 03 30 30 52 35 ck
                # etc...         [] [  Data   ]

                # becomes:
                # 49 02 [] 00 00 00 31 44 34 47 50 30 30 52 35
                #       |  [         ] [         ] [         ]
                #  order byte is removed

                # sort the frames by the order byte
                frames = sorted(frames, key=lambda f: f.data[2])

                # check contiguity
                indices = [f.data[2] for f in frames]
                if not contiguous(indices, 1, len(frames)):
                    logger.debug("Recieved multiline response with missing frames")
                    return False

                # now that they're in order, accumulate the data from each frame

                # preserve the first frame's mode and PID bytes (for consistency with CAN)
                frames[0].data.pop(2) # remove the sequence byte
                message.data = frames[0].data

                # add the data from the remaining frames
                for f in frames[1:]:
                    message.data += f.data[3:] # loose the mode/pid/seq bytes

        return True



##############################################
#                                            #
# Here lie the class stubs for each protocol #
#                                            #
##############################################



class SAE_J1850_PWM(LegacyProtocol):
    ELM_NAME = "SAE J1850 PWM"
    ELM_ID = "1"
    def __init__(self, lines_0100, allow_long_messages):
        LegacyProtocol.__init__(self, lines_0100, allow_long_messages)


class SAE_J1850_VPW(LegacyProtocol):
    ELM_NAME = "SAE J1850 VPW"
    ELM_ID = "2"
    def __init__(self, lines_0100, allow_long_messages):
        LegacyProtocol.__init__(self, lines_0100, allow_long_messages)


class ISO_9141_2(LegacyProtocol):
    ELM_NAME = "ISO 9141-2"
    ELM_ID = "3"
    def __init__(self, lines_0100, allow_long_messages):
        LegacyProtocol.__init__(self, lines_0100, allow_long_messages)


class ISO_14230_4_5baud(LegacyProtocol):
    ELM_NAME = "ISO 14230-4 (KWP 5BAUD)"
    ELM_ID = "4"
    def __init__(self, lines_0100, allow_long_messages):
        LegacyProtocol.__init__(self, lines_0100, allow_long_messages)


class ISO_14230_4_fast(LegacyProtocol):
    ELM_NAME = "ISO 14230-4 (KWP FAST)"
    ELM_ID = "5"
    def __init__(self, lines_0100, allow_long_messages):
        LegacyProtocol.__init__(self, lines_0100, allow_long_messages)
