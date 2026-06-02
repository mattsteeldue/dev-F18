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

### Other conventions

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

## Heap Memory Facility

vForth provides an extended heap in the MMU7 8K page ($E000-$FFFF), growing across
multiple 8K pages. `HP@` tracks the current allocation frontier as a **heap-pointer**
(`ha`).

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

**Use `H"` (not `S"`) for persistent heap strings at interpret time.** `S"` at interpret
time returns a raw `$E000+` address that becomes invalid as soon as a subsequent `FAR` or
`HEAP` call maps a different page. `H"` returns a heap-pointer `ha` that remains valid
indefinitely; decode it with `FAR` immediately before use.

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
