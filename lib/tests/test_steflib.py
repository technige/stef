from datetime import date, datetime, timedelta

from steflib import stef, Boolean, Integer, Float, Text, List, Dictionary


integer_tests = [
    (0, "0"),
    (1, "1"),
    (-1, "-1"),
    (Integer("0x21", base=16), "33"),
    (Integer("0x21", base=16, as_hex=True), "0x21"),
    (Integer(33, width=4, as_hex=True), "0x0021"),
    (Integer(-33, width=4, as_hex=True), "-0x0021"),
    (Integer(33, signed=True), "+33"),
    (Integer(0, signed=True), "0"),
]

float_tests = [
    (0.0, "0.0"),
    (3.14, "3.14"),
    (-3.14, "-3.14"),
    (1.0, "1.0"),
    (1e0, "1.0"),
    (float("NaN"), "NaN"),
    (float("inf"), "infinity"),
    (float("+inf"), "infinity"),
    (float("-inf"), "-infinity"),
    (Float(3.14), "3.14"),
    (Float(3.14, comment="approx"), "3.14 (approx)"),
]

text_tests = [
    ("none", 'none'),
    ("None", 'None'),
    ("null", '"null"'),
    ("Null", '"Null"'),
    ("true", '"true"'),
    ("True", '"True"'),
    ("false", '"false"'),
    ("False", '"False"'),
    ("infinity", '"infinity"'),
    ("Infinity", '"Infinity"'),
    ("NaN", '"NaN"'),
    ("nan", '"nan"'),
    ("", '""'),
    ("hello", 'hello'),
    ("hello, world", '"hello, world"'),
    (Text(""), '""'),
    (Text("hello"), 'hello'),
    (Text("hello, world"), '"hello, world"'),
]

timestamp_tests = [
    (datetime(2012, 3, 4, 5, 6, 7), '2012-03-04T05:06:07'),
]

duration_tests = [
    (timedelta(days=3), "3d"),
    (timedelta(days=3, hours=7), "3d07h"),
    (timedelta(days=3, hours=7, minutes=12), "3d07h12m"),
    (timedelta(days=3, hours=7, minutes=12, seconds=59), "3d07h12m59s"),
    (timedelta(hours=7), "7h"),
    (timedelta(hours=7, minutes=12), "7h12m"),
    (timedelta(hours=7, minutes=12, seconds=59), "7h12m59s"),
    (timedelta(minutes=12), "12m"),
    (timedelta(minutes=12, seconds=59), "12m59s"),
    (timedelta(seconds=59), "59s"),
    (timedelta(), "0s"),
    (timedelta(seconds=86400), "1d"),
]


list_tests = [
    ([], "[]"),
    ([1], "- 1"),
    ([1, 2], "- 1\n- 2"),
    ([{"one": 1}, {"two": 2}], "- one: 1\n- two: 2"),
    (List(), "[]"),
    (List(comment="empty"), "[] (empty)"),
    (List([1], comment="singleton"), "- 1\n(singleton)"),
    (List([1, 2], comment="block"), "- 1\n- 2\n(block)"),
]


dictionary_tests = [
    ({}, "{}"),
    ({"one": 1}, "one: 1"),
    ({"first": {"one": 1}, "second": {"two": 2}}, "first: one: 1\nsecond: two: 2"),
    ({"one": 1, "two": 2}, "one: 1\ntwo: 2"),
    ({1: "one", 2: "two"}, "1: one\n2: two"),
    ({-1: "minus one", -2: "minus two"}, "-1: \"minus one\"\n-2: \"minus two\""),
    ({1: "one", 0: "zero", -1: "minus one"}, "1: one\n0: zero\n-1: \"minus one\""),
    ({True: "true", False: "false"}, "1: \"true\"\n0: \"false\""),
    ({Boolean(True): "true", Boolean(False): "false"}, "1: \"true\"\n0: \"false\""),
    ({"1": "one", "2": "two"}, '"1": one\n"2": two'),
    ({0x01: "one", 0x02: "two"}, '1: one\n2: two'),
    ({"0x01": "one", "0x02": "two"}, '"0x01": one\n"0x02": two'),
    ({Integer(1, width=2, as_hex=True): "one", Integer(2, width=2, as_hex=True): "two"}, '0x01: one\n0x02: two'),
    ({date(2012, 3, 4): "date"}, "\"2012-03-04\": date"),
    ({"colours": ["red", "green", "blue"]}, "colours:\n- red\n- green\n- blue"),
    ({"empty": []}, "empty: []"),
    ({"odds": [1, 3, 5], "evens": [2, 4, 6]}, "odds: 1, 3, 5\nevens: 2, 4, 6"),
    ({"odds": [{"one": 1}, {"three": 3}], "evens": [{"two": 2}, {"four": 4}]}, "odds: {one: 1}, {three: 3}\nevens: {two: 2}, {four: 4}"),
    (Dictionary(), "{}"),
    (Dictionary(comment="empty"), "{} (empty)"),
    (Dictionary({"one": 1}, comment="singleton"), "one: 1\n(singleton)"),
    (Dictionary({"one": 1, "two": 2}, comment="block"), "one: 1\ntwo: 2\n(block)"),
    (Dictionary({"colours": ["red", "green", "blue"]}, comment="primary"), "colours:\n- red\n- green\n- blue\n(primary)"),
]


def test_integer_dumps(subtests):
    for value, output in integer_tests:
        with subtests.test(f"{value!r} -> {output!r}"):
            assert stef(value) == output


def test_float_dumps(subtests):
    for value, output in float_tests:
        with subtests.test(f"{value!r} -> {output!r}"):
            assert stef(value) == output


def test_text_dumps(subtests):
    for value, output in text_tests:
        with subtests.test(f"{value!r} -> {output!r}"):
            assert stef(value) == output


def test_timestamp_dumps(subtests):
    for value, output in timestamp_tests:
        with subtests.test(f"{value!r} -> {output!r}"):
            assert stef(value) == output


def test_duration_dumps(subtests):
    for value, output in duration_tests:
        with subtests.test(f"{value!r} -> {output!r}"):
            assert stef(value) == output


def test_list_dumps(subtests):
    for value, output in list_tests:
        with subtests.test(f"{value!r} -> {output!r}"):
            assert stef(value) == output


def test_dictionary_dumps(subtests):
    for value, output in dictionary_tests:
        with subtests.test(f"{value!r} -> {output!r}"):
            assert stef(value) == output
