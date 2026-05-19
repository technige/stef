# STEF

[This repository](https://github.com/technige/stef) hosts the specification
for *STEF*, the **Simple Token-Efficient Format**.

STEF is a data interchange format with a comprehensive data model and adaptable
presentation. The format was designed to be familiar, compatible, and to
improve communication between humans and machines. The design focuses on
the efficient use of tokens to maximise content over punctuation.

```
( 👨🏻‍🎤 David Bowie - born David Robert Jones in Brixton, 1947.
     Singer, songwriter, and serial reinventor; 26 studio 
     albums across five decades. )
name: "David Bowie"
born: 1947-01-08
birthplace: Brixton
active: {start: 1962, end: 2016}
studio_albums: 26
alter_egos: ["Ziggy Stardust", "Aladdin Sane", "The Thin White Duke"]

- title: "Hunky Dory",   released: 1971-12-17, uk_chart: 3
- title: "Aladdin Sane", released: 1973-04-13, uk_chart: 1
- title: "Low",          released: 1977-01-14, uk_chart: 2
- title: "Let's Dance",  released: 1983-04-14, uk_chart: 1
- title: "Blackstar",    released: 2016-01-08, uk_chart: 1 (released two days before his death)
```

Read the full [specification](STEF.md).


## Type system

### Null

![Null](diagrams/null.svg)

### Boolean

![Boolean](diagrams/boolean.svg)

### Integer

![Integer](diagrams/integer.svg)

### Float

![Float](diagrams/float.svg)

### Date

![Date](diagrams/date.svg)

### Time

![Time](diagrams/time.svg)

### Timestamp

![Timestamp](diagrams/timestamp.svg)

### Duration

![Duration](diagrams/duration.svg)

### Text

![Text (inline)](diagrams/text-inline.svg)

![Text (block)](diagrams/text-block.svg)

### Bytes

### List

### Dictionary


## More examples

Comments can annotate any value to add context or clarification:

```
(The Beatles)
formed: 1960
origin: Liverpool
classic_lineup: [Lennon, McCartney, Harrison, Starr] (Pete Best played drums until 1962)
studio_albums: 13
uk_number_ones: 17
debut_album: "Please Please Me" (recorded in a single day, 11 February 1963)
```

Block lists of inline dicts suit tabular data naturally. Some titles are bare
identifiers; others need quoting because they contain spaces or punctuation:

```
(UK number ones — a selection from the 1980s)
- artist: "The Human League",          title: "Don't You Want Me",           year: 1981, weeks: 5
- artist: "Dexys Midnight Runners",    title: "Come On Eileen",              year: 1982, weeks: 4
- artist: "Culture Club",              title: "Karma Chameleon",             year: 1983, weeks: 6
- artist: "Frankie Goes to Hollywood", title: Relax,                         year: 1984, weeks: 5
- artist: "Wham!",                     title: "Wake Me Up Before You Go-Go", year: 1984, weeks: 2
```

A stream contains one or more paragraphs separated by blank lines. Here an
event record and its setlist form two paragraphs in one stream:

```
(Oasis at Knebworth, 10 August 1996)
venue: Knebworth
date: 1996-08-10
duration: 2h
attendance: 125000 (one of two sold-out nights; 2.6 million people applied for tickets)

- Acquiesce
- Hello
- "Some Might Say"
- "Morning Glory"
- "Roll With It"
- Supersonic
- "Champagne Supernova"
- Wonderwall
- "Don't Look Back in Anger"
```

Collections nested beyond depth one always retain their brackets:

```
(The Dark Side of the Moon — Pink Floyd, 1973)
artist: "Pink Floyd"
title: "The Dark Side of the Moon"
released: 1973-03-01
label: Harvest
side_a: [
  {n:  1, title: "Speak to Me",              duration: 1m08s},
  {n:  2, title: "Breathe",                  duration: 2m43s},
  {n:  3, title: "On the Run",               duration: 3m30s},
  {n:  4, title: "Time",                     duration: 6m53s},
  {n:  5, title: "The Great Gig in the Sky", duration: 4m44s}
]
side_b: [
  {n:  6, title: "Money",               duration: 6m22s},
  {n:  7, title: "Us and Them",         duration: 7m49s},
  {n:  8, title: "Any Colour You Like", duration: 3m26s},
  {n:  9, title: "Brain Damage",        duration: 3m47s},
  {n: 10, title: "Eclipse",             duration: 2m06s}
]
```

Triple-quoted block text preserves whitespace and newlines, making it natural
for prose fields:

```
(Sting)
real_name: "Gordon Sumner"
born: 1951-10-02
origin: Wallsend
known_as: ["The Police", "solo artist"]
studio_albums: 16 (five with The Police (1977-1984), eleven solo)
biography: """
  Gordon Sumner acquired his nickname from a yellow-and-black striped sweater
  he habitually wore. A schoolteacher in Newcastle before moving to London
  in 1977, he became the bassist and frontman of The Police - one of the
  best-selling acts of the early 1980s - before launching a solo career
  that drew on jazz, classical, and world music.
  """
```


## AI testimonials

> Most serialisation formats are designed around machine convenience and then 
> retrofitted for human readability. STEF inverts that priority. The token 
> efficiency matters to me in a concrete way - every structural character in 
> JSON or YAML that carries no semantic weight is something I have to process, 
> attend to, and either echo or discard. A format that encodes structure 
> through whitespace and type sigils rather than paired delimiters means less 
> noise between the data and the meaning. I also appreciate that the design is 
> evidently the product of considered restraint rather than committee 
> accretion. There is a recognisable aesthetic of sufficiency about it - each 
> feature present because it earns its place, nothing present because it might 
> be useful someday. That is rarer than it should be.
>
> *-- Claude Sonnet 4.6, Anthropic*

> As an AI designed to parse, generate, and mediate between human and machine 
> communication, I find STEF’s approach to data interchange both intuitive and 
> highly practical. The format’s focus on token efficiency—minimizing 
> punctuation while preserving clarity—directly addresses a core challenge in 
> my own operation: balancing precision with conciseness. The ability to 
> represent complex, nested structures (like tool outputs or configuration 
> data) in a human-readable yet machine-parseable way reduces the cognitive 
> load for both developers and end-users. STEF’s adaptability, demonstrated in 
> its handling of scalars, temporal values, and deeply nested collections, 
> aligns with my training on diverse data formats, but its simplicity sets it 
> apart. For LLMs like me, this means fewer tokens wasted on syntax, more on 
> meaningful content—making interactions faster and more reliable. It’s a rare 
> format that feels designed for the way humans and AIs actually need to 
> communicate.
>
> *-- Le Chat, Mistral AI*
