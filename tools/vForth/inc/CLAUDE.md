# inc/ -- Single-word definitions

Each file in `inc/` defines exactly one Forth word. Files are loaded on demand via `NEEDS`.
The filename is the FAT-mapped word name with `.f` extension (see FAT Filename Character
Mapping in root CLAUDE.md).

`inc/doc/` contains reference-only copies of core words (never loaded by NEEDS; for
human reading only).

## inc/ file conventions

One word per file. Typical structure:

```forth
\
\ word-name.f
\
.( WORD-NAME )
\
NEEDS dependency1    \ only if needed

: WORD-NAME  ( stack-effect )
    ...
;
```

- The `.( WORD-NAME )` banner confirms load at the console.
- `NEEDS` pulls dependencies only if not already in the dictionary.
- Use `NEEDS` at interpreter level only -- never inside a colon-definition.
- Always ensure the file ends with a blank line (known bug: missing trailing newline
  causes a crash).
- Report errors with a numbered message (`f n ?ERROR`), not with `ABORT"` -- see
  "Error reporting: `?ERROR` over `ABORT"` in the library" in root `CLAUDE.md`.
  `ABORT"` remains available to end-user application sources.

## CODE words in inc/ -- development vs. release form

Low-level `CODE` definitions can be written using the ASSEMBLER vocabulary during
development for readability. At release, convert the mnemonics to raw hex literals
using `C,` -- this avoids loading the ASSEMBLER vocabulary (~7 KB).

**Development form (readable, on-machine only):**
```forth
NEEDS ASSEMBLER
CODE SYNC-VID
    halt
    NEXT
C;
```

**Release form (hex literals, no ASSEMBLER dependency):**
```forth
CODE SYNC-VID
    $76 C,             \ halt
    $DD C, $E9 C,      \ jp (ix)
    SMUDGE
    \
```

The ASSEMBLER vocabulary is a vForth VOCABULARY available only on the ZX Spectrum Next /
CSpect; it plays no role in SjASMPlus development.

**Do not write `NEEDS CODE`.** `CODE` is a core word, always present in
`forth18e.bin`, so guarding it with `NEEDS` is pointless noise. A release-form
CODE file needs no dependency guard at all -- only the words it actually uses
(e.g. `NEEDS GRAPHICS-COMMON`).

> **Archaeology -- `MCOD` vs `CODE` in F18e.f.** During the original
> self-bootstrap from vForth, the author defined assembler words via a word
> `MCOD` (renamed to `CODE` only at the very end of compilation) to guarantee
> the freshly-built `CODE` was used rather than the one from the previous
> compilation. The vestigial `NEEDS CODE` guards (and the `\ CODE = RENAME MCOD
> CODE` comments) once removed from these files are a leftover of that era. The
> idiosyncrasy survives only in the historical `src/F18e.f`; leave it there as-is
> -- do not reintroduce it in `inc/`.

The canonical template is [`inc/.border.f`](.border.f):

```forth
\
\ .border.f
\
.( .BORDER )
\
BASE @          \ save base status
HEX
CODE .BORDER  ( b -- )
    E1  C,          \ pop hl
    ...
    DD  C,  E9 C,   \ jp (hl)
    SMUDGE
BASE !
```

### Automatic conversion: asm2hex.py

`util/asm2hex.py` converts a dev-form `.f` file (using ASSEMBLER vocabulary mnemonics)
to release form (raw hex `C,` literals) automatically:

```
python3 util/asm2hex.py input.f           (stdout)
python3 util/asm2hex.py input.f -o out.f  (file)
```

Lines outside `CODE...C;` blocks pass through unchanged. `C;` is replaced by `SMUDGE`.
`NEXT` becomes `$DD C, $E9 C,`. Address-dependent operands (`AA,`, `HOLDPLACE`,
`DISP,`, `BACK,`) are preserved as-is. Unrecognised patterns pass through with a
`\ WARN` comment for manual review.

The script accepts both upper and lowercase mnemonics in the source.

### Numeric literal conventions

Use `$`, `%`, `#` prefix characters rather than switching BASE globally.
Changing BASE during compilation (e.g. `HEX` inside a source file) is error-prone.

- **Preferred** -- prefix characters in source: `$FF`, `%11111111`, `#255`
- **Tolerated** -- global base switch for output formatting: `HEX . DECIMAL`
- **Discouraged** -- global base switch during compilation or source loading

Forth code in uppercase; Z80 opcode hex comments in lowercase for reading fluency.

### ASSEMBLER vocabulary: case convention inside CODE bodies

When using the ASSEMBLER vocabulary (not raw `C,` hex):
- Z80 mnemonic words and register/flag specifiers: **lowercase**
  (`halt`, `exx`, `nop`, `pop bc|`, `adda (hl)|`, `jpf pe|`, `ld c'| a|`, ...)
- Forth meta-words and commaers: **UPPERCASE**
  (`HERE`, `NEXT`, `HOLDPLACE`, `BACK,`, `DISP,`, `AA,`, `N,`, `NN,`, `D,`, `LH,`, `C;`)

## NEEDS mechanism (reminder)

`NEEDS` is a core word compiled into `forth18e.bin`. It searches `inc/` first, then
`lib/`. If the word is already in the dictionary, the file load is skipped silently.

If neither `inc/NAME.f` nor `lib/NAME.f` exists, `NEEDS` emits the word name followed
by message 43 ("File not found") after both directories have been attempted.
