# Three months, nine builds, and thirty-six years

*Draft post for the vForth Next community - build 20260820*

With build 20260820 just released, and the new LOCALS library finally where
I wanted it to be, I think it is a good moment to stop for a minute and look
back - not just at the last release, but at the last three months, which have
been the most productive season this project has ever had.

## Where this comes from

Long-time readers know the story, so I will keep it short. This Forth was
born in the spring of 1990, when I spent a couple of months with a ZX
Spectrum 48K and a Microdrive, disassembling White Lightning by hand and
re-typing a Forth of my own with the GENS-3 assembler, a few words at a
time. The cassettes with the original source were later overwritten, the
Spectrum keyboard gave up, and the project went quiet - but it never really
stopped. Through the nineties, the 2000s and the 2010s it kept moving in
the background: the Z80 assembler vocabulary grown out of Albert van der
Horst's 8080 work, the 64-column display, the MGT DISCiPLE port, the mdr
tools, an email from Marcos Cruz in 2015 that woke everything up again.
When the ZX Spectrum Next arrived in April 2020, porting vForth to
NextZXOS was the obvious thing to do, and this repository has existed
since May 2020.

Three decades of silent, continuous, and honestly *fun* work. That part
has not changed. What changed is the pace.

## What changed at the end of May

At the end of May 2026 I adopted Claude Code as a daily companion for this
project. I was curious more than convinced: could an AI coding assistant be
of any use on a direct-threaded Forth for a Z80N machine, where the
"build system" is a hand-tuned assembler listing and the debugger is your
own eyes on a 64-column screen?

The answer, three months and nine released builds later, is in the
HISTORY.txt file. Between build 20260525 and build 20260820 the project
shipped more - and dug deeper - than in any comparable stretch since 2020.
The development repository counts about 170 commits since May 26. But the
number I care about is not the commit count: it is what those commits
contain.

## An emulator as a workbench

The first thing we built together, in early June, was something I had
wanted for years and never found the time for: a headless Z80/Z80N
emulator, written in Python, that boots the *actual* vForth binaries -
the same forth18e.bin and ram8.bin that go on the SD card - all the way
through the COLD/WARM/AUTOEXEC chain to the `ok` prompt. You type
`1 2 + .` and it prints `3`, with no CSpect window, no SD image, no
real hardware. It stubs just enough of NextZXOS and the ROM to let the
system live.

That emulator changed everything downstream. It became the regression
bench for the whole summer: every fix below was reproduced, fixed and
verified there first, then confirmed on CSpect, and it now also powers
the tooling that regenerates the manual's "dictionary structure"
chapter directly from the running binaries.

## Bug archaeology

A system that has been alive for decades accumulates bugs that only
surface when you finally have the instruments to see them. Some of this
summer's catches:

- **The MMU7 clobber.** Sending output to a file corrupted the 8K page
  mapped at $E000-$FFFF after every `rst $10`, so `13 SELECT WORDS`
  derailed into a garbled screen. `(EMITC)` now saves and restores the
  MMU7 page on every character. This one had been lurking in the
  NextZXOS interface since the beginning.
- **EVALUATE inside an INCLUDEd file** lost the rest of the line.
- **(COMPARE)** had a defect that silently broke DIR's sorting, plus a
  subtle FAR-remapping aliasing bug on top of it.
- **F_STAT and F_CHMOD** each corrupted a register across the NextZXOS
  call - one of them restoring the return-stack pointer with a
  mislabeled `pop hl`.

None of these were new bugs. They were old bugs, finally caught.

## Libraries, from pixels to interrupts

The feature side kept the same rhythm. The whole LAYERxx-GRAPHICS family
was refactored into uniform per-mode modules sharing common words, and
gained LAYER22, a driver for the Layer 2 320x256 mode with its 80K
vertical-band framebuffer paged through MMU7 (with an experimental
640x256 sibling waiting for verification on real hardware). PAINT was
rewritten around a proper Scanline Span Fill. DIR was rebuilt on
NextZXOS's own wildcard-filtered directory calls, and the filesystem
toolkit grew CD, PWD, MAKEDIR and REMOVEDIR. New libraries appeared for
the keyboard matrix, DMA, and hardware Interrupt Mode 2 on the Z80N.

And then LOCALS - which deserves its own chapter, below.

## Documentation, at last

