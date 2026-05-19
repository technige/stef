"""
steflib - Python implementation of STEF (Simple Token-Efficient Format)
https://stef.nige.tech
"""


from datetime import date, time, datetime
from io import StringIO
from json import dumps as json_dumps
from re import compile as regex
from sys import stdout


# TODO: use full Unicode identifier pattern
identifier = regex(r"^[a-z_][a-z0-9_]*$")


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

    def __new__(cls, value, base=10, width=0, signed=False, comment=None):
        if isinstance(value, str):
            value = int(value, base)
        obj = super().__new__(cls, value)
        obj._base = 16 if base == 16 else 10
        obj._width = width
        obj._signed = bool(signed)
        obj.__comment__ = comment
        return obj

    def __repr__(self):
        return f"{self.__class__.__name__}({int(self)})"

    def __str__(self):
        if self._base == 16:
            return f"{self.sign}0x{abs(self):0{self._width}X}"
        else:
            return f"{self.sign}{abs(self):0{self._width}}"

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

    @property
    def signed(self) -> bool:
        return self._signed


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
        if identifier.match(key):
            self._buffer.append(key)
        else:
            self._write_text(key)
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

    def _write_float(self, data):
        self._buffer.append(str(data))

    def _write_text(self, data):
        self._buffer.append(json_dumps(str(data)))

    def _write_bytes(self, data):
        self._buffer.append("'")
        self._buffer.extend(f"{b:02X}" for b in bytes(data))
        self._buffer.append("'")

    def _write_list(self, data):
        data = list(data)
        depth = len(self._stack)
        self._stack.append("[")
        if depth == 0:
            # block list
            for i, value in enumerate(data):
                if i > 0:
                    self._buffer.append("\n")
                self._buffer.append("- ")
                self._write_value(value)
        elif depth == 1 and len(data) >= 2:
            # inline list
            for i, value in enumerate(data):
                if i > 0:
                    self._buffer.append(", ")
                self._write_value(value)
        else:
            # bracketed list
            self._buffer.append("[")
            for i, value in enumerate(data):
                if i > 0:
                    self._buffer.append(", ")
                self._write_value(value)
            self._buffer.append("]")
        self._stack.pop()

    def _write_dictionary(self, data):
        data = dict(data)
        depth = len(self._stack)
        self._stack.append("{")
        if depth == 0:
            # block dictionary
            for i, (key, value) in enumerate(data.items()):
                if i > 0:
                    self._buffer.append("\n")
                self._write_key(key)
                self._buffer.append(": ")
                self._write_value(value)
        elif depth == 1 and len(data) >= 2:
            # inline dictionary
            for i, (key, value) in enumerate(data.items()):
                if i > 0:
                    self._buffer.append(", ")
                self._write_key(key)
                self._buffer.append(": ")
                self._write_value(value)
        else:
            # bracketed dictionary
            self._buffer.append("{")
            for i, (key, value) in enumerate(data.items()):
                if i > 0:
                    self._buffer.append(", ")
                self._write_key(key)
                self._buffer.append(": ")
                self._write_value(value)
            self._buffer.append("}")
        self._stack.pop()


def dumps(value):
    out = StringIO()
    writer = StefWriter(out)
    writer.write(value)
    return out.getvalue()
