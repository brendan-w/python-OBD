
import random
from obd.protocols import *
from obd.protocols.protocol import Message


LEGACY_PROTOCOLS = [
    SAE_J1850_PWM,
    SAE_J1850_VPW,
    ISO_9141_2,
    ISO_14230_4_5baud,
    ISO_14230_4_fast
]


def check_message(m, n_frames, tx_id, data):
    """ generic test for correct message values """
    assert len(m.frames) == n_frames
    assert m.tx_id == tx_id
    assert m.data == bytearray(data)


def test_single_frame():
    for protocol in LEGACY_PROTOCOLS:
        p = protocol([])

        # minimum valid length
        r = p(["48 6B 10 41 00 FF"])
        assert len(r) == 1
        check_message(r[0], 1, 0x10, [0x41, 0x00])

        # maximum valid length
        r = p(["48 6B 10 41 00 00 01 02 03 04 FF"])
        assert len(r) == 1
        check_message(r[0], 1, 0x10, [0x41, 0x00,
                                      0x00, 0x01, 0x02, 0x03, 0x04])

        # to short
        r = p(["48 6B 10 41 FF"])
        assert len(r) == 0

        # to long
        r = p(["48 6B 10 41 00 00 01 02 03 04 05 FF"])
        assert len(r) == 0

        # odd (invalid)
        r = p(["48 6B 10 41 00 00 F"])
        assert len(r) == 0


def test_hex_straining():
    """
        If non-hex values are sent, they should be marked as ECU.UNKNOWN
    """

    for protocol in LEGACY_PROTOCOLS:
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
        r = p(["NO DATA", "48 6B 10 41 00 00 01 02 03 FF"])
        assert len(r) == 2

        # first message should be the valid, parsable hex message
        # NOTE: the parser happens to process the valid one's first
        check_message(r[0], 1, 0x10, [0x41, 0x00, 0x00, 0x01, 0x02, 0x03])

        # second message: invalid, non-parsable non-hex
        assert r[1].ecu == ECU.UNKNOWN
        assert len(r[1].frames) == 1
        assert len(r[1].data) == 0  # no data


def test_multi_ecu():
    for protocol in LEGACY_PROTOCOLS:
        p = protocol([])

        test_case = [
            "48 6B 13 41 00 00 01 02 03 FF",
            "48 6B 10 41 00 00 01 02 03 FF",
            "48 6B 11 41 00 00 01 02 03 FF",
        ]

        correct_data = [0x41, 0x00, 0x00, 0x01, 0x02, 0x03]

        # seperate ECUs, single frames each
        r = p(test_case)
        assert len(r) == len(test_case)

        # messages are returned in ECU order
        check_message(r[0], 1, 0x10, correct_data)
        check_message(r[1], 1, 0x11, correct_data)
        check_message(r[2], 1, 0x13, correct_data)


def test_multi_line():
    """
        Tests that valid multiline messages are recombined into single
        messages.
    """

    for protocol in LEGACY_PROTOCOLS:
        p = protocol([])

        test_case = [
            "48 6B 10 49 02 01 00 01 02 03 FF",
            "48 6B 10 49 02 02 04 05 06 07 FF",
            "48 6B 10 49 02 03 08 09 0A 0B FF",
        ]

        correct_data = [0x49, 0x02] + list(range(12))

        # in-order
        r = p(test_case)
        assert len(r) == 1
        check_message(r[0], len(test_case), 0x10, correct_data)

        # test a few out-of-order cases
        for n in range(4):
            random.shuffle(test_case)  # mix up the frame strings
            r = p(test_case)
            assert len(r) == 1
            check_message(r[0], len(test_case), 0x10, correct_data)


def test_multi_line_missing_frames():
    """
        Missing frames in a multi-frame message should drop the message.
        Tests the contiguity check, and data length byte
    """

    for protocol in LEGACY_PROTOCOLS:
        p = protocol([])

        test_case = [
            "48 6B 10 49 02 01 00 01 02 03 FF",
            "48 6B 10 49 02 02 04 05 06 07 FF",
            "48 6B 10 49 02 03 08 09 0A 0B FF",
        ]

        for n in range(len(test_case) - 1):
            sub_test = list(test_case)
            del sub_test[n]

            r = p(sub_test)
            assert len(r) == 0


def test_multi_line_mode_03():
    """
        Tests the special handling of mode 3 commands.
        An extra byte is fudged in to make the output look like CAN
    """

    for protocol in LEGACY_PROTOCOLS:
        p = protocol([])

        test_case = [
            "48 6B 10 43 00 01 02 03 04 05 FF",
            "48 6B 10 43 06 07 08 09 0A 0B FF",
        ]

        # data is stitched in order recieved
        correct_data = [0x43, 0x00] + list(range(12))
        #                     ^^^^ this is an arbitrary value in the source code

        r = p(test_case)
        assert len(r) == 1
        check_message(r[0], len(test_case), 0x10, correct_data)
