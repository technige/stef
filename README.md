# STEF

[This repository](https://github.com/technige/stef) hosts the specification
for *STEF*, the **Simple Token-Efficient Format**.

STEF is a data interchange format with a comprehensive data model and adaptable
presentation. The format was designed to be familiar, compatible, and to
improve communication between humans and machines. The design focuses on
the efficient use of tokens to maximise content over punctuation.

```
(Apollo program -
 crewed lunar landings)

program: Apollo
agency: NASA
first_landing: 1969-07-20T20:17:40Z
active: {start: 1961-05-25, end: 1972-12-19}
total_samples_kg: 381.69 (approx)
missions_successful: 6

- mission: Apollo11, commander: "Neil Armstrong", landed: 1969-07-20, samples_kg: 21.55
- mission: Apollo12, commander: "Pete Conrad",    landed: 1969-11-19, samples_kg: 34.35
- mission: Apollo14, commander: "Alan Shepard",   landed: 1971-02-05, samples_kg: 42.80
- mission: Apollo15, commander: "David Scott",    landed: 1971-07-30, samples_kg: 76.82
- mission: Apollo16, commander: "John Young",     landed: 1972-04-21, samples_kg: 95.71
- mission: Apollo17, commander: "Gene Cernan",    landed: 1972-12-11, samples_kg: 110.52
```

Read the full [specification](STEF.md).


## Type system

| Type       | Quick examples                       | Description                                                                             |
|------------|--------------------------------------|-----------------------------------------------------------------------------------------|
| null       | `null`                               | absence of value or unknown value                                                       |
| boolean    | `true`, `false`                      | logical truth value, 1 or 0, yes or no                                                  |
| integer    | `123`, `-42`, `0xFFC033`, `0`        | signed whole number                                                                     |
| float      | `3.14`, `1e06`, `NaN`, `+infinity`   | [floating point](https://en.wikipedia.org/wiki/Floating-point_arithmetic) (real) number |
| date       | `2016-01-10`                         | calendar date (ISO 8601)                                                                |
| time       | `12:34:56.789`, `10:08+02:00`        | clock time (ISO 8601), optionally with time zone                                        |    
| timestamp  | `1999-12-31T23:59:59.999999Z`        | date and time, optionally with time zone                                                |          
| text       | `"hello, world"`, `token`, `"\r\n"`  | Unicode text string                                                                     |
| bytes      | `'57EF CAFE'`, `'#ffc033'`           | hexadecimal byte string                                                                 |
| list       | `[1, true, 3.1415]`                  | ordered sequence of values                                                              |
| dictionary | `{Alice: {age: 33}, Bob: {age: 44}}` | unordered set of key-value pairs                                                        |


## More examples

```
(
STEF Examples

This stream contains multiple paragraphs, each separated by a blank line.
Each paragraph demonstrates a different aspect of the format.
)


(1. Scalar primitives in a block dict)
null_value: null
boolean_true: true
boolean_false: false
integer: 42
negative: -17
large: 9007199254740992
float: 3.14159
scientific: 6.022e23
pos_infinity: +infinity
neg_infinity: -infinity
not_a_number: NaN
bare_string: hello
quoted_string: "hello, world"
escaped_string: "first line\nsecond line"

(2. Temporal values - dates, times, and timestamps)
calendar_date: 2026-05-18
hour_minute: 09:00
with_seconds: 09:30:15
with_subseconds: 09:30:15.750
timestamp_utc: 2026-05-18T09:30:15Z
timestamp_ahead: 2026-05-18T11:30:15+02:00
timestamp_behind: 2026-05-18T04:30:15-05:00

(3. String forms - from bare identifiers through to block text and bytes)
unquoted: hello
quoted: "hello, world"
escaped: "quoted: \"yes\"\nnewline above"
unicode_char: "\u{1F4E6} package shipped"
block_text: """
  This is a block text string.
  It preserves interior whitespace and newlines,
  making it ideal for prose, code snippets, or SQL.
  """
raw_hex: '48 65 6C 6C 6F'
c_prefix: '0x48 0x65 0x6C 0x6C 0x6F'
mac_notation: 'AA:BB:CC:DD:EE:FF'
hyphen_notation: 'DE-AD-BE-EF-00-FF'
block_bytes: '''
  504B 0304 1400 0000
  0800 2B76 5A54 7C40
  '''

(4. Block list of plain values)
- alpha
- beta
- gamma
- delta

(5. Block list with inline list items - brackets are dropped inside list items)
- 1, 0, 0
- 0, 1, 0
- 0, 0, 1

(6. Block list with inline dict items - braces are dropped inside list items)
- name: Alice, role: admin, active: true, joined: 2023-01-15
- name: Bob, role: editor, active: true, joined: 2024-06-01
- name: Carol, role: viewer, active: false, joined: 2022-11-30

(7. HTTP access log - a block list of inline dicts with mixed value types)
- method: GET, path: "/api/users", status: 200, ms: 42, at: 10:15:00
- method: POST, path: "/api/orders", status: 201, ms: 187, at: 10:15:03
- method: GET, path: "/api/users/99", status: 404, ms: 11, at: 10:15:07
- method: PUT, path: "/api/users/12", status: 200, ms: 203, at: 10:15:12
- method: DELETE, path: "/api/sessions/7", status: 204, ms: 8, at: 10:15:19

(8. Service configuration - a block dict whose values are standard collections)
(Collections nested inside a block dict retain their brackets.)
service: "inventory-api"
version: "2.1.0"
port: 8080
debug: false
database: {host: "db.internal", port: 5432, name: myapp, pool_size: 10}
cache: {host: "cache.internal", port: 6379, ttl: 3600}
features: ["search", "export", "webhooks"]
deployed: 2026-05-18T00:00:00Z

(9. Deeply nested structures - depth 2+ always requires standard bracket form)
{
  suite: integration_tests,
  passed: 2,
  failed: 1,
  cases: [
    {id: 1, name: basic_addition, expected: 3, actual: 3, ok: true},
    {id: 2, name: edge_case_zero, expected: 0, actual: 0, ok: true},
    {id: 3, name: overflow_check, expected: 256, actual: 255, ok: false}
  ]
}

(10. Null and empty value handling)
(Explicit null and absent values are semantically equivalent in STEF.)
{found: true, result: success, warnings: null, errors: [], metadata: null}
```
