# From NextBASIC to vForth: a migration guide (draft)

*Draft post for the vForth Next Facebook group - 2026-10-17*

If you know NextBASIC and have ever wondered what the same program looks
like in Forth, there is now a guide for that. I have just published the
first draft of "From NextBASIC to vForth" in the vForth Next repository:

https://github.com/mattsteeldue/vforth-next/tree/master/doc/basic-to-vforth

It follows the ZX Spectrum Next User Manual (third edition) chapter by
chapter: same numbers, same titles, from Basic Programming Concepts to
Using Machine Code, plus four appendices (character set and Z80N
mnemonics, error reports, machine personalities, the calculator) and an
index from every NextBASIC keyword to its vForth counterpart. Keep the
manual open next to it: the guide does not repeat it, it tells you what
changes when you move to Forth.

Every chapter has the same six parts: how much carries over, what
changes in the Forth way of thinking, a correspondence table (BASIC on
the left, vForth on the right), a few short programs written side by
side in both languages, what has no equivalent and why, and where to
read further among the tutorials and help files of vForth.

All the listings are new, written for the guide. Every Forth listing
has been run, and its output checked against what the guide says. The
listings are also on the SD card, in tools/vForth/bas2f: the BASIC ones
as .bas files ready to LOAD, the Forth ones as .f files ready to
INCLUDE, so you can run both and compare.

A few things I enjoyed along the way: a screen filled at random, one
pixel per value of RND, that shows the generator going round its whole
cycle of 65536 numbers; the logarithm computed as the area under a
hyperbola, to plot y = x ln|x| with integers only - the same function I
plotted on a Spectrum for my university exam in 1990; and a little man
walking across the screen, drawn pixel by pixel right in the source.

This is a draft. I have read a good part of it myself, and I am still trying
the BASIC listings on the machine, so a few of them may need a touch.
Corrections, suggestions and questions are very welcome, here or as
issues on GitHub.

Enjoy, and happy Forth-ing!

Matteo
