# Diagrams

## Stream

![Stream](stream.svg)

```
Diagram(Group(Sequence(
  ZeroOrMore(Sequence(
    NonTerminal("Paragraph"),
    ZeroOrMore(Sequence(NonTerminal("BLANK LINE"), NonTerminal("Paragraph"))),
  )) 
), "Stream"))
```

## Paragraph

![Paragraph](paragraph.svg)

```
Diagram(Group(Sequence(
  Choice(0,
    NonTerminal("Value"),
    NonTerminal("List (block)"),
    NonTerminal("Dictionary (block)"),
    NonTerminal("Keyed List (block)"),
  ),
  NonTerminal("LINE BREAK"),
), "Paragraph"))
```

## Value

![Value](value.svg)

```
Diagram(Group(Sequence(
  Choice(0,
    NonTerminal("Null"),
    NonTerminal("Boolean"),
    NonTerminal("Integer"),
    NonTerminal("Float"),
    NonTerminal("Date"),
    NonTerminal("Time"),
    NonTerminal("Timestamp"),
    NonTerminal("Duration"),
    NonTerminal("Text"),
    NonTerminal("Bytes"),
    NonTerminal("List (bracketed)"),
    NonTerminal("Dictionary (bracketed)"),
  ),
), "Value"))
```

## Comment

![Comment](comment.svg)

```
Diagram(Group(Sequence(
  "(",
  OneOrMore(Choice(1, 
    NonTerminal("Comment"),
    NonTerminal("COMMENT TEXT"),
  )),
  ")",
), "Comment"))
```

## Null

![Null](null.svg)

```
Diagram(Group(Sequence(
  "null"
), "Null"))
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
Diagram(Group(Choice(2,
  "NaN",
  Sequence(Choice(1, '+', Skip(), '-'), "infinity"),
  Stack(
    Group(Sequence(
      Choice(1, '+', Skip(), '-'), NonTerminal("0..9"),
      Choice(0, OneOrMore(Choice(1, "_", NonTerminal("0..9"))), Skip())
    ), "integer"),
    OptionalSequence(
      Group(Sequence(
        ".", NonTerminal("0..9"),
        Choice(0, OneOrMore(Choice(1, "_", NonTerminal("0..9"))), Skip())
      ), "fraction"),
      Group(Sequence(
        "e", Choice(1, '+', Skip(), '-'), NonTerminal("0..9"),
        Choice(0, OneOrMore(Choice(1, "_", NonTerminal("0..9"))), Skip())
      ), "exponent")
    ),
  ),
), "Float"))
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
Diagram(Group(Stack(
  Sequence(NonTerminal("hh"), ":", NonTerminal("mm")),
  Choice(1,
    Group(Sequence(
      ":",
      NonTerminal("ss"),
      Optional(Sequence(
        ".",
        OneOrMore(NonTerminal("0..9")),
      )),
    ), "seconds"),
  Skip()),
  Choice(1,
    Group(Sequence(
      Choice(1, "Z", Sequence(
        Choice(0, "+", "-"),
        NonTerminal("hh"), ":", NonTerminal("mm"),
      )),
    ), "time zone"),
  Skip()),
), "Time"))
```

## Timestamp

![Timestamp](timestamp.svg)

```
Diagram(Group(Sequence(
  NonTerminal("Date"), "T", NonTerminal("Time")
), "Timestamp"))
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
Diagram(Group(Stack(
  Choice(1,
    Sequence(
      NonTerminal("IDENTIFIER"),
      Comment("see Unicode TR #31"),
    ),
    Sequence(
      "\"",
      ZeroOrMore(
        Choice(1,
          NonTerminal("any of  \\\" \\\\ \\b \\f \\n \\r \\t"),
          NonTerminal("ASCII 32..126  except \" or \\"),
          NonTerminal("  Unicode U+0080..U+10FFFF  "),
          Sequence("\\uXXXX", Comment("       U+XXXX")),
          Sequence("\\u{XXXXXX}", Comment("U+XXXXXX")),
          Sequence("\\xXX", Comment("   ASCII char XX")),
        ),
      ),
      "\"",
    )
  )
), "Text (inline)"))
```

![Text (block)](text-block.svg)

```
Diagram(Group(Sequence(
  "\"\"\"",
  ZeroOrMore(
    Choice(3,
      Sequence("\"", Comment("    (except at end)")),
      Sequence("\"\"", Comment("   (except at end)")),
      NonTerminal("any of \\\" \\\\ \\b \\f \\n \\r \\t"),
      NonTerminal("ASCII 32..126 except \" or \\"),
      NonTerminal("  Unicode U+0080..U+10FFFF "),
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
      NonTerminal("any of # $ % & - . : [ ] 0x U+ \\x x"),
      NonTerminal("SPACE (U+0020) or TAB (U+0009)"),
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
      NonTerminal("any of # $ % & - . : [ ] 0x U+ \\x x"),
      NonTerminal("SPACE (U+0020) or TAB (U+0009)"),
      NonTerminal("LINE BREAK"),
    ),
  ),
  "'''",
), "Bytes (block)"))
```

## List

![List (bracketed)](list-bracketed.svg)

```
Diagram(Group(Sequence(
  "[",
  ZeroOrMore(Sequence(NonTerminal("Value")), ","),
  Choice(0, Skip(), ","),
  "]",
), "List (bracketed)"))
```

![List (inline)](list-inline.svg)

```
Diagram(Group(Sequence(
  NonTerminal("Value"), ",",
  OneOrMore(NonTerminal("Value"), ","),
), "List (inline)"))
```

![List (block)](list-block.svg)

```
Diagram(Group(OneOrMore(
  Sequence(
    "-", NonTerminal("SPACE"),
    Choice(0,
      NonTerminal("Value"),
      NonTerminal("List (inline)"),
      NonTerminal("Dictionary (inline)"),
    )
  ), NonTerminal("LINE BREAK")
), "List (block)"))
```

## Dictionary

![Dictionary (bracketed)](dictionary-bracketed.svg)

```
Diagram(Group(Sequence(
  "{",
  ZeroOrMore(Sequence(Group(Choice(0, NonTerminal("Text"), NonTerminal("Integer")), "key"), ":", NonTerminal("Value")), ","),
  Choice(0, Skip(), ","),
  "}",
), "Dictionary (bracketed)"))
```

![Dictionary (inline)](dictionary-inline.svg)

```
Diagram(Group(Sequence(
  OneOrMore(
    Sequence(Group(Choice(0, NonTerminal("Text"), NonTerminal("Integer")), "key"), ":", NonTerminal("Value")),
    ","
  ) ,
), "Dictionary (inline)"))
```

![Dictionary (block)](dictionary-block.svg)

```
Diagram(Group(OneOrMore(
  Sequence(
    Group(Choice(0, NonTerminal("Text"), NonTerminal("Integer")), "key"), ":", 
    Choice(0,
      NonTerminal("Value"),
      NonTerminal("List (inline)"),
      NonTerminal("Dictionary (inline)"),
    )
  ), NonTerminal("LINE BREAK")
), "Dictionary (block)"))
```

## Hybrid collections

![Keyed List (block)](keyed-list-block.svg)

```
Diagram(Group(Stack(
  Sequence(
    Group(Choice(0, NonTerminal("Text"), NonTerminal("Integer")), "key"), ":", 
    NonTerminal("LINE BREAK"),
    NonTerminal("List (block)"),
  ),
), "Keyed List (block)"))
```
