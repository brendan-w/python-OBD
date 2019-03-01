
from binascii import unhexlify
from obd.UnitsAndScaling import Unit, UAS_IDS


# shim to convert human-readable hex into bytearray
def b(_hex):
    return bytearray(unhexlify(_hex))


FLOAT_EQUALS_TOLERANCE = 0.025

# comparison for pint floating point values


def float_equals(va, vb):
    units_match = (va.u == vb.u)
    values_match = (abs(va.magnitude - vb.magnitude) < FLOAT_EQUALS_TOLERANCE)
    return values_match and units_match


"""
Unsigned Units
"""


def test_01():
    assert UAS_IDS[0x01](b("0000")) == 0 * Unit.count
    assert UAS_IDS[0x01](b("0001")) == 1 * Unit.count
    assert UAS_IDS[0x01](b("FFFF")) == 65535 * Unit.count


def test_02():
    assert UAS_IDS[0x02](b("0000")) == 0 * Unit.count
    assert UAS_IDS[0x02](b("0001")) == 0.1 * Unit.count
    assert UAS_IDS[0x02](b("FFFF")) == 6553.5 * Unit.count


def test_03():
    assert UAS_IDS[0x03](b("0000")) == 0 * Unit.count
    assert UAS_IDS[0x03](b("0001")) == 0.01 * Unit.count
    assert UAS_IDS[0x03](b("FFFF")) == 655.35 * Unit.count


def test_04():
    assert UAS_IDS[0x04](b("0000")) == 0 * Unit.count
    assert UAS_IDS[0x04](b("0001")) == 0.001 * Unit.count
    assert UAS_IDS[0x04](b("FFFF")) == 65.535 * Unit.count


def test_05():
    assert float_equals(UAS_IDS[0x05](b("0000")), 0 * Unit.count)
    assert float_equals(UAS_IDS[0x05](b("0001")), 0.0000305 * Unit.count)
    assert float_equals(UAS_IDS[0x05](b("FFFF")), 1.9999 * Unit.count)


def test_06():
    assert float_equals(UAS_IDS[0x06](b("0000")), 0 * Unit.count)
    assert float_equals(UAS_IDS[0x06](b("0001")), 0.000305 * Unit.count)
    assert float_equals(UAS_IDS[0x06](b("FFFF")), 19.988 * Unit.count)


def test_07():
    assert float_equals(UAS_IDS[0x07](b("0000")), 0 * Unit.rpm)
    assert float_equals(UAS_IDS[0x07](b("0002")), 0.5 * Unit.rpm)
    assert float_equals(UAS_IDS[0x07](b("FFFD")), 16383.25 * Unit.rpm)
    assert float_equals(UAS_IDS[0x07](b("FFFF")), 16383.75 * Unit.rpm)


def test_08():
    assert float_equals(UAS_IDS[0x08](b("0000")), 0 * Unit.kph)
    assert float_equals(UAS_IDS[0x08](b("0064")), 1 * Unit.kph)
    assert float_equals(UAS_IDS[0x08](b("03E7")), 9.99 * Unit.kph)
    assert float_equals(UAS_IDS[0x08](b("FFFF")), 655.35 * Unit.kph)


def test_09():
    assert float_equals(UAS_IDS[0x09](b("0000")), 0 * Unit.kph)
    assert float_equals(UAS_IDS[0x09](b("0064")), 100 * Unit.kph)
    assert float_equals(UAS_IDS[0x09](b("03E7")), 999 * Unit.kph)
    assert float_equals(UAS_IDS[0x09](b("FFFF")), 65535 * Unit.kph)


def test_0A():
    # the standard gives example values that don't line up perfectly
    # with the scale. The last two tests here deviate from the standard
    assert float_equals(UAS_IDS[0x0A](b("0000")), 0 * Unit.millivolt)
    assert float_equals(UAS_IDS[0x0A](b("0001")), 0.122 * Unit.millivolt)
    assert float_equals(UAS_IDS[0x0A](b("2004")),
                        999.912 * Unit.millivolt)  # 1000.488 mV
    assert float_equals(UAS_IDS[0x0A](b("FFFF")),
                        7995.27 * Unit.millivolt)  # 7999 mV


def test_0B():
    assert UAS_IDS[0x0B](b("0000")) == 0 * Unit.volt
    assert UAS_IDS[0x0B](b("0001")) == 0.001 * Unit.volt
    assert UAS_IDS[0x0B](b("FFFF")) == 65.535 * Unit.volt


