# STEF Specification

This document provides a specification for *STEF*, the **Simple Token-Efficient
Format**. This is a text-based, human-readable format for data interchange.


## Grammar

The format draws from the Unicode character set. Encoding must use UTF-8
without byte order marks.

Literal strings are shown here in their canonical casing, but the format is
case-insensitive, so any casing may apply.

```
HT              := U+0009
LF              := U+000A
CR              := U+000D
SP              := U+0020
ASCII           := U+0020..U+007E
IDENTIFIER      := <defined by https://www.unicode.org/reports/tr31/>
```


In the general case, white space and comments encode presentational detail
only. Comments are enclosed in parentheses and may be nested; a comment closes
only when the outermost parenthesis is matched. Comments may contain any
characters and may span multiple lines.

Emitters may insert comments before, after or between any tokens, as desired by
the implementation. Parsers may choose to either ignore comments, or to
associate them with adjacent values, e.g. `pi: 3.14 (approx)`.

```
space           := SP | HT
line-break      := CR LF | CR | LF
inline-char     := ASCII | U+0080..U+10FFFF
char            := inline-char | CR | LF | HT
comment-char    := char EXCEPT "(" EXCEPT ")"
comment-text    := comment-char*
comment         := "(" comment-text (comment comment-text)* ")"
inline-space    := space | comment
white-space     := inline-space | line-break
~~              := white-space*   # optional whitespace/comments, including newlines
--              := inline-space*  # optional whitespace/comments, excluding newlines
```


All content is considered part of a stream. A stream is a sequence of zero or
more paragraphs delimited by blank lines. Each paragraph represents exactly
one top-level value. Paragraphs in the same stream are not required to share
a common type or structure. Comments may be inserted between paragraphs. A
standalone comment between paragraphs does not constitute a new paragraph.

```
stream          := paragraph-seq?
paragraph-seq   := paragraph (blank-line paragraph)*
paragraph       := (value | block-list | block-dict) -- line-break
blank-line      := ~~ line-break
value           := null | boolean | numeric | temporal | string | collection
```


Several terms are considered reserved words and must not be used as keys or
values without quoting. Parsers should identify these as single tokens. All
case variants are reserved.

```
reserved        := null | true | false | infinity | NaN
```


Null is provided as a representation of missing or unknown values. The precise
semantic meaning of the `null` placeholder is not dictated by this grammar, and
is instead left as an implementation design decision. Emitters may therefore
include or exclude `null` as desired. Parsers must gracefully accept `null` in
any valid position; implementations may choose to keep or discard these.

```
null            := "null"/i
```


Boolean values are represented by the keywords `true` and `false`. These are
the only forms, but are case-insensitive. The canonical representations are
lower case.

```
boolean         := true | false
true            := "true"/i
false           := "false"/i
```


Numeric values include integers and floating point numbers. These begin with
either a digit or a sign character. While no size limit is defined here, it
is typically assumed that 64-bit signed integers and 64-bit floating point
numbers are represented. Provision is also made for out-of-range values with
`infinity` and `NaN`.

Underscores are permitted in sequences of decimal and hexadecimal digits as
separators. The grammar makes no restriction of where these may be placed, or
how many, aside from the requirement that the first character is always a
digit. Emitters may choose any valid underscore-separation strategy for output.
Parsers must ignore underscores in digit sequences.

Emitters should generally prefer to output the simplest form of a number
where multiple options are available. Therefore, `1.0` is preferred to `+1.0`
or `1e0`. However, implementations may choose to output any valid form.
Parsers should gracefully accept any valid form.

```
numeric         := number | not-a-number
number          := sign? (integer | float | infinity)

sign            := "+" | "-"
digit           := "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
digit-seq       := digit (digit | "_")*
hex-upper       := "A" | "B" | "C" | "D" | "E" | "F"
hex-lower       := "a" | "b" | "c" | "d" | "e" | "f"
hex-digit       := digit | hex-upper | hex-lower
hex-digit-seq   := hex-digit (hex-digit | "_")*

integer         := dec-integer | hex-integer
dec-integer     := digit-seq
hex-integer     := "0x" hex-digit-seq
float           := digit-seq (fraction | exponent | fraction exponent)
fraction        := "." digit-seq
exponent        := "e"/i sign? digit-seq

not-a-number    := "NaN"/i
infinity        := "infinity"/i
```


Temporal values include dates, times, timestamps and durations. ISO 8601
formatting is used to represent date, time, and timestamp values according to
the Gregorian calendar and the 24-hour clock.

Duration values chain together a count of days, hours, minutes and seconds.
Such counts must be listed in order and must be contiguous. Parsers should
reject duration values with non-contiguous components. Emitters may output
zero durations using any one or more components with a zero value, and in a
valid sequence.

