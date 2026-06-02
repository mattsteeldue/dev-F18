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