def test_0C():
    assert float_equals(UAS_IDS[0x0C](b("0000")), 0 * Unit.volt)
    assert float_equals(UAS_IDS[0x0C](b("0001")), 0.01 * Unit.volt)
    assert float_equals(UAS_IDS[0x0C](b("FFFF")), 655.350 * Unit.volt)


def test_0D():
    assert float_equals(UAS_IDS[0x0D](b("0000")), 0 * Unit.milliampere)
    assert float_equals(UAS_IDS[0x0D](b("0001")), 0.004 * Unit.milliampere)
    assert float_equals(UAS_IDS[0x0D](b("8000")), 128 * Unit.milliampere)
    assert float_equals(UAS_IDS[0x0D](b("FFFF")), 255.996 * Unit.milliampere)


def test_0E():
    assert UAS_IDS[0x0E](b("0000")) == 0 * Unit.ampere
    assert UAS_IDS[0x0E](b("8000")) == 32.768 * Unit.ampere
    assert UAS_IDS[0x0E](b("FFFF")) == 65.535 * Unit.ampere


def test_0F():
    assert UAS_IDS[0x0F](b("0000")) == 0 * Unit.ampere
    assert UAS_IDS[0x0F](b("0001")) == 0.01 * Unit.ampere
    assert UAS_IDS[0x0F](b("FFFF")) == 655.35 * Unit.ampere


def test_10():
    assert UAS_IDS[0x10](b("0000")) == 0 * Unit.millisecond
    assert UAS_IDS[0x10](b("8000")) == 32768 * Unit.millisecond
    assert UAS_IDS[0x10](b("EA60")) == 60000 * Unit.millisecond
    assert UAS_IDS[0x10](b("FFFF")) == 65535 * Unit.millisecond


def test_11():
    assert UAS_IDS[0x11](b("0000")) == 0 * Unit.millisecond
    assert UAS_IDS[0x11](b("8000")) == 3276800 * Unit.millisecond
    assert UAS_IDS[0x11](b("EA60")) == 6000000 * Unit.millisecond
    assert UAS_IDS[0x11](b("FFFF")) == 6553500 * Unit.millisecond


def test_12():
    assert UAS_IDS[0x12](b("0000")) == 0 * Unit.second
    assert UAS_IDS[0x12](b("003C")) == 60 * Unit.second
    assert UAS_IDS[0x12](b("0E10")) == 3600 * Unit.second
    assert UAS_IDS[0x12](b("FFFF")) == 65535 * Unit.second


def test_13():
    assert UAS_IDS[0x13](b("0000")) == 0 * Unit.milliohm
    assert UAS_IDS[0x13](b("0001")) == 1 * Unit.milliohm
    assert UAS_IDS[0x13](b("8000")) == 32768 * Unit.milliohm
    assert UAS_IDS[0x13](b("FFFF")) == 65535 * Unit.milliohm


def test_14():
    assert UAS_IDS[0x14](b("0000")) == 0 * Unit.ohm
    assert UAS_IDS[0x14](b("0001")) == 1 * Unit.ohm
    assert UAS_IDS[0x14](b("8000")) == 32768 * Unit.ohm
    assert UAS_IDS[0x14](b("FFFF")) == 65535 * Unit.ohm


def test_15():
    assert UAS_IDS[0x15](b("0000")) == 0 * Unit.kiloohm
    assert UAS_IDS[0x15](b("0001")) == 1 * Unit.kiloohm
    assert UAS_IDS[0x15](b("8000")) == 32768 * Unit.kiloohm
    assert UAS_IDS[0x15](b("FFFF")) == 65535 * Unit.kiloohm


def test_16():
    assert UAS_IDS[0x16](b("0000")) == Unit.Quantity(-40, Unit.celsius)
    assert UAS_IDS[0x16](b("0001")) == Unit.Quantity(-39.9, Unit.celsius)
    assert UAS_IDS[0x16](b("00DC")) == Unit.Quantity(-18, Unit.celsius)
    assert UAS_IDS[0x16](b("0190")) == Unit.Quantity(0, Unit.celsius)
    assert UAS_IDS[0x16](b("FFFF")) == Unit.Quantity(6513.5, Unit.celsius)


def test_17():
    assert UAS_IDS[0x17](b("0000")) == 0 * Unit.kilopascal
    assert UAS_IDS[0x17](b("0001")) == 0.01 * Unit.kilopascal
    assert UAS_IDS[0x17](b("FFFF")) == 655.35 * Unit.kilopascal


def test_18():
    assert UAS_IDS[0x18](b("0000")) == 0 * Unit.kilopascal
    assert UAS_IDS[0x18](b("0001")) == 0.0117 * Unit.kilopascal
    assert UAS_IDS[0x18](b("FFFF")) == 766.7595 * Unit.kilopascal


