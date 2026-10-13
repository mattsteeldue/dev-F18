# From NextBASIC to vForth

A migration guide for programmers who know NextBASIC and want to move to
vForth, the Forth system for the ZX Spectrum Next.

> **Draft.** Chapters 1 to 9 are written. Chapter 3 (Looping) was the pilot:
> it fixes the form and the tone of every other chapter; the plan is in
> `planners/BASIC-TO-FORTH-PLAN.md`.

## How to read this guide

The guide follows the table of contents of the *ZX Spectrum Next User Manual*,
third edition: one chapter here for each chapter there, with the same number
and title. References such as "p. 21" are page numbers of that manual's PDF.
The manual itself is not quoted: keep it open next to this guide.

Every chapter is a file of its own and has the same six parts:

1. **In short** -- how much of the chapter carries over.
2. **What changes** -- where the Forth model differs from the BASIC one.
3. **Correspondence table** -- BASIC on the left, vForth on the right.
4. **Side by side** -- a few short programs in both languages.
5. **No equivalent** -- what vForth does not offer, and why.
6. **Further reading** -- tutorials, help entries, vForth manual sections.

Conventions used in the listings:

- The BASIC listings are written for this guide; they are not taken from the
  manual.
- In the Forth listings `\ => text` shows what the line prints. When the
  output takes several lines it follows the listing in a block of its own.
- `NEEDS name` loads a word that is not part of the core. Words used without
  a `NEEDS` are always available.
- Every Forth listing is typed into vForth and checked by
  `emu/test_basic_guide.py`, except those that wait for a key, never end,
  or need a part of the machine the emulator does not have (floating
  point, graphics, sound).
- Type the Forth listings of a chapter in order: later ones may use earlier
  definitions.

## Chapters

A chapter without a link is not written yet.

1. [Basic Programming Concepts](01-basic-programming-concepts.md)
2. [Decisions](02-decisions.md)
3. [Looping](03-looping.md)
4. [Procedures and Subroutines](04-procedures-and-subroutines.md)
5. [READ, DATA, RESTORE](05-read-data-restore.md)
6. [Expressions](06-expressions.md)
7. [Strings](07-strings.md)
8. [Functions](08-functions.md)
9. [Mathematical Functions](09-mathematical-functions.md)
10. Random Numbers
11. Arrays
12. Conditions
13. The Character Set
14. More about PRINT and INPUT
15. Colours
16. Graphics
17. Time and Motion
18. Sound and Music
19. NextZXOS and alternatives
20. Channels, Streams, Drivers and Windows
21. Optional Features
22. IN, OUT and the Next Registers
23. The Memory
24. The System Variables
25. Using Machine Code

Appendices:

- A. Character Set, Z80N, Control Codes
- B. Reference -- with the keyword index, BASIC keyword to Forth word
- C. Machine Personalities
- D. The Calculator
