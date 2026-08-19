# The reading — pilot and sampled

## The pilot (`PCP-005`, TASK-004)

Blind key drawn by `python -c "import secrets; print('new = ' + secrets.choice('AB'))"` into
`$U/blind-key-PCP-005.md` BEFORE the agent is launched; A.pdf/B.pdf copied under the letters by a
command that prints neither the key nor the sizes nor the page counts (the `PCR-007` session
printed page counts and inferred the key — do not); the owner is told:

> `A.pdf` and `B.pdf` are two versions of the whole `PCP-005` protocol (Protein A Chromatography,
> Step 5), about thirty pages each. One is the shipped plan; the other was written under the
> rebuilt apparatus. Which is which is sealed. Suggested read, the same sections in each: Purpose
> and scope; Prior knowledge and quality risk basis; Study design; Acceptance and decision
> criteria; Risks and assumptions. Read more if you want to.
> 1. Which sentences read as machine prose? Quote them, and say A or B.
> 2. Which of the two reads as a paper — A, B, or no difference?

**Rule** (`state.json → decisions.pass_rule`, unchanged from `PCR-007`): PASS iff the owner judges
the new document the better text AND quotes fewer than five sentences from it across what was read.
Applied mechanically after the reading is recorded verbatim and the key opened by checksum.

## The sampled reading per batch (`READ-Bn` tasks)

After a batch is promoted and re-grounded, the owner names ONE document from it. The shipped
version is recovered from git by name (`git show <commit-before-promotion>:pc_package/<DOC>_<uokey>.pdf > $U/Bn-A-or-B.pdf`),
the new one is the promoted pdf; key drawn then, same delivery, same two questions, same rule.
A PASS releases the next batch. A FAIL stops the unit: the next batch is not started, the
finding is recorded, and the owner decides (D8).