def test_19():
    assert UAS_IDS[0x19](b("0000")) == 0 * Unit.kilopascal
    assert UAS_IDS[0x19](b("0001")) == 0.079 * Unit.kilopascal
    assert UAS_IDS[0x19](b("FFFF")) == 5177.265 * Unit.kilopascal


def test_1A():
    assert UAS_IDS[0x1A](b("0000")) == 0 * Unit.kilopascal
    assert UAS_IDS[0x1A](b("0001")) == 1 * Unit.kilopascal
    assert UAS_IDS[0x1A](b("FFFF")) == 65535 * Unit.kilopascal


def test_1B():
    assert UAS_IDS[0x1B](b("0000")) == 0 * Unit.kilopascal
    assert UAS_IDS[0x1B](b("0001")) == 10 * Unit.kilopascal
    assert UAS_IDS[0x1B](b("FFFF")) == 655350 * Unit.kilopascal


def test_1C():
    assert UAS_IDS[0x1C](b("0000")) == 0 * Unit.degree
    assert UAS_IDS[0x1C](b("0001")) == 0.01 * Unit.degree
    assert UAS_IDS[0x1C](b("8CA0")) == 360 * Unit.degree
    assert UAS_IDS[0x1C](b("FFFF")) == 655.35 * Unit.degree


def test_1D():
    assert UAS_IDS[0x1D](b("0000")) == 0 * Unit.degree
    assert UAS_IDS[0x1D](b("0001")) == 0.5 * Unit.degree
    assert UAS_IDS[0x1D](b("FFFF")) == 32767.5 * Unit.degree


def test_1E():
    assert float_equals(UAS_IDS[0x1E](b("0000")), 0 * Unit.ratio)
    assert float_equals(UAS_IDS[0x1E](b("8013")), 1 * Unit.ratio)
    assert float_equals(UAS_IDS[0x1E](b("FFFF")), 1.999 * Unit.ratio)


def test_1F():
    assert float_equals(UAS_IDS[0x1F](b("0000")), 0 * Unit.ratio)
    assert float_equals(UAS_IDS[0x1F](b("0001")), 0.05 * Unit.ratio)
    assert float_equals(UAS_IDS[0x1F](b("0014")), 1 * Unit.ratio)
    assert float_equals(UAS_IDS[0x1F](b("0126")), 14.7 * Unit.ratio)
    assert float_equals(UAS_IDS[0x1F](b("FFFF")), 3276.75 * Unit.ratio)


def test_20():
    assert float_equals(UAS_IDS[0x20](b("0000")), 0 * Unit.ratio)
    assert float_equals(UAS_IDS[0x20](b("0001")), 0.0039062 * Unit.ratio)
    assert float_equals(UAS_IDS[0x20](b("FFFF")), 255.993 * Unit.ratio)


def test_21():
    assert UAS_IDS[0x21](b("0000")) == 0 * Unit.millihertz
    assert UAS_IDS[0x21](b("8000")) == 32768 * Unit.millihertz
    assert UAS_IDS[0x21](b("FFFF")) == 65535 * Unit.millihertz


def test_22():
    assert UAS_IDS[0x22](b("0000")) == 0 * Unit.hertz
    assert UAS_IDS[0x22](b("8000")) == 32768 * Unit.hertz
    assert UAS_IDS[0x22](b("FFFF")) == 65535 * Unit.hertz


def test_23():
    assert UAS_IDS[0x23](b("0000")) == 0 * Unit.kilohertz
    assert UAS_IDS[0x23](b("8000")) == 32768 * Unit.kilohertz
    assert UAS_IDS[0x23](b("FFFF")) == 65535 * Unit.kilohertz


def test_24():
    assert UAS_IDS[0x24](b("0000")) == 0 * Unit.count
    assert UAS_IDS[0x24](b("0001")) == 1 * Unit.count
    assert UAS_IDS[0x24](b("FFFF")) == 65535 * Unit.count


def test_25():
    assert UAS_IDS[0x25](b("0000")) == 0 * Unit.kilometer
    assert UAS_IDS[0x25](b("0001")) == 1 * Unit.kilometer
    assert UAS_IDS[0x25](b("FFFF")) == 65535 * Unit.kilometer


def test_26():
    assert UAS_IDS[0x26](b("0000")) == 0 * Unit.millivolt / Unit.millisecond
    assert UAS_IDS[0x26](b("0001")) == 0.1 * Unit.millivolt / Unit.millisecond
    assert UAS_IDS[0x26](b("FFFF")) == 6553.5 * \
        Unit.millivolt / Unit.millisecond


