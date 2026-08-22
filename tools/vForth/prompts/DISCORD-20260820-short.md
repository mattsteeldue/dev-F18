🚀 vForth 1.8 — builds 2026-08-17 and 2026-08-20 are out!

Two builds, one headline: **vForth has named local variables now.**

The core binary is unchanged in both (bar the build stamp) — LOCALS is a pure library. It patches nothing and redefines no core word, so `MARKER NO-LOCALS` unloads it cleanly.

**Declared in place**
```forth
: MULADD  ( a b c -- n )  { A B C }  A B * C + ;
```
`{` is the first word of the body: it names the arguments in the order the caller pushed them, and binds them. A local reads like a `VALUE`, and you write to it with `TO` (`12 TO A`).

**Output locals**
An optional `--` marks a second group: created at 0 on every entry and pushed automatically by every exit path, the closing `;` and any early `EXIT` alike.
```forth
: SUM-TO  ( n -- sum )  { N -- ACC }  N 0 ?DO  ACC I 1+ + TO ACC  LOOP ;
```

**Re-entrant — RECURSE works**
A local here is a permanent cell, not a frame slot: on entry its previous content is saved on the return stack and every exit path restores it, so two live activations each see their own values. Budget: 8 locals per scope, 4+4n bytes of return stack per activation. The older `LOCALS-FOR` / `LOCALS` two-part form still works, and is what `{` is built on.

**SEE reads it back**
Decompiling a word with locals used to hang; it now terminates and prints the binders by name.

**Also in these builds**
• Fixed a trailing space in IDE_PATH's pathspec: MAKEDIR and REMOVEDIR were creating directories whose name ended in a blank.
• help/ pages completed for every word whose name needs FAT filename mapping, plus ASK-Y/N and BMP-LOAD".
• Tutorial 061-locals walks through all of it; tests in test/LOCALS-TESTS.f.

Grab it here: https://github.com/mattsteeldue/vforth-next
Full changelog in HISTORY.txt.

Bug reports and feedback very welcome. Happy forth-ing on your Next! 🐉
