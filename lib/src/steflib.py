"""
steflib - Python implementation of STEF (Simple Token-Efficient Format)
https://stef.nige.tech
"""


from datetime import date, time, datetime, timedelta
from io import StringIO
from json import dumps as json_dumps
from math import isnan, isinf
from re import compile as regex, IGNORECASE
from sys import stdout


__version__ = "0.1.0"


# TODO: use full Unicode identifier pattern
identifier_pattern = regex(r"^[a-z_][a-z0-9_]*$", IGNORECASE)

decimal_integer_pattern = regex(r"^(([+-]?)([0-9]+))$")
hexadecimal_integer_pattern = regex(r"^(([+-]?)0x([0-9A-F]+))$", IGNORECASE)


class _Commented:
    """ Mixin for types that can have a comment attached.
    """
    __comment__ = None


# Python disallows extension of the bool built-in (see Guido's reasoning)
# But bool is a subclass of int, so we fall back to that.
class Boolean(_Commented, int):

    __true_instance = None
    __false_instance = None

    def __new__(cls, value):
        if value:
            if cls.__true_instance is None:
                cls.__true_instance = super().__new__(cls, 1)
            return cls.__true_instance
        else:
            if cls.__false_instance is None:
                cls.__false_instance = super().__new__(cls, 0)
            return cls.__false_instance

    def __repr__(self):
        return f"{self.__class__.__name__}({bool(self)})"

    def __str__(self):
        return "true" if self else "false"


class Integer(_Commented, int):

    def __new__(cls, value, base=None, width=0, signed=False, as_hex=False, comment=None):
        if base:
            obj = super().__new__(cls, value, base=base)
        else:
            obj = super().__new__(cls, value)
        obj._width = width
        obj._signed = bool(signed)
        obj._as_hex = as_hex
        obj.__comment__ = comment
        return obj

    def __repr__(self):
        parts = [str(self)]
        if self._width:
            parts.append(f"width={self._width!r}")
        if self._signed:
            parts.append(f"signed={self._signed!r}")
        if self._as_hex:
            parts.append(f"as_hex={self._as_hex!r}")
        if self.__comment__:
            parts.append(f"comment={self.__comment__!r}")
        return f"{self.__class__.__name__}({', '.join(parts)})"

    def __str__(self):
        return self.to_str(as_hex=self._as_hex)

    def to_str(self, as_hex=False):
        if as_hex:
            return f"{self.sign}0x{abs(self):0{self._width}X}"
        else:
            return f"{self.sign}{abs(self):0{self._width}}"

    @property
    def signed(self) -> bool:
        return self._signed

    @property
    def sign(self) -> str:
        if self == 0:
            return ""
        elif self < 0:
            return "-"
        elif self._signed:
            return "+"
        else:
            return ""


class Float(_Commented, float):

    def __new__(cls, *args, **kwargs):
        comment = kwargs.pop("comment", None)
        obj = super().__new__(cls, *args, **kwargs)
        obj.__comment__ = comment
        return obj


class String(_Commented, str):

    def __new__(cls, *args, **kwargs):
        comment = kwargs.pop("comment", None)
        obj = super().__new__(cls, *args, **kwargs)
        obj.__comment__ = comment
        return obj


class Date(_Commented, date):

    def __new__(cls, *args, **kwargs):
        comment = kwargs.pop("comment", None)
        obj = super().__new__(cls, *args, **kwargs)
        obj.__comment__ = comment
        return obj


class Time(_Commented, time):

    def __new__(cls, *args, **kwargs):
        comment = kwargs.pop("comment", None)
        obj = super().__new__(cls, *args, **kwargs)
        obj.__comment__ = comment
        return obj


class Timestamp(_Commented, datetime):

    def __new__(cls, *args, **kwargs):
        comment = kwargs.pop("comment", None)
        obj = super().__new__(cls, *args, **kwargs)
        obj.__comment__ = comment
        return obj