def test_27():
    assert UAS_IDS[0x27](b("0000")) == 0 * Unit.grams_per_second
    assert UAS_IDS[0x27](b("0001")) == 0.01 * Unit.grams_per_second
    assert UAS_IDS[0x27](b("FFFF")) == 655.35 * Unit.grams_per_second


def test_28():
    assert UAS_IDS[0x28](b("0000")) == 0 * Unit.grams_per_second
    assert UAS_IDS[0x28](b("0001")) == 1 * Unit.grams_per_second
    assert UAS_IDS[0x28](b("FFFF")) == 65535 * Unit.grams_per_second


def test_29():
    assert UAS_IDS[0x29](b("0000")) == 0 * Unit.pascal / Unit.second
    assert UAS_IDS[0x29](b("0004")) == 1 * Unit.pascal / Unit.second
    assert UAS_IDS[0x29](b("FFFF")) == 16383.75 * Unit.pascal / \
        Unit.second  # deviates from standard examples


def test_2A():
    assert UAS_IDS[0x2A](b("0000")) == 0 * Unit.kilogram / Unit.hour
    assert UAS_IDS[0x2A](b("0001")) == 0.001 * Unit.kilogram / Unit.hour
    assert UAS_IDS[0x2A](b("FFFF")) == 65.535 * Unit.kilogram / Unit.hour


def test_2B():
    assert UAS_IDS[0x2B](b("0000")) == 0 * Unit.count
    assert UAS_IDS[0x2B](b("0001")) == 1 * Unit.count
    assert UAS_IDS[0x2B](b("FFFF")) == 65535 * Unit.count


def test_2C():
    assert UAS_IDS[0x2C](b("0000")) == 0 * Unit.gram
    assert UAS_IDS[0x2C](b("0001")) == 0.01 * Unit.gram
    assert UAS_IDS[0x2C](b("FFFF")) == 655.35 * Unit.gram


def test_2D():
    assert UAS_IDS[0x2D](b("0000")) == 0 * Unit.milligram
    assert UAS_IDS[0x2D](b("0001")) == 0.01 * Unit.milligram
    assert UAS_IDS[0x2D](b("FFFF")) == 655.35 * Unit.milligram


def test_2E():
    assert UAS_IDS[0x2E](b("0000")) == False
    assert UAS_IDS[0x2E](b("0001")) == True
    assert UAS_IDS[0x2E](b("FFFF")) == True


def test_2F():
    assert UAS_IDS[0x2F](b("0000")) == 0 * Unit.percent
    assert UAS_IDS[0x2F](b("0001")) == 0.01 * Unit.percent
    assert UAS_IDS[0x2F](b("2710")) == 100 * Unit.percent
    assert UAS_IDS[0x2F](b("FFFF")) == 655.35 * Unit.percent


def test_30():
    assert float_equals(UAS_IDS[0x30](b("0000")), 0 * Unit.percent)
    assert float_equals(UAS_IDS[0x30](b("0001")), 0.001526 * Unit.percent)
    assert float_equals(UAS_IDS[0x30](b("FFFF")), 100.00641 * Unit.percent)


def test_31():
    assert UAS_IDS[0x31](b("0000")) == 0 * Unit.liter
    assert UAS_IDS[0x31](b("0001")) == 0.001 * Unit.liter
    assert UAS_IDS[0x31](b("FFFF")) == 65.535 * Unit.liter


def test_32():
    assert float_equals(UAS_IDS[0x32](b("0000")), 0 * Unit.inch)
    assert float_equals(UAS_IDS[0x32](b("0010")), 0.0004883 * Unit.inch)
    assert float_equals(UAS_IDS[0x32](b("0011")), 0.0005188 * Unit.inch)
    assert float_equals(UAS_IDS[0x32](b("FFFF")), 1.9999695 * Unit.inch)


def test_33():
    assert float_equals(UAS_IDS[0x33](b("0000")), 0 * Unit.ratio)
    assert float_equals(UAS_IDS[0x33](b("0001")), 0.00024414 * Unit.ratio)
    assert float_equals(UAS_IDS[0x33](b("1000")), 1.0 * Unit.ratio)
    assert float_equals(UAS_IDS[0x33](b("E5BE")), 14.36 * Unit.ratio)
    assert float_equals(UAS_IDS[0x33](b("FFFF")), 16.0 * Unit.ratio)


def test_34():
    assert UAS_IDS[0x34](b("0000")) == 0 * Unit.minute
    assert UAS_IDS[0x34](b("003C")) == 60 * Unit.minute
    assert UAS_IDS[0x34](b("0E10")) == 3600 * Unit.minute
    assert UAS_IDS[0x34](b("FFFF")) == 65535 * Unit.minute


