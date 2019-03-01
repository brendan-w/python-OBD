
import random
from obd.protocols import *
from obd.protocols.protocol import Frame, Message


def test_ECU():
    # make sure none of the ECU ID values overlap
    tested = []

    # NOTE: does't include ECU.ALL
    for ecu in [ECU.UNKNOWN, ECU.ENGINE, ECU.TRANSMISSION]:
        assert (ECU.ALL & ecu) > 0, "ECU: %d is not included in ECU.ALL" % ecu

        for other_ecu in tested:
            assert (
                ecu & other_ecu) == 0, "ECU: %d has a conflicting bit with another ECU constant" % ecu

        tested.append(ecu)


def test_frame():
    # constructor
    frame = Frame("asdf")
    assert frame.raw == "asdf", "Frame failed to accept raw data as __init__ argument"
    assert frame.priority == None
    assert frame.addr_mode == None
    assert frame.rx_id == None
    assert frame.tx_id == None
    assert frame.type == None
    assert frame.seq_index == 0
    assert frame.data_len == None


def test_message():

    # constructor
    frame = Frame("raw input from OBD tool")
    frame.tx_id = 42

    frames = [frame]

    # a message is simply a special container for a bunch of frames
    message = Message(frames)

    assert message.frames == frames
    assert message.ecu == ECU.UNKNOWN
    assert message.tx_id == 42  # this is dynamically read from the first frame

    # if no frames are given, then we can't report a tx_id
    assert Message([]).tx_id == None


def test_message_hex():
    message = Message([])
    message.data = b'\x00\x01\x02'

    assert message.hex() == b'000102'
    assert int(message.hex()[0:2], 16) == 0x00
    assert int(message.hex()[2:4], 16) == 0x01
    assert int(message.hex()[4:6], 16) == 0x02
    assert int(message.hex(), 16) == 0x000102


def test_populate_ecu_map():
    # parse from messages

    # use primary ECU when multiple are present
    p = SAE_J1850_PWM(["48 6B 10 41 00 BE 1F B8 11 AA",
                       "48 6B 12 41 00 BE 1F B8 11 AA"])
    assert p.ecu_map[0x10] == ECU.ENGINE

    # use lone responses regardless
    p = SAE_J1850_PWM(["48 6B 12 41 00 BE 1F B8 11 AA"])
    assert p.ecu_map[0x12] == ECU.ENGINE

    # if primary ECU is not listed, use response with most PIDs supported
    p = SAE_J1850_PWM(["48 6B 12 41 00 BE 1F B8 11 AA",
                       "48 6B 14 41 00 00 00 B8 11 AA"])
    assert p.ecu_map[0x12] == ECU.ENGINE

    # if no messages were received, then the map is empty
    p = SAE_J1850_PWM([])
    assert len(p.ecu_map) == 0
