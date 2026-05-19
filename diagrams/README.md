# Diagrams

## Null

![Null](null.svg)

```
Diagram(
  Group(
    "null", "Null"
  )
)
```

## Boolean

![Boolean](boolean.svg)

```
Diagram(
  Group(
    Choice(0, "true", "false"), "Boolean"
  )
)
```

## Integer

![Integer](integer.svg)

```
Diagram(
  Group(
    Sequence(
      Choice(1, '+', Skip(), '-'),
      Choice(
        0,
        Group(
          Sequence(
            NonTerminal("0..9"),
            Choice(0, OneOrMore(Choice(1, "_", NonTerminal("0..9"))), Skip())
          ), "decimal"
        ),
        Group(
          Sequence(
            "0x",
            NonTerminal("0..F"),
            Choice(0, OneOrMore(Choice(1, "_", NonTerminal("0..F"))), Skip())
          ), "hexadecimal"
        ),
      )
    ), "Integer"
  )
)
```

## Float

![Float](float.svg)

```
Diagram(
  Group(
    Choice(
      0,
      Stack(
        Group(
          Sequence(
            Choice(1, '+', Skip(), '-'),
            NonTerminal("0..9"),
            Choice(0, OneOrMore(Choice(1, "_", NonTerminal("0..9"))), Skip())
          ), "integer"
        ),
        Group(
          Sequence(
            ".",
            NonTerminal("0..9"),
            Choice(0, OneOrMore(Choice(1, "_", NonTerminal("0..9"))), Skip())
          ), "fraction"
        ),
        Choice(
          0,
          Skip(),
          Group(
            Sequence(
              "e",
              Choice(1, '+', Skip(), '-'),
              NonTerminal("0..9"),
              Choice(0, OneOrMore(Choice(1, "_", NonTerminal("0..9"))), Skip())
            ), "exponent"
          )
        )
      ), "NaN", Sequence(Choice(1, '+', Skip(), '-'), "infinity")
    ), "Float"
  )
)
```

## Date

![Date](date.svg)

```
Diagram(
  Group(
    Sequence(
      NonTerminal("YYYY"), "-", NonTerminal("MM"), "-", NonTerminal("DD")
    ), "Date"
  )
)
```

## Time

![Time](time.svg)

```
Diagram(
  Group(
    Stack(
      Sequence(
        NonTerminal("hh"), ":", NonTerminal("mm"),
        Choice(0, Sequence(":", NonTerminal("ss")), Skip()),
      ),
      Choice(
        1,
        Group(
          Sequence(
            Choice(1, "Z", Sequence(
              Choice(0, "+", "-"),
              NonTerminal("hh"), ":", NonTerminal("mm"),
            )),
          ), "time zone"
        ),
        Skip(),
      ),
    ), "Time"
  )
)
```

## Timestamp

![Timestamp](timestamp.svg)

```
Diagram(
  Group(
    Stack(
      Sequence(
        Group(Sequence(
          NonTerminal("YYYY"), "-", NonTerminal("MM"), "-", NonTerminal("DD")
        ), "date"), "T"
      ),
      Group(
        Stack(
          Sequence(
            NonTerminal("hh"), ":", NonTerminal("mm"),
            Choice(0, Sequence(":", NonTerminal("ss")), Skip()),
          ),
          Choice(
            1,
            Group(
              Sequence(
                Choice(1, "Z", Sequence(
                  Choice(0, "+", "-"),
                  NonTerminal("hh"), ":", NonTerminal("mm"),
                )),
              ), "time zone"
            ),
            Skip(),
          ),
        ), "time"
      )
    ), "Timestamp"
  )
)
```

## Duration

![Duration](duration.svg)

