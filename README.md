# STEF

This repository hosts the specification for *STEF*, the Simple
Token-Efficient Format. This is a data interchange format with a comprehensive
but familiar data model and presentational forms that minimise punctuational
noise and optimise semantic richness. Output is deliberately token-efficient
when consumed by a large language model.

```
(Apollo program - crewed lunar landings)

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


## Contents

- [STEF Specification](STEF.md)