def test_35():
    assert UAS_IDS[0x35](b("0000")) == 0 * Unit.millisecond
    assert UAS_IDS[0x35](b("8000")) == 327680 * Unit.millisecond
    assert UAS_IDS[0x35](b("EA60")) == 600000 * Unit.millisecond
    assert UAS_IDS[0x35](b("FFFF")) == 655350 * Unit.millisecond


def test_36():
    assert UAS_IDS[0x36](b("0000")) == 0 * Unit.gram
    assert UAS_IDS[0x36](b("0001")) == 0.01 * Unit.gram
    assert UAS_IDS[0x36](b("FFFF")) == 655.35 * Unit.gram


def test_37():
    assert UAS_IDS[0x37](b("0000")) == 0 * Unit.gram
    assert UAS_IDS[0x37](b("0001")) == 0.1 * Unit.gram
    assert UAS_IDS[0x37](b("FFFF")) == 6553.5 * Unit.gram


def test_38():
    assert UAS_IDS[0x38](b("0000")) == 0 * Unit.gram
    assert UAS_IDS[0x38](b("0001")) == 1 * Unit.gram
    assert UAS_IDS[0x38](b("FFFF")) == 65535 * Unit.gram


def test_39():
    assert float_equals(UAS_IDS[0x39](b("0000")), -327.68 * Unit.percent)
    assert float_equals(UAS_IDS[0x39](b("58F0")), -100 * Unit.percent)
    assert float_equals(UAS_IDS[0x39](b("7FFF")), -0.01 * Unit.percent)
    assert float_equals(UAS_IDS[0x39](b("8000")), 0 * Unit.percent)
    assert float_equals(UAS_IDS[0x39](b("8001")), 0.01 * Unit.percent)
    assert float_equals(UAS_IDS[0x39](b("A710")), 100 * Unit.percent)
    assert float_equals(UAS_IDS[0x39](b("FFFF")), 327.67 * Unit.percent)


def test_3A():
    assert UAS_IDS[0x3A](b("0000")) == 0 * Unit.gram
    assert UAS_IDS[0x3A](b("0001")) == 0.001 * Unit.gram
    assert UAS_IDS[0x3A](b("FFFF")) == 65.535 * Unit.gram


def test_3B():
    assert float_equals(UAS_IDS[0x3B](b("0000")), 0 * Unit.gram)
    assert float_equals(UAS_IDS[0x3B](b("0001")), 0.0001 * Unit.gram)
    assert float_equals(UAS_IDS[0x3B](b("FFFF")), 6.5535 * Unit.gram)


def test_3C():
    assert UAS_IDS[0x3C](b("0000")) == 0 * Unit.microsecond
    assert UAS_IDS[0x3C](b("8000")) == 3276.8 * Unit.microsecond
    assert UAS_IDS[0x3C](b("EA60")) == 6000.0 * Unit.microsecond
    assert UAS_IDS[0x3C](b("FFFF")) == 6553.5 * Unit.microsecond


def test_3D():
    assert UAS_IDS[0x3D](b("0000")) == 0 * Unit.milliampere
    assert UAS_IDS[0x3D](b("0001")) == 0.01 * Unit.milliampere
    assert UAS_IDS[0x3D](b("FFFF")) == 655.35 * Unit.milliampere


def test_3E():
    assert float_equals(UAS_IDS[0x3E](b("0000")), 0 * Unit.millimeter ** 2)
    assert float_equals(UAS_IDS[0x3E](b("8000")),
                        1.9999 * Unit.millimeter ** 2)
    assert float_equals(UAS_IDS[0x3E](b("FFFF")),
                        3.9999 * Unit.millimeter ** 2)


def test_3F():
    assert UAS_IDS[0x3F](b("0000")) == 0 * Unit.liter
    assert UAS_IDS[0x3F](b("0001")) == 0.01 * Unit.liter
    assert UAS_IDS[0x3F](b("FFFF")) == 655.35 * Unit.liter


def test_40():
    assert UAS_IDS[0x40](b("0000")) == 0 * Unit.ppm
    assert UAS_IDS[0x40](b("0001")) == 1 * Unit.ppm
    assert UAS_IDS[0x40](b("FFFF")) == 65535 * Unit.ppm


def test_41():
    assert UAS_IDS[0x41](b("0000")) == 0 * Unit.microampere
    assert UAS_IDS[0x41](b("0001")) == 0.01 * Unit.microampere
    assert UAS_IDS[0x41](b("FFFF")) == 655.35 * Unit.microampere


