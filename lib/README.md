# steflib

Python implementation of [STEF](https://stef.nige.tech): the Simple 
Token-Efficient Format.

For more details on the format and a full specification, visit 
[stef.nige.tech](https://stef.nige.tech).


## Installation

```shell
pip install steflib
```


## Usage

```python-repl
>>> from steflib import stef
>>> from datetime import date
>>> print(stef({"name": "David Bowie", "born": date(1947, 1, 8), "studio_albums": 26}))
name: "David Bowie"
born: 1947-01-08
studio_albums: 26
```

For streaming output, use the `StefWriter` directly:

```python-repl
>>> from steflib import StefWriter
>>> from datetime import date
>>> writer = StefWriter()
>>> writer.print({"name": "David Bowie", "born": date(1947, 1, 8)})
>>> writer.print({"name": "Sting", "born": date(1951, 10, 2)})
```

Plain Python types are mapped to their STEF equivalents automatically. For
additional control, typed wrappers are provided - for example, to emit an
integer in hexadecimal, or to attach a comment to any value:

```python-repl
>>> from steflib import stef, Integer, Float
>>> print(stef(Integer(255, as_hex=True)))
0xFF
>>> print(stef(Float(3.14, comment="approx")))
3.14 (approx)
```
