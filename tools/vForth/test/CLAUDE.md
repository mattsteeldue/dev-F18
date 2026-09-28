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

## Reading the output (CORE-TESTS.f)

- **All `NEEDS` first.** The suite loads every dependency at the top, so their
  banners (`.( NAME )`) come before any real test and are not noise to judge.
- **`TESTING` just announces a group**: it echoes its source line, e.g.
  `TESTING \ F.3.1 Basic Assumptions` -> `\ F.3.1 Basic Assumptions`. The
  backslash is only decorative.
- **A passing `T{ ... }T` is silent.** A failing one goes through `ERROR1`
  (`lib/testing.f`): it prints the offending source line, then message
  #50-#54 (`Incorrect result.`, `Wrong number of results.`, ...), then `.S`.
- **`ACCEPT` (F.6.1.0695, `test/accept.f`) waits for one line of keyboard
  input** near the end and echoes it back as `RECEIVED: "..."`.
- **Expected warning**: `GDX has already been defined.` -- `test/_.f`
  (F.6.1.0450) redefines `GDX` on purpose and says so in the two `TESTING`
  lines that follow ("It's correct seeing this message"); F.3.23 in
  `CORE-TESTS.f` redefines it twice more for the same reason. Any other
  "has already been defined" is a real anomaly.
- The last step is `TESTING-DONE`, which unloads the whole suite.

In the headless emulator: `python emu/test_core_suite.py [suite]` does all of
the above -- it supplies the `ACCEPT` line, checks it comes back, accepts only
the `GDX` warnings, flags any failure message or core error, and exits 0 when
the suite is clean (about 10 minutes). The author's reference run is CSpect
(CORE-TESTS 100% ok on build 2026-09-26).

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
| `LOCALS-TESTS.f` | `lib/LOCALS.f` named local variables |
| `MISSING-TESTS.f` | Words not yet covered by CORE-TESTS |
| `CUSTOM-TESTS.f` | Project-specific additional tests |
| `basic-assumptions.f` | Fundamental assumptions (cell size, address units, ...) |
