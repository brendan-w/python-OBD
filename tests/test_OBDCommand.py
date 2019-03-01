
from obd.OBDCommand import OBDCommand
from obd.UnitsAndScaling import Unit
from obd.decoders import noop
from obd.protocols import *


def test_constructor():

    # default constructor
    #                 name       description        cmd  bytes decoder ECU
    cmd = OBDCommand("Test", "example OBD command",
                     b"0123", 2, noop, ECU.ENGINE)
    assert cmd.name == "Test"
    assert cmd.desc == "example OBD command"
    assert cmd.command == b"0123"
    assert cmd.bytes == 2
    assert cmd.decode == noop
    assert cmd.ecu == ECU.ENGINE
    assert cmd.fast == False

    assert cmd.mode == 1
    assert cmd.pid == 35

    # a case where "fast", and "supported" were set explicitly
    #                 name       description        cmd  bytes decoder ECU         fast
    cmd = OBDCommand("Test 2", "example OBD command",
                     b"0123", 2, noop, ECU.ENGINE, True)
    assert cmd.fast == True


def test_clone():
    #                 name       description        mode  cmd bytes decoder
    cmd = OBDCommand("", "", b"0123", 2, noop, ECU.ENGINE)
    other = cmd.clone()

    assert cmd.name == other.name
    assert cmd.desc == other.desc
    assert cmd.command == other.command
    assert cmd.bytes == other.bytes
    assert cmd.decode == other.decode
    assert cmd.ecu == other.ecu
    assert cmd.fast == cmd.fast


def test_call():
    # train the ecu_map to identify the engine
    p = SAE_J1850_PWM(["48 6B 10 41 00 FF FF FF FF AA"])
    # parse valid data into response object
    messages = p(["48 6B 10 41 00 BE 1F B8 11 AA"])

    print(messages[0].data)

    # valid response size
    cmd = OBDCommand("", "", b"0123", 6, noop, ECU.ENGINE)
    r = cmd(messages)
    assert r.value == bytearray([0x41, 0x00, 0xBE, 0x1F, 0xB8, 0x11])

    # response too short (pad)
    cmd = OBDCommand("", "", b"0123", 7, noop, ECU.ENGINE)
    r = cmd(messages)
    assert r.value == bytearray([0x41, 0x00, 0xBE, 0x1F, 0xB8, 0x11, 0x00])

    # response too long (clip)
    cmd = OBDCommand("", "", b"0123", 5, noop, ECU.ENGINE)
    r = cmd(messages)
    assert r.value == bytearray([0x41, 0x00, 0xBE, 0x1F, 0xB8])


def test_get_mode():
    cmd = OBDCommand("", "", b"0123", 4, noop, ECU.ENGINE)
    assert cmd.mode == 0x01

    cmd = OBDCommand("", "", b"", 4, noop, ECU.ENGINE)
    assert cmd.mode == None

    cmd = OBDCommand("", "", b"totally not hex", 4, noop, ECU.ENGINE)
    assert cmd.mode == None


def test_pid():
    cmd = OBDCommand("", "", b"0123", 4, noop, ECU.ENGINE)
    assert cmd.pid == 0x23

    cmd = OBDCommand("", "", b"01", 4, noop, ECU.ENGINE)
    assert cmd.pid == None

    cmd = OBDCommand("", "", b"totally not hex", 4, noop, ECU.ENGINE)
    assert cmd.mode == None