"""
signed Units
"""


def test_81():
    assert UAS_IDS[0x81](b("8000")) == -32768 * Unit.count
    assert UAS_IDS[0x81](b("FFFF")) == -1 * Unit.count
    assert UAS_IDS[0x81](b("0000")) == 0 * Unit.count
    assert UAS_IDS[0x81](b("0001")) == 1 * Unit.count
    assert UAS_IDS[0x81](b("7FFF")) == 32767 * Unit.count


def test_82():
    assert UAS_IDS[0x82](b("8000")) == -3276.8 * Unit.count
    assert UAS_IDS[0x82](b("FFFF")) == -0.1 * Unit.count
    assert UAS_IDS[0x82](b("0000")) == 0 * Unit.count
    assert UAS_IDS[0x82](b("0001")) == 0.1 * Unit.count
    assert float_equals(UAS_IDS[0x82](b("7FFF")), 3276.7 * Unit.count)


def test_83():
    assert UAS_IDS[0x83](b("8000")) == -327.68 * Unit.count
    assert UAS_IDS[0x83](b("FFFF")) == -0.01 * Unit.count
    assert UAS_IDS[0x83](b("0000")) == 0 * Unit.count
    assert UAS_IDS[0x83](b("0001")) == 0.01 * Unit.count
    assert float_equals(UAS_IDS[0x83](b("7FFF")), 327.67 * Unit.count)


def test_84():
    assert UAS_IDS[0x84](b("8000")) == -32.768 * Unit.count
    assert UAS_IDS[0x84](b("FFFF")) == -0.001 * Unit.count
    assert UAS_IDS[0x84](b("0000")) == 0 * Unit.count
    assert UAS_IDS[0x84](b("0001")) == 0.001 * Unit.count
    assert float_equals(UAS_IDS[0x84](b("7FFF")), 32.767 * Unit.count)


def test_85():
    assert float_equals(UAS_IDS[0x85](b("8000")), -0.9999995 * Unit.count)
    assert float_equals(UAS_IDS[0x85](b("FFFF")), -0.0000305 * Unit.count)
    assert float_equals(UAS_IDS[0x85](b("0000")), 0 * Unit.count)
    assert float_equals(UAS_IDS[0x85](b("0001")), 0.0000305 * Unit.count)
    assert float_equals(UAS_IDS[0x85](b("7FFF")), 0.9999995 * Unit.count)


def test_86():
    assert float_equals(UAS_IDS[0x86](b("8000")), -9.999995 * Unit.count)
    assert float_equals(UAS_IDS[0x86](b("FFFF")), -0.000305 * Unit.count)
    assert float_equals(UAS_IDS[0x86](b("0000")), 0 * Unit.count)
    assert float_equals(UAS_IDS[0x86](b("0001")), 0.000305 * Unit.count)
    assert float_equals(UAS_IDS[0x86](b("7FFF")), 9.999995 * Unit.count)


def test_87():
    assert UAS_IDS[0x87](b("8000")) == -32768 * Unit.ppm
    assert UAS_IDS[0x87](b("FFFF")) == -1 * Unit.ppm
    assert UAS_IDS[0x87](b("0000")) == 0 * Unit.ppm
    assert UAS_IDS[0x87](b("0001")) == 1 * Unit.ppm
    assert UAS_IDS[0x87](b("7FFF")) == 32767 * Unit.ppm


def test_8A():
    # the standard gives example values that don't line up perfectly
    # with the scale. The last two tests here deviate from the standard
    assert float_equals(UAS_IDS[0x8A](b("8000")), -
                        3997.696 * Unit.millivolt)  # -3999.998 mV
    assert float_equals(UAS_IDS[0x8A](b("FFFF")), -0.122 * Unit.millivolt)
    assert float_equals(UAS_IDS[0x8A](b("0000")), 0 * Unit.millivolt)
    assert float_equals(UAS_IDS[0x8A](b("0001")), 0.122 * Unit.millivolt)
    assert float_equals(UAS_IDS[0x8A](b("7FFF")),
                        3997.574 * Unit.millivolt)  # 3999.876 mV


def test_8B():
    assert UAS_IDS[0x8B](b("8000")) == -32.768 * Unit.volt
    assert UAS_IDS[0x8B](b("FFFF")) == -0.001 * Unit.volt
    assert UAS_IDS[0x8B](b("0000")) == 0 * Unit.volt
    assert UAS_IDS[0x8B](b("0001")) == 0.001 * Unit.volt
    assert UAS_IDS[0x8B](b("7FFF")) == 32.767 * Unit.volt