```
Diagram(
  Group(
    Choice(
      0,

      Sequence(Group(Sequence(
        OneOrMore(NonTerminal("0..9")), "d",
        OneOrMore(NonTerminal("0..9")), "h",
        OneOrMore(NonTerminal("0..9")), "m",
        OneOrMore(NonTerminal("0..9")), "s"
      ), "days, hours, minutes, seconds")),

      Sequence(Group(Sequence(
        OneOrMore(NonTerminal("0..9")), "d",
        OneOrMore(NonTerminal("0..9")), "h",
        OneOrMore(NonTerminal("0..9")), "m",
      ), "days, hours, minutes")),

      Sequence(Group(Sequence(
        OneOrMore(NonTerminal("0..9")), "d",
        OneOrMore(NonTerminal("0..9")), "h",
      ), "days, hours")),

      Sequence(Group(Sequence(
        OneOrMore(NonTerminal("0..9")), "d",
      ), "days")),

      Sequence(Group(Sequence(
        OneOrMore(NonTerminal("0..9")), "h",
        OneOrMore(NonTerminal("0..9")), "m",
        OneOrMore(NonTerminal("0..9")), "s"
      ), "hours, minutes, seconds")),

      Sequence(Group(Sequence(
        OneOrMore(NonTerminal("0..9")), "h",
        OneOrMore(NonTerminal("0..9")), "m",
      ), "hours, minutes")),

      Sequence(Group(Sequence(
        OneOrMore(NonTerminal("0..9")), "h",
      ), "hours")),

      Sequence(Group(Sequence(
        OneOrMore(NonTerminal("0..9")), "m",
        OneOrMore(NonTerminal("0..9")), "s"
      ), "minutes, seconds")),

      Sequence(Group(Sequence(
        OneOrMore(NonTerminal("0..9")), "s",
      ), "seconds")),

    ), "Duration"
  )
)
```

## Text

![Text (inline)](text-inline.svg)

```
Diagram(Group(Sequence(
  "\"",
  ZeroOrMore(
    Choice(0,
      NonTerminal("ASCII 32..126 except \" or \\"),
      NonTerminal("U+0080..U+10FFFF"),
      Sequence("\\\"", Comment("      DOUBLE QUOTE")),
      Sequence("\\\\", Comment("         BACKSLASH")),
      Sequence("\\b", Comment("         BACKSPACE")),
      Sequence("\\f", Comment("         FORM FEED")),
      Sequence("\\n", Comment("         LINE FEED")),
      Sequence("\\r", Comment("   CARRIAGE RETURN")),
      Sequence("\\t", Comment("    HORIZONTAL TAB")),
      Sequence("\\uXXXX", Comment("       U+XXXX")),
      Sequence("\\u{XXXXXX}", Comment("U+XXXXXX")),
      Sequence("\\xXX", Comment("   ASCII char XX")),
    ),
  ),
  "\"",
), "Text (inline)"))
```

![Text (block)](text-block.svg)

```
Diagram(Group(Sequence(
  "\"\"\"",
  ZeroOrMore(
    Choice(2,
      Sequence("\"", Comment("    (except at end)")),
      Sequence("\"\"", Comment("   (except at end)")),
      NonTerminal("ASCII 32..126 except \" or \\"),
      NonTerminal("U+0080..U+10FFFF"),
      Sequence("\\\"", Comment("      DOUBLE QUOTE")),
      Sequence("\\\\", Comment("         BACKSLASH")),
      Sequence("\\b", Comment("         BACKSPACE")),
      Sequence("\\f", Comment("         FORM FEED")),
      Sequence("\\n", Comment("         LINE FEED")),
      Sequence("\\r", Comment("   CARRIAGE RETURN")),
      Sequence("\\t", Comment("    HORIZONTAL TAB")),
      Sequence("\\uXXXX", Comment("       U+XXXX")),
      Sequence("\\u{XXXXXX}", Comment("U+XXXXXX")),
      Sequence("\\xXX", Comment("   ASCII char XX")),
      NonTerminal("LINE BREAK"),
    ),
  ),
  "\"\"\"",
), "Text (block)"))
```

## Bytes

![Bytes (inline)](bytes-inline.svg)

```
Diagram(Group(Sequence(
  "'",
  ZeroOrMore(
    Choice(0,
      Sequence(NonTerminal("0..F"), NonTerminal("0..F")),
      NonTerminal("any of # $ % & - . : [ ]"),
      Sequence("0x"),
      Sequence("U+"),
      Sequence("\\x"),
      Sequence("x"),
      NonTerminal("SP or HT"),
    ),
  ),
  "'",
), "Bytes (inline)"))
```

![Bytes (block)](bytes-block.svg)

```
Diagram(Group(Sequence(
  "'''",
  ZeroOrMore(
    Choice(0,
      Sequence(NonTerminal("0..F"), NonTerminal("0..F")),
      NonTerminal("any of # $ % & - . : [ ]"),
      Sequence("0x"),
      Sequence("U+"),
      Sequence("\\x"),
      Sequence("x"),
      NonTerminal("SP or HT"),
      NonTerminal("LINE BREAK"),
    ),
  ),
  "'''",
), "Bytes (block)"))
```

## List

## Dictionary
