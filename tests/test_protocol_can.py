
import random
from obd.protocols import *
from obd.protocols.protocol import Message


CAN_11_PROTOCOLS = [
    ISO_15765_4_11bit_500k,
    ISO_15765_4_11bit_250k,
]

CAN_29_PROTOCOLS = [
    ISO_15765_4_29bit_500k,
    ISO_15765_4_29bit_250k,
    SAE_J1939
]


def check_message(m, num_frames, tx_id, data):
    """ generic test for correct message values """
    assert len(m.frames) == num_frames
    assert m.tx_id == tx_id
    assert m.data == bytearray(data)


def test_single_frame():
    for protocol in CAN_11_PROTOCOLS:
        p = protocol([])

        r = p(["7E8 06 41 00 00 01 02 03"])
        assert len(r) == 1
        check_message(r[0], 1, 0x0, [0x41, 0x00, 0x00, 0x01, 0x02, 0x03])

        # minimum valid length
        r = p(["7E8 01 41"])
        assert len(r) == 1
        check_message(r[0], 1, 0x0, [0x41])

        # maximum valid length
        r = p(["7E8 07 41 00 00 01 02 03 04"])
        assert len(r) == 1
        check_message(r[0], 1, 0x0, [0x41, 0x00, 0x00, 0x01, 0x02, 0x03, 0x04])

        # to short
        r = p(["7E8 01"])
        assert len(r) == 0

        # to long
        r = p(["7E8 08 41 00 00 01 02 03 04 05"])
        assert len(r) == 0

        # drop frames with zero data
        r = p(["7E8 00"])
        assert len(r) == 0

        # drop odd-sized frames (post padding)
        r = p(["7E8 08 41 00 00 01 02 03 04 0"])
        assert len(r) == 0


def test_hex_straining():
    """
        If non-hex values are sent, they should be marked as ECU.UNKNOWN
    """

    for protocol in CAN_11_PROTOCOLS:
        p = protocol([])

        # single non-hex message
        r = p(["12.8 Volts"])
        assert len(r) == 1
        assert r[0].ecu == ECU.UNKNOWN
        assert len(r[0].frames) == 1

        # multiple non-hex message
        r = p(["12.8 Volts", "NO DATA"])
        assert len(r) == 2

        for m in r:
            assert m.ecu == ECU.UNKNOWN
            assert len(m.frames) == 1

        # mixed hex and non-hex
        r = p(["NO DATA", "7E8 06 41 00 00 01 02 03"])
        assert len(r) == 2

        # first message should be the valid, parsable hex message
        # NOTE: the parser happens to process the valid one's first
        check_message(r[0], 1, 0x0, [0x41, 0x00, 0x00, 0x01, 0x02, 0x03])

        # second message: invalid, non-parsable non-hex
        assert r[1].ecu == ECU.UNKNOWN
        assert len(r[1].frames) == 1
        assert len(r[1].data) == 0  # no data


def test_multi_ecu():
    for protocol in CAN_11_PROTOCOLS:
        p = protocol([])

        test_case = [
            "7E8 06 41 00 00 01 02 03",
            "7EB 06 41 00 00 01 02 03",
            "7EA 06 41 00 00 01 02 03",
        ]

        correct_data = [0x41, 0x00, 0x00, 0x01, 0x02, 0x03]

        # seperate ECUs, single frames each
        r = p(test_case)
        assert len(r) == 3

        # messages are returned in ECU order
        check_message(r[0], 1, 0x0, correct_data)
        check_message(r[1], 1, 0x2, correct_data)
        check_message(r[2], 1, 0x3, correct_data)


def test_multi_line():
    """
        Tests that valid multiline messages are recombined into single
        messages.
    """

    for protocol in CAN_11_PROTOCOLS:
        p = protocol([])

        test_case = [
            "7E8 10 20 49 04 00 01 02 03",
            "7E8 21 04 05 06 07 08 09 0A",
            "7E8 22 0B 0C 0D 0E 0F 10 11",
            "7E8 23 12 13 14 15 16 17 18"
        ]

        correct_data = [0x49, 0x04] + list(range(25))

        # in-order
        r = p(test_case)
        assert len(r) == 1
        check_message(r[0], len(test_case), 0x0, correct_data)

        # test a few out-of-order cases
        for n in range(4):
            random.shuffle(test_case)  # mix up the frame strings
            r = p(test_case)
            assert len(r) == 1
            check_message(r[0], len(test_case), 0x0, correct_data)


def test_multi_line_missing_frames():
    """
        Missing frames in a multi-frame message should drop the message.
        Tests the contiguity check, and data length byte
    """

    for protocol in CAN_11_PROTOCOLS:
        p = protocol([])

        test_case = [
            "7E8 10 20 49 04 00 01 02 03",
            "7E8 21 04 05 06 07 08 09 0A",
            "7E8 22 0B 0C 0D 0E 0F 10 11",
            "7E8 23 12 13 14 15 16 17 18"
        ]

        for n in range(len(test_case) - 1):
            sub_test = list(test_case)
            del sub_test[n]

            r = p(sub_test)
            assert len(r) == 0


def test_multi_line_mode_03():
    """
        Tests the special handling of mode 3 commands.
        Namely, Mode 03 commands have a DTC count byte that is accounted for
        in the protocol layer.
    """

    for protocol in CAN_11_PROTOCOLS:
        p = protocol([])

        test_case = [
            "7E8 10 20 43 04 00 01 02 03",
            "7E8 21 04 05 06 07 08 09 0A",
        ]

        correct_data = [0x43, 0x04] + list(range(8))

        r = p(test_case)
        assert len(r) == 1
        check_message(r[0], len(test_case), 0, correct_data)


def test_can_29():
    pass
