# test/ -- Test suite

Test files for ANS Forth compliance and vForth-specific words.

## Running the tests

```forth
INCLUDE TEST/CORE-TESTS.f
INCLUDE TEST/FLOATING-TESTS.f
INCLUDE TEST/FIXED88-TESTS.f
```

Each suite loads `lib/testing.f` (via NEEDS TESTING inside the file) which provides
the `{...}T` test notation.

## Test notation

```forth
T{  expression  ->  expected-stack  }T
```

Example:
```forth
T{  3 4 +  ->  7  }T
T{  -1 ABS  ->  1  }T
```

A failed test prints a diagnostic; a passing test is silent.

## MARKER pattern

Each main suite begins with:
```forth
MARKER TESTING-DONE
```

Execute `TESTING-DONE` to unload the entire suite from the dictionary after a test run.

## File naming in test/

Individual word-level test files follow the same FAT character mapping as `inc/`:

| Word | Test file |
|---|---|
| `?DUP` | `^dup.f` |
| `/MOD` | `%mod.f` |
| `>R` | `}r.f` |
| `U<` | `u{.f` |
| `S"` | `s~.f` |

These individual files are INCLUDEd by the main suite files (e.g. `CORE-TESTS.f`).

## Adding a test for a new word

1. Create `test/FAT-MAPPED-NAME.f` with `{...}T` assertions for the word.
2. Add an `INCLUDE TEST/FAT-MAPPED-NAME.f` line inside the appropriate main suite
   (`CORE-TESTS.f`, `MISSING-TESTS.f`, or a new suite file).
3. Ensure the file ends with a blank line (known vForth INCLUDE bug: missing trailing
   newline causes a crash).

## Main suite files

| File | Contents |
|---|---|
| `CORE-TESTS.f` | ANS Forth core word compliance |
| `FLOATING-TESTS.f` | Floating-point word tests |
| `FIXED88-TESTS.f` | Fixed-point 8.8 word tests |
| `MISSING-TESTS.f` | Words not yet covered by CORE-TESTS |
| `CUSTOM-TESTS.f` | Project-specific additional tests |
| `basic-assumptions.f` | Fundamental assumptions (cell size, address units, ...) |
