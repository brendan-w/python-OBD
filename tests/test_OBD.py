
"""
    Tests for the API layer
"""

import obd
from obd import Unit
from obd import ECU
from obd.protocols.protocol import Message
from obd.utils import OBDStatus
from obd.OBDCommand import OBDCommand
from obd.decoders import noop


class FakeELM:
    """
        Fake ELM327 driver class for intercepting the commands from the API
    """

    def __init__(self, portname, UNUSED_baudrate=None, UNUSED_protocol=None):
        self._portname = portname
        self._status = OBDStatus.CAR_CONNECTED
        self._last_command = None

    def port_name(self):
        return self._portname

    def status(self):
        return self._status

    def ecus(self):
        return [ECU.ENGINE, ECU.UNKNOWN]

    def protocol_name(self):
        return "ISO 15765-4 (CAN 11/500)"

    def protocol_id(self):
        return "6"

    def close(self):
        pass

    def send_and_parse(self, cmd):
        # stow this, so we can check that the API made the right request
        print(cmd)
        self._last_command = cmd

        # all commands succeed
        message = Message([])
        message.data = bytearray(b'response data')
        message.ecu = ECU.ENGINE  # picked engine so that simple commands like RPM will work
        return [message]

    def _test_last_command(self, expected):
        r = self._last_command == expected
        self._last_command = None
        return r


# a toy command to test with
command = OBDCommand("Test_Command",
                     "A test command",
                     "0123456789ABCDEF",
                     0,
                     noop,
                     ECU.ALL,
                     True)


def test_is_connected():
    o = obd.OBD("/dev/null")
    assert not o.is_connected()

    # our fake ELM class always returns success for connections
    o.interface = FakeELM("/dev/null")
    assert o.is_connected()


def test_status():
    """
        Make sure that the API's status() function reports the
        same values as the underlying ELM327 class.
    """
    o = obd.OBD("/dev/null")
    assert o.status() == OBDStatus.NOT_CONNECTED

    o.interface = None
    assert o.status() == OBDStatus.NOT_CONNECTED

    # we can manually set our fake ELM class to test
    # the other values
    o.interface = FakeELM("/dev/null")

    o.interface._status = OBDStatus.ELM_CONNECTED
    assert o.status() == OBDStatus.ELM_CONNECTED

    o.interface._status = OBDStatus.CAR_CONNECTED
    assert o.status() == OBDStatus.CAR_CONNECTED


def test_supports():
    o = obd.OBD("/dev/null")

    # since we haven't actually connected,
    # no commands should be marked as supported
    assert not o.supports(obd.commands.RPM)
    o.supported_commands.add(obd.commands.RPM)
    assert o.supports(obd.commands.RPM)

    # commands that aren't in python-OBD's tables are unsupported by default
    assert not o.supports(command)


def test_port_name():
    """
        Make sure that the API's port_name() function reports the
        same values as the underlying ELM327 class.
    """
    o = obd.OBD("/dev/null")
    o.interface = FakeELM("/dev/null")
    assert o.port_name() == o.interface._portname

    o.interface = FakeELM("A different port name")
    assert o.port_name() == o.interface._portname


def test_protocol_name():
    o = obd.OBD("/dev/null")

    o.interface = None
    assert o.protocol_name() == ""

    o.interface = FakeELM("/dev/null")
    assert o.protocol_name() == o.interface.protocol_name()


def test_protocol_id():
    o = obd.OBD("/dev/null")

    o.interface = None
    assert o.protocol_id() == ""

    o.interface = FakeELM("/dev/null")
    assert o.protocol_id() == o.interface.protocol_id()


"""
    The following tests are for the query() function
"""


def test_force():
    # disable the trailing response count byte
    o = obd.OBD("/dev/null", fast=False)
    o.interface = FakeELM("/dev/null")

    r = o.query(obd.commands.RPM)
    assert r.is_null()
    assert o.interface._test_last_command(None)

    r = o.query(obd.commands.RPM, force=True)
    assert not r.is_null()
    assert o.interface._test_last_command(obd.commands.RPM.command)

    # a command that isn't in python-OBD's tables
    r = o.query(command)
    assert r.is_null()
    assert o.interface._test_last_command(None)

    r = o.query(command, force=True)
    assert o.interface._test_last_command(command.command)


def test_fast():
    o = obd.OBD("/dev/null", fast=False)
    o.interface = FakeELM("/dev/null")

    assert command.fast
    # force since this command isn't in the tables
    o.query(command, force=True)
    # assert o.interface._test_last_command(command.command)
