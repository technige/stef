from steflib import dumps, Integer


def test_dumps_integer_zero():
    assert dumps(0) == "0"


def test_dumps_integer_plus_one():
    assert dumps(1) == "1"


def test_dumps_integer_minus_one():
    assert dumps(-1) == "-1"


def test_dumps_positive_hex_integer():
    assert dumps(Integer(33, base=16, width=4)) == "0x0021"


def test_dumps_negative_hex_integer():
    assert dumps(Integer(-33, base=16, width=4)) == "-0x0021"
