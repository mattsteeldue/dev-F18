# lib/ -- Multi-word library modules

Each module in `lib/` covers a coherent feature or hardware subsystem (GRAPHICS, AY,
MOUSE, floating-point, ...). Modules are loaded via `NEEDS MODULENAME`.

## lib/ module conventions

### MARKER pattern

Place `MARKER NO-MODULENAME` near the top (after the initial comments). This lets the
entire module be removed from the dictionary in one step during interactive development.

### Stub + patch pattern (alternative to MARKER)

When the module's primary word is the natural unload handle, define a stub early as a
`FORGET` anchor, then patch it after all subsidiary words are defined:

```forth
: TUTORIAL  NOOP ;          \ stub -- creates FORGET anchor early

\ ... all subsidiary definitions (TUT-TABLE, FILENAME, LOAD-TUTORIAL) ...

' LOAD-TUTORIAL              \ xt of real implementation
' TUTORIAL >BODY !           \ patch stub body: TUTORIAL now calls LOAD-TUTORIAL
```

After loading, `TUTORIAL` behaves exactly like `LOAD-TUTORIAL`. `FORGET TUTORIAL` removes
the stub and every definition that follows it, cleanly unloading the entire module.

### Patch-requiring libraries (FLOATING, ASSEMBLER)

Some libraries cannot use `MARKER` for unloading because they **patch core definitions**
at load time. A plain `MARKER` + `FORGET` would remove the library words but leave the
patched core in an inconsistent state.

**FLOATING** patches `INTERPRET` by replacing the `NUMBER` call with `FNUMBER`, so that
decimal literals (e.g. `3.14`) are parsed as floating-point values. `NO-FLOATING` undoes
this patch, restoring `NUMBER` in `INTERPRET`.

**ASSEMBLER** is a `VOCABULARY`. It patches `;CODE` in the core by replacing the `NOOP`
placeholder left intentionally in the core for this purpose. The patch installs the
ASSEMBLER vocabulary so that words after `;CODE` are looked up in the assembler word-set.
There is currently no `NO-ASSEMBLER` equivalent to restore `;CODE` -- see `TODO.md`.

For FLOATING, the correct unload sequence is:

1. Call `NO-FLOATING` first to restore `NUMBER` inside `INTERPRET`.
2. Then remove the library words via `FORGET` or the module's own unload word.

In tutorials that use FLOATING, `MARKER NEWTASK` is replaced with:

```forth
: NEWTASK  NO-FLOATING ;   \ restores INTERPRET; does NOT remove lib words
```

`NEWTASK` in tutorial 024 only restores integer mode -- it does not unload the
floating-point vocabulary. Reload via `024 TUTORIAL` from a clean session for a full reset.

### LOCALS (named local variables)

`lib/LOCALS.f` adds `VALUE`-like named locals. Unlike FLOATING and ASSEMBLER above it
**patches nothing and redefines no core word**, so `MARKER NO-LOCALS` unloads it cleanly
and loading it cannot disturb already-compiled code. Declared in place, `{ ... }`:

```forth
: MULADD  ( a b c -- n )  { A B C }  A B *  C + ;
```

An optional `--` inside the braces marks off a second group of names: **output locals**.
They are not bound from the stack (created at 0 on every entry) and the body does not
push them either -- every exit path (the closing `;` and any early `EXIT`) pushes their
current value automatically, in declaration order, before restoring the caller's own
locals underneath them:

```forth
: SUM-TO  ( n -- sum )  { N -- ACC }  N 0 ?DO  ACC I 1+ + TO ACC  LOOP ;
```

The older two-part form still works and is what `{` is built on -- `LOCALS-FOR` in
interpretation state, on one line, immediately before the `:`, then `LOCALS` as the
first word of the body (no `--`: every name in this form comes off the stack):

```forth
3 LOCALS-FOR MULADD  A B C
: MULADD  ( a b c -- n )  LOCALS  A B *  C + ;
```

Three facts worth carrying into any `lib/` work, not just into LOCALS:

- **You cannot `CREATE` a word while a colon definition is being compiled.** `CREATE`
  writes at `HERE`, and inside a definition `HERE` *is* the thread being generated, so
  the new word's header lands in the middle of the code and the IP later runs into it.
  Anything else that wants to define words at compile time hits the same wall.