def test_8C():
    assert UAS_IDS[0x8C](b("8000")) == -327.68 * Unit.volt
    assert UAS_IDS[0x8C](b("FFFF")) == -0.01 * Unit.volt
    assert UAS_IDS[0x8C](b("0000")) == 0 * Unit.volt
    assert UAS_IDS[0x8C](b("0001")) == 0.01 * Unit.volt
    assert UAS_IDS[0x8C](b("7FFF")) == 327.67 * Unit.volt


def test_8D():
    assert float_equals(UAS_IDS[0x8D](b("8000")), -128 * Unit.milliampere)
    assert float_equals(UAS_IDS[0x8D](b("FFFF")), -
                        0.00390625 * Unit.milliampere)
    assert float_equals(UAS_IDS[0x8D](b("0000")), 0 * Unit.milliampere)
    assert float_equals(UAS_IDS[0x8D](b("0001")),
                        0.00390625 * Unit.milliampere)
    assert float_equals(UAS_IDS[0x8D](b("7FFF")), 127.996 * Unit.milliampere)


def test_8E():
    assert UAS_IDS[0x8E](b("8000")) == -32.768 * Unit.ampere
    assert UAS_IDS[0x8E](b("FFFF")) == -0.001 * Unit.ampere
    assert UAS_IDS[0x8E](b("0000")) == 0 * Unit.ampere
    assert UAS_IDS[0x8E](b("0001")) == 0.001 * Unit.ampere
    assert UAS_IDS[0x8E](b("7FFF")) == 32.767 * Unit.ampere


def test_90():
    assert UAS_IDS[0x90](b("8000")) == -32768 * Unit.millisecond
    assert UAS_IDS[0x90](b("FFFF")) == -1 * Unit.millisecond
    assert UAS_IDS[0x90](b("0000")) == 0 * Unit.millisecond
    assert UAS_IDS[0x90](b("0001")) == 1 * Unit.millisecond
    assert UAS_IDS[0x90](b("7FFF")) == 32767 * Unit.millisecond


def test_96():
    assert float_equals(UAS_IDS[0x96](b("8000")),
                        Unit.Quantity(-3276.8, Unit.celsius))
    assert float_equals(UAS_IDS[0x96](b("FFFF")),
                        Unit.Quantity(-0.1, Unit.celsius))
    assert float_equals(UAS_IDS[0x96](b("0000")),
                        Unit.Quantity(0, Unit.celsius))
    assert float_equals(UAS_IDS[0x96](b("0001")),
                        Unit.Quantity(0.1, Unit.celsius))
    assert float_equals(UAS_IDS[0x96](b("7FFF")),
                        Unit.Quantity(3276.7, Unit.celsius))


def test_99():
    assert float_equals(UAS_IDS[0x99](b("8000")), -3276.8 * Unit.kilopascal)
    assert float_equals(UAS_IDS[0x99](b("FFFF")), -0.1 * Unit.kilopascal)
    assert float_equals(UAS_IDS[0x99](b("0000")), 0 * Unit.kilopascal)
    assert float_equals(UAS_IDS[0x99](b("0001")), 0.1 * Unit.kilopascal)
    assert float_equals(UAS_IDS[0x99](b("7FFF")), 3276.7 * Unit.kilopascal)


def test_9C():
    assert UAS_IDS[0x9C](b("8000")) == -327.68 * Unit.degree
    assert UAS_IDS[0x9C](b("FFFF")) == -0.01 * Unit.degree
    assert UAS_IDS[0x9C](b("0000")) == 0 * Unit.degree
    assert UAS_IDS[0x9C](b("0001")) == 0.01 * Unit.degree
    assert UAS_IDS[0x9C](b("7FFF")) == 327.67 * Unit.degree


def test_9D():
    assert UAS_IDS[0x9D](b("8000")) == -16384 * Unit.degree
    assert UAS_IDS[0x9D](b("FFFF")) == -0.5 * Unit.degree
    assert UAS_IDS[0x9D](b("0000")) == 0 * Unit.degree
    assert UAS_IDS[0x9D](b("0001")) == 0.5 * Unit.degree
    assert UAS_IDS[0x9D](b("7FFF")) == 16383.5 * Unit.degree


def test_A8():
    assert UAS_IDS[0xA8](b("8000")) == -32768 * Unit.grams_per_second
    assert UAS_IDS[0xA8](b("FFFF")) == -1 * Unit.grams_per_second
    assert UAS_IDS[0xA8](b("0000")) == 0 * Unit.grams_per_second
    assert UAS_IDS[0xA8](b("0001")) == 1 * Unit.grams_per_second
    assert UAS_IDS[0xA8](b("7FFF")) == 32767 * Unit.grams_per_second