The part of a one-person project that always loses the priority battle is
documentation. Not this summer. The tutorial directory now holds over 60
guided tutorials - from `1 2 + .` to sprites, the copper, dot commands
and standalone executables - cross-referenced against Leo Brodie's
*Starting FORTH*. The HELP system serves about 450 plain-text pages, one
per word. The reference manual was reorganized and regenerated where it
describes the living dictionary. And the wiki keeps growing, including
Rob Probin's excellent pages on installing vForth Next under MAME and
ZEsarUX - thank you, Rob.

## LOCALS, one step at a time

The piece I am most fond of is the new LOCALS library, and the way it
was built says more about this summer than the feature itself. vForth
now has named local variables with an inline declaration - `{ a b c }`
as the first word of a definition - including an optional group of
*output* locals, marked by `--` inside the braces, that every exit path
pushes automatically. It patches nothing and redefines no core word, so
`MARKER NO-LOCALS` unloads it cleanly, and definitions remain fully
re-entrant: RECURSE and an early EXIT both unwind correctly.

I did not design that in one sitting. I had the goal clear from the
start; the road there was deliberately broken into small, verifiable
steps - eight internal versions in five days, each one proven on the
emulator before touching CSpect:

1. **Scope first.** Where do local names live without polluting the
   dictionary? Answer: a dedicated `VOCABULARY`, reused and reset at
   every definition, so `a` inside one word never collides with `a`
   inside another - or with the global dictionary.
2. **A static version.** The first working form was two-part and
   humble: `3 LOCALS-FOR MULADD A B C` before the colon, `LOCALS` at
   the start of the body. Locals were permanent cells - simple,
   inspectable, and not yet re-entrant. That version still exists, as
   a dependency-free reference rendering.
3. **Re-entrancy.** Instead of building stack frames, LOCALS adopted
   shallow binding: on entry each local's previous value is saved on
   the return stack, and EXIT is diverted through a restore chain that
   puts everything back. Recursion suddenly worked - factorial and all -
   without changing what a local *is*.
4. **The braces.** `{ a b c }` inside the definition itself runs into a
   hard core constraint: CREATE inside an open colon definition breaks
   the thread being compiled. First workaround: a *trampoline* - close
   the definition early on a stub, build the locals and the real body
   in a second anonymous thread, and jump across. It worked, but every
   call paid an extra indirection, and recursion paid it at every
   level. A working dead end.
5. **BRANCH instead.** The clean escape was the idiom the core already
   uses for IF/THEN: compile a forward BRANCH that simply jumps over
   the headers created mid-definition. One thread again, the trampoline
   gone, and the decompiler SEE was then taught to recognize a
   definition that opens with a BRANCH.
6. **Closures, at last.** The final refinement replaced the raw binding
   sequence with one *binder word per local* - same name, second
   vocabulary, built with `CREATE ... DOES>`, closure-style - so SEE
   now decompiles a definition with locals into something a human can
   actually read. This step failed on the first attempt, was diagnosed
   as structurally impossible, and rolled back; the next day, re-reading
   the inner interpreter with fresh eyes, the diagnosis was overturned -
   the offending return-stack level came from one avoidable call, not
   from DOES> itself - and version 8 shipped.

Every one of those steps, including the wrong diagnosis, is written
down in a two-thousand-line design document in the repository. The dead
ends are recorded as carefully as the successes, because they are the
part you forget first and pay for twice.

## What I learned

Working with an AI assistant on a codebase like this is not magic
dictation. It is closer to finally having a colleague who never gets
bored: one who will happily write a Python emulator so that a
thirty-year-old bug has nowhere left to hide, who reads a `.lst` file
without complaining, and who needs to be told - firmly, sometimes twice -
how a Forth programmer thinks. The judgment, the taste, and the
occasional stubborn wrong idea are still mine.

LOCALS is the clearest example of the division of labour. The paradigm
never wavered: I knew what I wanted locals to *be* on this machine.
What the AI changed is the speed of exploration - I would estimate
tenfold. Each of those design steps used to be weeks of evenings:
sketch it, type it in, crash the machine, think in the dark. This
summer a candidate model could be implemented, exercised against the
emulator, and accepted or demolished in a day - and when the facts
contradicted the model, we did not patch around the contradiction: we
changed the model and rebuilt, cheaply. Version 7 was discarded whole.
Nobody mourned it. That freedom to throw work away is, I think, the
real acceleration.

Thirty-six years in, this is still the most fun I have with a computer.
The next items on the list are already queued up. As always, everything
is at https://github.com/mattsteeldue/vforth-next - and if you try it and
something breaks, that is a gift: tell me.

*Matteo Vitturi, August 2026*