- **The way around it is to end the definition early and re-open the body anonymously.**
  This is the *trampoline* `{` uses, and it is the reason the locals can be declared
  inside the definition instead of before it: `{` compiles a slot plus `EXIT` inside the
  outer word (left smudged, exactly as plain `:` would leave it), and only then -- with
  `HERE` outside any pending definition -- `CREATE`s one cell per local. It then builds,
  by hand, a second nameless colon-header (just the 3-byte `call Enter_Ptr` prologue
  that `:` itself would write) and patches its address into the slot, so the visible
  word is just `( call body ) EXIT`. The nameless body gets no dictionary header at all
  -- unlike `:NONAME` (`inc/_noname.f`), the first design tried here and dropped because
  it hooks a phantom entry into the `CURRENT` vocabulary chain for every definition.
  `LATEST` therefore stays the outer word throughout the body, so `RECURSE` compiles a
  call back to it, not directly into the body: correct, but the trampoline's entry cost
  is paid again on every recursion level, not only once. The user's closing `;` still
  belongs to the outer word: it compiles the body's final `EXIT` and `SMUDGE`s the outer
  word, revealing it in the dictionary.
- **`:` resets `CONTEXT`** (`CURRENT @ CONTEXT !`), so a search-order change made before
  the definition does not survive into its body -- which is why the older form needs a
  second word, `LOCALS`, inside the definition at all.

A local is one permanent cell, not a frame slot, but the word is still **re-entrant**:
`LOCALS` compiles a save of each cell's previous content onto the return stack, and
diverts the definition's `EXIT` into a chain of restore steps by pushing that chain's
address above the caller's return address. Recursion (`RECURSE`) therefore works, and
every exit path -- including an early `EXIT` inside `IF` -- unwinds, without `EXIT`, `;`
or `:` being redefined. Every scope builds its **own** chain rather than sharing one
fixed table, because an output local's step must push its value before restoring, while
an input local's step only restores -- a single shared table cannot represent a
different mix of the two per scope. Output locals are bound to a literal 0 (not a stack
value) by the same entry code, so they too reset on every entry, including a recursive
one. Two consequences worth remembering:

- Each activation costs `4+4n` bytes on the 160-byte return stack shared with the TIB,
  plus one cell for the trampoline's return address, paid on every recursion level (not
  only on entry) because `RECURSE` calls back through the outer word. Measured: one
  local survives 15 recursion levels and corrupts the system at 20. The per-scope chain
  also adds `n+1` dictionary cells per scope (no longer shared across scopes), and an
  output local's exit step costs three more primitives than a plain input local's.
- `ABORT` and `THROW` bypass the chain, leaving inner values in the cells. Harmless
  only because every entry re-binds all the locals before the body runs -- do not
  build anything that reads a local outside its own definition.

Maximum 8 locals per scope, input and output combined. Design notes and the rejected
alternatives are in `prompts/LOCALS-PLAN.md`; tests in `test/LOCALS-TESTS.f`; tutorial 061.

### Other conventions

