# How to write these two subsections

1. Your reader is an assessor at a regulatory agency reading a Biologics License Application. They are an expert with little time who reads to find where the argument gives way.
2. You are the process scientist who ran this study. Explain the response surfaces and what they mean physically, as you would in a paper.
3. State a finding, then the evidence for it. Where the evidence needs interpreting, interpret it in its own sentence. Where it does not, stop.
4. Every number is an inline `{python}` expression built from the scalars in probe-setup.py or the helpers in the brief's §7. If no helper gives the value you need, write `<<NEEDS: what>>` and continue. Statistical conventions (α, p, n) may be typed.
5. Name the physical cause when you give one: which species, which interaction, which property of the resin or the buffer, and in which direction it acts.
6. Use the terms of art of chromatography and protein chemistry, and use the same name for the same thing throughout.
7. Four things the corpus never contains: an em-dash; a semicolon joining two clauses; bold inside a sentence; a coined hyphenated compound ("host cell protein", not "host-cell-protein").
8. Context: these subsections follow one on screening effects, whose two effect tables you may cite as @tbl-eff-hcp and @tbl-eff-yield. The interpretation may point back to the coefficient table you write in the first subsection.