def test_A9():
    assert UAS_IDS[0xA9](b("8000")) == -8192 * Unit.pascal / Unit.second
    assert UAS_IDS[0xA9](b("FFFC")) == -1 * Unit.pascal / Unit.second
    assert UAS_IDS[0xA9](b("0000")) == 0 * Unit.pascal / Unit.second
    assert UAS_IDS[0xA9](b("0004")) == 1 * Unit.pascal / Unit.second
    assert UAS_IDS[0xA9](b("7FFF")) == 8191.75 * Unit.pascal / Unit.second


def test_AD():
    assert UAS_IDS[0xAD](b("8000")) == -327.68 * Unit.milligram
    assert UAS_IDS[0xAD](b("FFFF")) == -0.01 * Unit.milligram
    assert UAS_IDS[0xAD](b("0000")) == 0 * Unit.milligram
    assert UAS_IDS[0xAD](b("0001")) == 0.01 * Unit.milligram
    assert UAS_IDS[0xAD](b("7FFF")) == 327.67 * Unit.milligram


def test_AE():
    assert UAS_IDS[0xAE](b("8000")) == -3276.8 * Unit.milligram
    assert UAS_IDS[0xAE](b("FFFF")) == -0.1 * Unit.milligram
    assert UAS_IDS[0xAE](b("0000")) == 0 * Unit.milligram
    assert UAS_IDS[0xAE](b("0001")) == 0.1 * Unit.milligram
    assert float_equals(UAS_IDS[0xAE](b("7FFF")), 3276.7 * Unit.milligram)


def test_AF():
    assert UAS_IDS[0xAF](b("8000")) == -327.68 * Unit.percent
    assert UAS_IDS[0xAF](b("FFFF")) == -0.01 * Unit.percent
    assert UAS_IDS[0xAF](b("0000")) == 0 * Unit.percent
    assert UAS_IDS[0xAF](b("0001")) == 0.01 * Unit.percent
    assert UAS_IDS[0xAF](b("7FFF")) == 327.67 * Unit.percent


def test_B0():
    assert UAS_IDS[0xB0](b("8000")) == -100.007936 * Unit.percent
    assert UAS_IDS[0xB0](b("FFFF")) == -0.003052 * Unit.percent
    assert UAS_IDS[0xB0](b("0000")) == 0 * Unit.percent
    assert UAS_IDS[0xB0](b("0001")) == 0.003052 * Unit.percent
    assert UAS_IDS[0xB0](b("7FFF")) == 100.004884 * Unit.percent


def test_B1():
    assert UAS_IDS[0xB1](b("8000")) == -65536 * Unit.millivolt / Unit.second
    assert UAS_IDS[0xB1](b("FFFF")) == -2 * Unit.millivolt / Unit.second
    assert UAS_IDS[0xB1](b("0000")) == 0 * Unit.millivolt / Unit.second
    assert UAS_IDS[0xB1](b("0001")) == 2 * Unit.millivolt / Unit.second
    assert UAS_IDS[0xB1](b("7FFF")) == 65534 * Unit.millivolt / Unit.second


def test_FC():
    assert UAS_IDS[0xFC](b("8000")) == -327.68 * Unit.kilopascal
    assert UAS_IDS[0xFC](b("FFFF")) == -0.01 * Unit.kilopascal
    assert UAS_IDS[0xFC](b("0000")) == 0 * Unit.kilopascal
    assert UAS_IDS[0xFC](b("0001")) == 0.01 * Unit.kilopascal
    assert UAS_IDS[0xFC](b("7FFF")) == 327.67 * Unit.kilopascal


def test_FD():
    assert UAS_IDS[0xFD](b("8000")) == -32.768 * Unit.kilopascal
    assert UAS_IDS[0xFD](b("FFFF")) == -0.001 * Unit.kilopascal
    assert UAS_IDS[0xFD](b("0000")) == 0 * Unit.kilopascal
    assert UAS_IDS[0xFD](b("0001")) == 0.001 * Unit.kilopascal
    assert UAS_IDS[0xFD](b("7FFF")) == 32.767 * Unit.kilopascal


def test_FE():
    assert UAS_IDS[0xFE](b("8000")) == -8192 * Unit.pascal
    assert UAS_IDS[0xFE](b("FFFC")) == -1 * Unit.pascal
    assert UAS_IDS[0xFE](b("0000")) == 0 * Unit.pascal
    assert UAS_IDS[0xFE](b("0004")) == 1 * Unit.pascal
    assert UAS_IDS[0xFE](b("7FFF")) == 8191.75 * Unit.pascal