class Duration(_Commented, timedelta):

    def __new__(cls, *args, **kwargs):
        comment = kwargs.pop("comment", None)
        obj = super().__new__(cls, *args, **kwargs)
        obj.__comment__ = comment
        return obj


class Bytes(_Commented, bytes):

    def __new__(cls, *args, **kwargs):
        comment = kwargs.pop("comment", None)
        obj = super().__new__(cls, *args, **kwargs)
        obj.__comment__ = comment
        return obj


class List(_Commented, list):

    def __new__(cls, *args, **kwargs):
        comment = kwargs.pop("comment", None)
        obj = super().__new__(cls, *args, **kwargs)
        obj.__comment__ = comment
        return obj


class Dictionary(_Commented, dict):

    def __new__(cls, *args, **kwargs):
        comment = kwargs.pop("comment", None)
        obj = super().__new__(cls, *args, **kwargs)
        obj.__comment__ = comment
        return obj


class StefWriter:

    def __init__(self, out=stdout):
        self._out = out
        self._paragraphs = 0
        self._buffer = []
        self._stack = []

    def print(self, *values, end="\n"):
        """ Write a sequence of values.

        This is a convenience function, primarily for interactive use. After
        writing output, this resets the internal paragraph counter, which is
        generally used to automatically insert blank lines between paragraphs.
        """
        for i, value in enumerate(values):
            self.write(value)
        self._out.write(end)
        self._paragraphs = 0

    def write(self, value):
        """ Write a paragraph.
        """
        try:
            if self._paragraphs > 0:
                self._buffer.append("\n\n")
            self._write_value(value)
        except:
            raise
        else:
            self._out.write("".join(self._buffer))
            self._paragraphs += 1
        finally:
            self._buffer.clear()

    def _write_comment(self, comment, prefix=""):
        if comment:
            self._buffer.append(prefix)
            self._buffer.append("(")
            self._buffer.append(comment)
            self._buffer.append(")")

    def _write_key(self, key):
        """ Write a dictionary key.

        Keys can be either text strings or integers. If the supplied key is
        not of either of these types, the key is first converted to a string,
        and then a pattern match is carried out.
        """
        if isinstance(key, str):
            self._write_text(key)
        elif isinstance(key, (bool, Boolean)):
            # Coerce to integer so that True/False map to 1/0
            self._write_integer(int(key))
        elif isinstance(key, int):
            self._write_integer(key)
        else:
            str_key = str(key)
            if decimal_integer_pattern.match(str_key):
                self._write_integer(Integer(str_key, base=10))
            elif hexadecimal_integer_pattern.match(str_key):
                self._write_integer(Integer(str_key, base=16, as_hex=True))
            else:
                self._write_text(str_key)
        self._write_comment(getattr(key, "__comment__", None), prefix=" ")

    def _write_value(self, value):
        if value is None:
            self._write_null()
        elif isinstance(value, (bool, Boolean)):
            # IMPORTANT: always test for Boolean before int
            # as the former is a subclass of the latter.
            self._write_boolean(value)
        elif isinstance(value, int):
            self._write_integer(value)
        elif isinstance(value, float):
            self._write_float(value)
        elif isinstance(value, datetime):
            # IMPORTANT: always test for datetime before date
            # as the former is a subclass of the latter.
            self._write_timestamp(value)
        elif isinstance(value, date):
            self._write_date(value)
        elif isinstance(value, time):
            self._write_time(value)
        elif isinstance(value, timedelta):
            self._write_duration(value)
        elif isinstance(value, str):
            self._write_text(value)
        elif isinstance(value, (bytes, bytearray)):
            self._write_bytes(value)
        elif isinstance(value, (list, tuple, set, frozenset)):
            self._write_list(value)
        elif isinstance(value, dict):
            self._write_dictionary(value)
        else:
            raise ValueError(value)
        self._write_comment(getattr(value, "__comment__", None), prefix=" ")

    def _write_null(self):
        self._buffer.append("null")

    def _write_boolean(self, value):
        self._buffer.append("true" if value else "false")

    def _write_integer(self, value):
        self._buffer.append(str(value))

    def _write_float(self, value):
        if isnan(value):
            self._buffer.append("NaN")
        elif isinf(value):
            if value > 0:
                self._buffer.append("infinity")
            else:
                self._buffer.append("-infinity")
        else:
            self._buffer.append(str(value))

    def _write_date(self, value):
        self._buffer.append(value.isoformat())

    def _write_time(self, value):
        self._buffer.append(value.isoformat())

    def _write_timestamp(self, value):
        self._buffer.append(value.isoformat())

    def _write_duration(self, value):
        assert isinstance(value, timedelta)
        # Milliseconds are ignored, as not supported in the spec
        minutes, seconds = divmod(value.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        parts = [(value.days, "d"), (hours, "h"), (minutes, "m"), (seconds, "s")]
        while parts and parts[0][0] == 0:
            parts = parts[1:]
        while parts and parts[-1][0] == 0:
            parts = parts[:-1]
        if not parts:
            parts = [(0, "s")]
        for i, part in enumerate(parts[1:], start=1):
            if part[0] < 10:
                parts[i] = (f"0{part[0]}", part[1])
        self._buffer.extend(f"{value}{unit}" for value, unit in parts)

    def _write_text(self, value):
        value = str(value)
        if identifier_pattern.match(value) and not is_reserved(value):
            self._buffer.append(value)
        else:
            self._buffer.append(json_dumps(value))

    def _write_bytes(self, value):
        self._buffer.append("'")
        self._buffer.extend(f"{b:02X}" for b in bytes(value))
        self._buffer.append("'")

    def _write_list(self, value):
        value = list(value)
        depth = len(self._stack)
        self._stack.append("[")
        if depth == 0 and len(value) >= 1:
            # block list
            for i, value in enumerate(value):
                if i > 0:
                    self._buffer.append("\n")
                self._buffer.append("- ")
                self._write_value(value)
        elif depth == 1 and len(value) >= 2:
            # inline list
            for i, value in enumerate(value):
                if i > 0:
                    self._buffer.append(", ")
                self._write_value(value)
        else:
            # bracketed list
            self._buffer.append("[")
            for i, value in enumerate(value):
                if i > 0:
                    self._buffer.append(", ")
                self._write_value(value)
            self._buffer.append("]")
        self._stack.pop()

    def _write_dictionary(self, value):
        value = dict(value)
        depth = len(self._stack)
        self._stack.append("{")
        if depth == 0 and len(value) >= 1:
            # block dictionary
            for i, (key, value) in enumerate(value.items()):
                if i > 0:
                    self._buffer.append("\n")
                self._write_key(key)
                self._buffer.append(": ")
                self._write_value(value)
        elif depth == 1 and len(value) >= 2:
            # inline dictionary
            for i, (key, value) in enumerate(value.items()):
                if i > 0:
                    self._buffer.append(", ")
                self._write_key(key)
                self._buffer.append(": ")
                self._write_value(value)
        else:
            # bracketed dictionary
            self._buffer.append("{")
            for i, (key, value) in enumerate(value.items()):
                if i > 0:
                    self._buffer.append(", ")
                self._write_key(key)
                self._buffer.append(": ")
                self._write_value(value)
            self._buffer.append("}")
        self._stack.pop()


def is_reserved(word):
    return str(word).lower() in {"null", "true", "false", "infinity", "nan"}


def stef(value):
    """ Convert a value to a STEF string.
    """
    out = StringIO()
    writer = StefWriter(out)
    writer.write(value)
    return out.getvalue()


def dumps(value):
    """ Convert a value to a STEF string.

    This function is a compatibility wrapper for Python to implement a
    familiar interface.
    """
    return stef(value)
