# help/ -- Word help files

Each file in `help/` is a short plain-text description of one vForth word, displayed
on the ZX Spectrum Next by the `HELP` command. One `.txt` file per word.

## File naming

Same FAT character mapping as `inc/` (see root CLAUDE.md). The `.txt` extension replaces
`.f`. Examples:

| Word | Filename |
|---|---|
| `!` | `!.txt` |
| `?DUP` | `^dup.txt` |
| `/MOD` | `%mod.txt` |
| `>R` | `}r.txt` |
| `S"` | `s~.txt` |

## File format

```
    WORD-NAME    stack-effect

brief description of what the word does (1-3 lines)
```

Rules:
- First line: word name (4-space indent), then stack effect.
- Blank line after stack effect.
- Description: plain prose, no markup, max ~64 columns.
- **Maximum 21 lines total.** `HELP` (`inc/help.f` -> `VIEW-FILE-PAD`) streams the
  file straight to the screen with no pagination/pause -- it just `TYPE`s every
  line until EOF or `[BREAK]`. The ZX Spectrum Next text screen is 24 rows; a
  file longer than 21 lines scrolls its own top off before the reader can see
  it, or runs into the `ok` prompt. Count actual lines (blank separators
  included, final trailing newline excluded) -- e.g. with Python:
  `len(open('help/word.txt',encoding='ascii').read().split(chr(10))[:-1])`.
  If a word needs more, trim prose rather than exceeding the limit: cut an
  example, shorten a rationale, or push secondary detail into a "See also"
  pointer to another HELP entry instead of restating it.
- File ends with a blank line.
- 7-bit ASCII only, no BOM, no smart quotes, no em-dash (use -).

Example (`!.txt`):
```
    !    n a  --

store integer n in the memory cell at address a and a + 1
```

## When to create or update

- Create a `help/` file whenever a new word is added to `inc/` or `lib/`.
- Update the existing file if the word's stack effect or semantics change.
- Core words defined in `project/` (not in `inc/`) also have help files here;
  their source reference is `inc/doc/WORD.f` (read-only, never loaded by NEEDS).

## Encoding check

Before saving, verify ASCII compliance:

```python
python3 -c "
data=open('help/word.txt','rb').read()
bad=[(i,b) for i,b in enumerate(data) if b>0x7E and b!=0x7F]
print('OK' if not bad else bad[:5])
"
```