- **Errors: `?ERROR`, not `ABORT"`.** Library modules report with numbered messages
  (`f n ?ERROR`) from the error blocks, listable with `9 LOAD`; `ABORT"` is left to
  end-user application sources. Document the numbers a module reserves in a comment at
  its top -- `lib/locals.f` (#57-#60) is the model. Rationale in root `CLAUDE.md`,
  "Error reporting: `?ERROR` over `ABORT"` in the library".
- **NEEDS for dependencies**: always use `NEEDS` to pull in prerequisites -- never assume
  a word is already present.
- **Refactoring guideline**: if a definition inside a `lib/` module is general enough to
  be useful independently, extract it into a new `inc/` file and replace the inline
  definition with a `NEEDS` call.

```forth
\ Before -- definition inline in lib/GRAPHICS.f:
: FLIP  ( n -- n' )  ... ;

\ After -- moved to inc/flip.f; lib/GRAPHICS.f becomes:
NEEDS FLIP
```

- **Refactoring caveat -- re-audit the `NEEDS` header when a definition changes which
  words it calls.** When you rewrite a word's body and it starts using a different
  primitive (e.g. `(COLOR)` swapping `NEGATE` for `INVERT`, where `INVERT` comes from
  `inc/invert.f` and is **not** a guaranteed core word), add the matching `NEEDS` line.
  Crucially, do this in **every** module that carries a copy of that definition: several
  features ship in both a modular form (`GRAPHICS-COMMON.f` + the `LAYERxx-GRAPHICS.f`
  files) and a monolithic form (`GRAPHICS.f`), and the two must stay in lockstep. A
  missing `NEEDS` is silent until someone loads that module standalone in a clean session
  and the new dependency is absent. Rule of thumb after such a refactor: grep every sibling
  module for the changed word and confirm its header `NEEDS` block covers the new callee.

## Heap Memory Facility

vForth provides an extended heap in the MMU7 8K page ($E000-$FFFF), growing across
multiple 8K pages. `HP@` tracks the current allocation frontier as a **heap-pointer**
(`ha`).

### MMU7 is a general RAM-paging gateway, not heap-exclusive

The $E000-$FFFF window is not reserved for the heap: it is the single gateway any
code uses to reach the whole 8K-page pool of expansion RAM (well beyond the 64K the
Z80 addresses directly). Compiler internals, `lib/GRAPHICS.f`'s LAYER2 framebuffer
paging, `lib/LED.f`'s large-file editor (pages through most of the ~2MB pool one row
at a time) and heap strings all share it -- whichever 8K page a prior `MMU7!` (or
`NEXTREG $57`) last selected is simply what is currently visible there. Two regimes
use it at different times:

- **Compile time** (`INCLUDE` / `NEEDS` / `LOAD`): dictionary search (`FIND`) pages
  in whichever heap page holds the word headers being searched.
- **Run time**: the dictionary is almost never consulted again -- normal execution
  runs from already-resolved xt/cfa, not from a name search. MMU7 is then free for
  whatever the running code needs: `FAR`-decoded Heap strings (see below), the
  LAYER2 framebuffer, or `LED`'s row paging.

**Exception -- words that DO walk the dictionary at run time.** `WORDS` is the
visible counter-example: it walks the live dictionary chain via `TRAVERSE`/link
fetch/`ID.`, reading heap pages while it runs. This caused a real bug (fixed
2026-06-12, see `emu/test_words_stream.py`): `13 SELECT WORDS` (output redirected to
a file stream) printed garbage and hung. `rst $10` to a file-attached stream goes
through +3DOS, which restores OS default banking on exit and unmaps the vForth heap
page from MMU7; because `WORDS` interleaves heap reads with `EMIT`s, every heap read
after the first emitted character hit the wrong page. Fixed by having `(EMITC)` save
the current MMU7 page before `rst $10` and restore it right after -- mirroring the
save/restore `(FIND)` already did for the same reason. **Rule:** any word that
interleaves a heap/dictionary read with an operation that might itself touch MMU7
(console/file I/O via `rst $10`/`$08`/`$94`, another `FAR`/`HEAP` call, an interrupt
handler, a DMA transfer) must save and restore the MMU7 page around that operation,
or read all the heap data it needs before performing it.

### Heap-pointer format (`ha`)

A heap-pointer is a single 16-bit cell:
- **Bits 15-13** (3 MSBs): page number (relative to the base heap page)
- **Bits 12-0** (13 LSBs): byte offset from `$E000` within that page

`FAR ( ha -- a )` decodes `ha`: maps the page onto MMU7, returns real address in
`$E000-$FFFF`. The page stays mapped until the next `FAR` call.

### Key heap words

| Word | Stack | Description |
|------|-------|-------------|
| `H"` | `( -- ha )` | Parse string literal; store as counted-z-string in heap; return `ha` |
| `FAR` | `( ha -- a )` | Map heap page onto MMU7; return real address in $E000+ |
| `>FAR` | `( ha -- a page )` | Decode `ha` without mapping (low-level) |
| `MMU7!` | `( page -- )` | Map page onto MMU7 slot |
| `MMU7@` | `( -- page )` | Read current MMU7 page |
| `HP@` | `( -- ha )` | Current heap frontier (as heap-pointer) |
| `HALLOT` | `( n -- )` | Allocate n bytes in heap; advance `HP@` |
| `HEAP` | `( n -- a )` | Allocate n bytes; return real address (maps MMU7) |
| `S"` | `( -- addr len )` | Like `H"` but returns real addr+len; **volatile at interpret time** |

### Usage rules

**Rule of thumb: prefer `S"` inside definitions, prefer `H"` when interpreting.**
`S"` (`inc/s~.f`) is state-sensitive and, at interpret time, is built directly on top
of `H"`:

```forth
: S"  ( -- a n )
    STATE @
    IF      COMPILE (H")  H" COMPILE,      \ compiling: see below
    ELSE    H" FAR COUNT                   \ interpreting: allocate + decode now
    THEN
; IMMEDIATE
```

- **Inside a colon-definition** (compile state), `S"` compiles a call to `(H")`
  followed by an inline `ha` cell -- the string is parsed and allocated on the heap
  once, at compile time. Every time the defined word *runs*, `(H")` decodes that `ha`
  via `FAR` fresh and hands back a real addr+len, safe to use right after the `S"`
  call -- this is the normal, safe case, and the one to reach for by default.
- **At the interpreter** (interpret state), `S"` reduces to `H" FAR COUNT`: it
  allocates a *new* heap string on every line executed and decodes it via `FAR`
  immediately, so the returned address goes stale as soon as any other `FAR`/`HEAP`
  call remaps MMU7 (and each re-run leaks another heap allocation). Prefer calling
  `H"` directly instead: keep the stable `ha` around, and decode it with `FAR` only
  immediately before use.

**Pattern for a string table in heap:**

```forth
CREATE MY-TABLE
    H" first string"  ,    \ ha stored in table
    H" second string" ,

\ Use: decode ha just before use
MY-TABLE CELLS + @    \ ha
FAR                   \ real address, MMU7 now mapped
1+                    \ skip count byte -> z-string
```

**`FAR` side-effect:** after `FAR`, MMU7 points to the page containing the returned
address. Do not call another `FAR` (or any word that calls `HEAP`) while you still need
the first address to remain valid.

### Defensive patterns for heap addresses

The address returned by `FAR` is valid only until the next `FAR` or `HEAP` call remaps
MMU7. Copy heap data to stable memory right after decoding:

- Use **`PAD`** when the data must outlive a subsequent operation (e.g. filename string
  passed to `F_OPEN`).
- Use **`HERE`** for short-lived scratch buffers (e.g. the 8-byte header block that
  `F_OPEN` writes internally).

Do not use `PAD` for both purposes simultaneously -- a common mistake is passing `PAD` to
`F_OPEN` as both the filename and the header buffer; the header write then corrupts the
string:

```forth
FILENAME  1+        \ z-string in PAD (count byte skipped)
HERE  1  F_OPEN     \ F_OPEN header at HERE, not PAD
```

**Factor out address resolution into a helper word** when a heap string must be decoded
and stabilised in more than one place:

```forth
: FILENAME  ( n -- a )
    CELLS  TUT-TABLE  +  @      \ ha: heap-pointer to counted-z-string
    FAR                          \ real address, MMU7 now mapped
    DUP C@ 2+                   \ total bytes: count + text + NUL
    PAD OVER BLANK              \ clear PAD
    PAD SWAP CMOVE              \ copy from heap to PAD
    PAD ;                        \ return stable address
```

### Sources

- `inc/doc/far.f` -- `FAR` definition (core word -- reference only)
- `inc/h~.f` -- `H"` definition (FAT mapping: `"` -> `~`)
- `inc/hallot.f` -- `HALLOT`
- `inc/aligned.f` -- `ALIGNED`
- PDF documentation: "Heap memory facility" section

## Deployment to ZX Spectrum Next (nextsync)

There is no separate SD/ staging directory. The repo root (`C:\Zx\Forth\F18`) is the
nextsync root and maps directly to the Next's SD card filesystem. Files edited in `lib/`
are ready to sync immediately.

To transfer files to the Next, run the nextsync server from the repo root:

```
cd C:\Zx\Forth\F18
python nextsync.py
```

Then on the Next, execute `.sync`. Only new or modified files are transferred.