```
temporal        := date | time | timestamp | duration

date            := digit*4 "-" digit*2 "-" digit*2

time            := time-naive | time-aware
time-aware      := time-naive time-zone
time-naive      := hh-mm | hh-mm-ss
time-zone       := "Z"/i | sign hh-mm
hh-mm-ss        := hh-mm ":" digit*2 ("." digit+)?
hh-mm           := digit*2 ":" digit*2

timestamp       := date "T"/i time

duration        := days | hours | minutes | seconds
days            := digit* "d"/i hours?
hours           := digit* "h"/i minutes?
minutes         := digit* "m"/i seconds?
seconds         := digit* "s"/i
```


String values can hold either text or byte sequences. Both types of string
allow triple-quoted forms which may span multiple lines. Text strings may
also be unquoted if the content exactly matches the identifier pattern
defined by Unicode and the content does not match a reserved word. Reserved
words include `null`, `true`, `false`, `infinity`, and `NaN`, all with any
casing.

Text strings may contain escaped characters prefixed by `\`. Though it is
technically permitted, emitters should not escape forward slashes within
strings for reasons of clarity. Parsers should however gracefully accept all
escaped characters.

Byte strings contain an even number of hexadecimal characters, each pair
representing a single byte value. Such characters are case-insensitive. Byte
strings may also contain additional decorative characters, such as white
space and hash symbols. Parsers should ignore any non-hexadecimal characters.

Parsers should take particular care to correctly support `0x` within byte
strings. The first character of the sequence is also a valid hexadecimal
character, but in the sequence `0x` the digit is merely decorative. Parsing
hexadecimal characters in distinct pairs is strongly advised.

```
string          := IDENTIFIER | text | bytes | block-text | block-bytes

escape          := '\"' | "\\" | "\/" | "\b" | "\f" | "\n" | "\r" | "\t" | u-escape | x-escape
u-escape        := u4-escape | u6-escape
u4-escape       := "\u" hex-digit*4
u6-escape       := "\u" "{" hex-digit+ "}"
x-escape        := "\x" hex-digit*2

text-char       := inline-char EXCEPT "\" EXCEPT '"'
text-atom       := text-char | escape
text            := '"' text-atom* '"'

block-text-atom := text-atom | line-break
block-text-quot := '"' | '""'
block-text-seq  := block-text-atom* (block-text-quot block-text-atom)?
block-text      := '"""' block-text-seq* '"""'

hex-pair        := hex-digit*2
hex-symbol      := "#" | "$" | "%" | "&" | "-" | "." | ":" | "[" | "]" | "0x" | "U+" | "\x" | "x"
hex-deco        := (hex-symbol | space)*
bytes           := "'" hex-deco (hex-pair hex-deco)* "'"

block-hex-deco  := (hex-symbol | space | line-break)*
block-bytes-seq := block-hex-deco (hex-pair block-hex-deco)*
block-bytes     := "'''" block-bytes-seq "'''"
```


Two types of collection exist: lists and dictionaries. Each has a standard
representation, plus two extended presentational representations.

Collections are considered to nest when one is placed inside another. Depth
begins at zero at the stream root, and increases by one for every collection
descended into. Nesting depth and element count provide conditions that permit
certain presentational forms. Block forms are only permitted at depth zero when
at least one element is present. Inline forms are only permitted at depth one
when at least two elements are present. All other cases, including empty
collections, require the standard bracketed form. The documented grammar
encodes these depth and content constraints fully.

Emitters should prefer extended presentational representations whenever
conditions are met, to maximise legibility of output. Standard forms remain
valid alternatives as fallbacks however, and parsers should gracefully accept
content in any form.

```
collection      := list | dict

comma           := ","

list-seq        := value ~~ (comma ~~ value ~~)* comma?
list            := "[" list-seq? ~~ "]"

key             := IDENTIFIER | text | (sign? integer)
key-value       := key ~~ ":" ~~ value
dict-seq        := key-value ~~ (comma ~~ key-value ~~)* comma?
dict            := "{" dict-seq? ~~ "}"

inline-list     := value -- comma -- value -- (comma -- value --)*
inline-dict     := key-value -- comma -- key-value -- (comma -- key-value --)*

inline-value    := value | inline-list | inline-dict
list-item       := "-" space+ inline-value
dict-item       := key -- ":" -- inline-value
block-list      := list-item -- (line-break -- list-item --)*
block-dict      := dict-item -- (line-break -- dict-item --)*
```

---

## References
- [Unicode](https://unicode.org)
- [ISO 8601 - Date and time format](https://www.iso.org/iso-8601-date-and-time-format.html)
