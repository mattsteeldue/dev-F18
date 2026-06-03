#!/usr/bin/env python3
"""
lint_tutorial.py -- Static linter for vForth tutorial files.

Usage:
    python tools/lint_tutorial.py                          # lint all tutorial/*.f files
    python tools/lint_tutorial.py tutorial/017-defer-is.f  # lint one file
    python tools/lint_tutorial.py --strict                 # treat warnings as errors
    python tools/lint_tutorial.py --fix                    # replace TAB with SPACE in-place

Exit code: 0 if no errors (warnings OK), 1 if any errors.

Claude Code PostToolUse hook (auto-lint after every Edit/Write):
    Add to .claude\\settings.local.json (create if not present):

    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "python tools/lint_tutorial.py \\"${file}\\""
              }
            ]
          }
        ]
      }
    }

    With this hook the linter fires automatically after each file edit and
    its output lands in the conversation context, so errors are caught
    immediately without manual invocation.
"""

import sys
import os
import glob

# ---------------------------------------------------------------------------
# Word sets
# ---------------------------------------------------------------------------

CORE_WORDS = {
    'DUP', 'DROP', 'SWAP', 'OVER', 'ROT', '-ROT', 'NIP', 'TUCK', 'PICK', 'ROLL',
    '+', '-', '*', '/', 'MOD', '/MOD', '*/', '*/MOD', '1+', '1-', '2+', '2-',
    '2*', '2/', 'NEGATE', 'ABS', 'MAX', 'MIN', 'AND', 'OR', 'XOR', 'NOT', 'INVERT',
    '0=', '0<', '0>', '<', '>', '=', '<>', 'U<', 'U>',
    '@', '!', 'C@', 'C!', '2@', '2!', '?', '+!',
    'MOVE', 'FILL', 'CMOVE', 'CMOVE>',
    'COUNT', 'HERE', 'ALLOT', ',', 'C,', 'ALIGN', 'ALIGNED',
    'CELLS', 'CELL+', 'CHARS', 'CHAR+',
    'DEPTH', '>R', 'R>', 'R@', 'I', 'J',
    'IF', 'ELSE', 'THEN', 'BEGIN', 'UNTIL', 'WHILE', 'REPEAT',
    'DO', '?DO', 'LOOP', '+LOOP', 'LEAVE', 'EXIT',
    'CASE', 'OF', 'ENDOF', 'ENDCASE',
    ':', ';', 'CONSTANT', 'VARIABLE', 'CREATE', 'DOES>',
    'LITERAL', '[', ']', "'", "[']", 'EXECUTE', 'COMPILE,', 'POSTPONE',
    'IMMEDIATE', 'FORGET', 'MARKER', 'FIND', '-FIND',
    'EMIT', 'EMITC', '.', 'U.', 'HEX.', 'CR', 'SPACE', 'SPACES', '.S',
    '.(', '."', '\\', '(',
    'KEY', 'WORD', 'PARSE', 'PARSE-NAME', 'SOURCE', '>IN',
    'EVALUATE', 'INCLUDE', 'NEEDS', 'LOAD', 'BLOCK', 'BUFFER',
    'UPDATE', 'FLUSH', 'SAVE-BUFFERS', 'EMPTY-BUFFERS',
    'NOOP', 'TRUE', 'FALSE', 'BL', 'CELL',
    'S"', 'C"', 'H"', 'Z"', 'PAD', 'TIB',
    'BASE', 'DECIMAL', 'HEX', 'BINARY', 'OCTAL', 'FLOATING', 'INTEGER',
    'STATE', 'BLK', 'SCR', 'SPAN', '>OUT',
    'COLS', 'ROWS', 'CLS', 'AT-XY', 'PAGE',
    'TYPE', 'EXPECT', 'ACCEPT',
    'SP@', 'SP!', 'RP@', 'RP!',
    'LAST', 'CONTEXT', 'CURRENT', 'VOCABULARY', 'ALSO', 'ONLY', 'FORTH',
    'DEFINITIONS', 'ORDER', 'WORDS', 'SEE', 'DUMP',
    'NMODE', 'FAR', 'HALLOT', 'HEAP', 'HP@', 'LIMIT', 'FIRST', 'FREE',
    'SAVE', 'RESTORE', 'VERSION', 'COLD', 'ABORT', 'QUIT', 'BYE',
    '2DUP', '2DROP', '2SWAP', '2OVER', '2ROT',
    'D+', 'D-', 'DNEGATE', 'DABS', 'D<', 'D=',
    'M+', 'M*', 'M*/', 'UM*', 'UM/MOD', 'SM/REM', 'FM/MOD', 'D.', 'UD.',
    'F_OPEN', 'F_CLOSE', 'F_READ', 'F_WRITE', 'F_SEEK', 'F_TELL',
    'F_INCLUDE', 'VIEW-FILE-PAD',
    'CATCH', 'THROW', 'ABORT"', '?ERROR', 'ERROR', 'MESSAGE',
    'EDIT', 'LIST', 'THRU', '.LINE',
    'CHAR', '[CHAR]',
    # vForth synonyms / extensions that are always present
    'UPPER', 'LOWER', 'LSHIFT', 'RSHIFT',
    'COMPILE', '[COMPILE]', '<BUILDS',
    'ENDIF', 'END', 'AGAIN',      # vForth synonyms for THEN / UNTIL / REPEAT
    '?TERMINAL',
    # Numeric output / formatting
    'U.R', '.R', '#', '#S', '#>', '<#', 'HOLD', 'SIGN',
    'D.R',
    # Misc always-present
    'CURS', 'NO-FLOATING',
    ',\"',                         # counted-z-string builder
}

# Words that require a NEEDS to be usable.
# The linter warns if one of these is used in executable position without
# a prior matching NEEDS line (or a NEEDS that "provides" it -- see NEEDS_PROVIDES).
NEEDS_WORDS = {
    'VALUE', 'TO', 'DEFER', 'IS', 'ACTION-OF',
    '2CONSTANT', '2VARIABLE', 'BUFFER:',
    'FVALUE',
    'F+', 'F-', 'F*', 'F/', 'FNEGATE', 'FABS', 'FSQRT', 'FSIN', 'FCOS',
    'FTAN', 'FEXP', 'FLN', 'FLOG', 'F**', 'F<', 'F>', 'F=', 'F0<', 'F0=',
    'FLOAT', 'FTRUNC', 'FROUND', 'F.', 'FE.', 'FS.',
    'TESTING', 'T{', '}T',
    'SPRITES', 'COPPER', 'TIMER', 'KEYBOARD',
    'STRUCT', 'FIELD', 'END-STRUCT', 'ENUMERATED',
}

# When NEEDS <key> is seen, also mark the value-set words as satisfied.
# This handles cases where one NEEDS loads a bundle of related words.
NEEDS_PROVIDES = {
    # NEEDS FLOATING loads the entire floating-point library
    'FLOATING': {
        'F+', 'F-', 'F*', 'F/', 'FNEGATE', 'FABS', 'FSQRT', 'FSIN', 'FCOS',
        'FTAN', 'FEXP', 'FLN', 'FLOG', 'F**', 'F<', 'F>', 'F=', 'F0<', 'F0=',
        'FLOAT', 'FTRUNC', 'FROUND', 'F.', 'FE.', 'FS.', 'FVALUE',
        'FLOATING', 'INTEGER', 'NO-FLOATING',
    },
    # NEEDS GRAPHICS loads the graphics library including layer helpers
    'GRAPHICS': {
        'LAYER0', 'LAYER1', 'LAYER2', 'LAYER12', 'LAYER!',
        'PLOT', 'POINT', 'XPLOT', 'LINE', 'DRAW-LINE',
        'CIRCLE', 'ELLIPSE', 'FILL-RECT',
        'PIXELADD', 'PIXELSUB',
        'ATTRIB', 'ATTRIB!', 'ATTRIB@',
        'SETUP', 'IDE-MODE@', 'IDE-MODE!',
        'LAYER2-BASE', 'LAYER2-PAGE',
    },
    # NEEDS TESTING loads the test harness
    'TESTING': {
        'TESTING', 'T{', '}T',
    },
    # NEEDS ASSEMBLER loads the assembler vocabulary
    'ASSEMBLER': {
        'CODE', 'C;', 'NEXT', 'HOLDPLACE', 'BACK,', 'DISP,', 'AA,', 'N,', 'NN,',
    },
    # NEEDS MOUSE
    'MOUSE': {
        'MOUSE-X', 'MOUSE-Y', 'MOUSE-B', 'MOUSE@', 'MOUSE-POLL',
    },
    # NEEDS AY
    'AY': {
        'AY!', 'AY@', 'AY-TONE', 'AY-NOISE', 'AY-ENV', 'AY-CHAN',
        'NOTE', 'CHORD', 'MELODY', 'BEEP',
    },
    # NEEDS BEEPER
    'BEEPER': {
        'BEEP', 'BEEPER',
    },
    # NEEDS MMU
    'MMU': {
        'MMU@', 'MMU!', 'MAP-PAGE', 'UNMAP-PAGE',
    },
    # NEEDS COPPER
    'COPPER': {
        'COPPER-DATA', 'COPPER-WAIT', 'COPPER-MOVE', 'COPPER-STOP',
        'COPPER-ENABLE', 'COPPER-DISABLE',
    },
    # NEEDS KEYBOARD
    'KEYBOARD': {
        'KEY-DOWN?', 'KSHIFT', 'KCAPS', 'KSYM',
    },
}

# Words that consume the NEXT token as a quoted argument (not executable position).
# After seeing one of these, skip the immediately following token.
QUOTE_NEXT_TOKEN = {
    'POSTPONE', 'COMPILE', '[COMPILE]',
    'CHAR', '[CHAR]',
}

# Control structure depth modifiers inside colon definitions.
# Openers increment depth; closers decrement.
# ELSE/WHILE are depth-neutral (they sit between an opener and closer pair).
CTRL_DEPTH_OPEN  = {'IF', 'BEGIN', 'DO', '?DO', 'CASE', 'OF'}
CTRL_DEPTH_CLOSE = {'THEN', 'ENDIF', 'UNTIL', 'END', 'REPEAT',
                    'LOOP', '+LOOP', 'ENDCASE', 'ENDOF', 'AGAIN'}


# ---------------------------------------------------------------------------
# Diagnostic helpers
# ---------------------------------------------------------------------------

def make_diag(level, lineno, msg):
    return (level, lineno, msg)


# ---------------------------------------------------------------------------
# Source line tokeniser
# ---------------------------------------------------------------------------

def strip_line_comment(line):
    """
    Remove a backslash line comment.  '\\' is a comment introducer only when it
    appears as a complete token (at start of line or preceded by whitespace).
    Returns the code portion of the line (everything before the \\ token).
    """
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '\\' and (i == 0 or line[i-1] in ' \t'):
            return line[:i], True
        i += 1
    return line, False


def extract_tokens(code_part):
    """
    Walk the code portion of a line and return a list of (upper_token, orig_token)
    tuples that are in executable position (i.e. not inside string literals or
    inline parenthesis comments).

    String openers handled:  ."  S"  H"  Z"  C"  ABORT"
    Print-string opener:     .(
    Inline comment:          (
    All of these consume content up to the closing delimiter on the same line.
    """
    tokens = []
    rest = code_part

    while True:
        rest = rest.lstrip()
        if not rest:
            break

        # Find end of the first token
        sp = 0
        while sp < len(rest) and rest[sp] not in ' \t':
            sp += 1
        tok = rest[:sp]
        tok_upper = tok.upper()
        after_tok = rest[sp:]  # everything after the token (including leading space)

        # --- String-literal openers: skip content to closing " ---
        if tok_upper in ('."', 'S"', 'H"', 'Z"', 'C"', 'ABORT"'):
            tokens.append((tok_upper, tok))
            close = after_tok.find('"')
            if close != -1:
                rest = after_tok[close+1:]
            else:
                rest = ''  # unclosed on this line
            continue

        # --- .( ... ) print string: skip content to closing ) ---
        if tok_upper == '.(':
            tokens.append((tok_upper, tok))
            close = after_tok.find(')')
            if close != -1:
                rest = after_tok[close+1:]
            else:
                rest = ''
            continue

        # --- ( ... ) inline comment: skip content to closing ) ---
        if tok == '(':
            # Skip everything until the closing )
            close = after_tok.find(')')
            if close != -1:
                rest = after_tok[close+1:]
            else:
                rest = ''
            continue

        # Regular token
        tokens.append((tok_upper, tok))
        rest = after_tok

    return tokens


# ---------------------------------------------------------------------------
# Main per-file linter
# ---------------------------------------------------------------------------

def lint_file(path):
    """
    Lint a single tutorial file.
    Returns a list of (level, lineno, message) tuples.
    """
    diags = []

    # --- Read raw bytes for encoding checks ---
    try:
        with open(path, 'rb') as fh:
            raw = fh.read()
    except OSError as exc:
        return [make_diag('ERROR', 0, f'cannot read file: {exc}')]

    # BOM check
    if raw[:3] == b'\xef\xbb\xbf':
        diags.append(make_diag('ERROR', 1,
                               'BOM detected (file must be 7-bit ASCII, no BOM)'))
        raw = raw[3:]

    # NUL byte check
    nul_pos = raw.find(b'\x00')
    if nul_pos != -1:
        lineno = raw[:nul_pos].count(b'\n') + 1
        diags.append(make_diag('ERROR', lineno,
                               'NUL byte (0x00) found -- silently stops interpretation'))

    # TAB check
    tab_pos = raw.find(b'\x09')
    if tab_pos != -1:
        lineno = raw[:tab_pos].count(b'\n') + 1
        diags.append(make_diag('ERROR', lineno,
                               'TAB (0x09) found -- use spaces; TAB disrupts the Forth tokeniser'))

    # Non-ASCII check (allowed: 0x0A 0x0D 0x20-0x7E 0x7F)
    for byte_idx, b in enumerate(raw):
        if not (b == 0x0A or b == 0x0D or
                (0x20 <= b <= 0x7E) or b == 0x7F):
            lineno = raw[:byte_idx].count(b'\n') + 1
            diags.append(make_diag('ERROR', lineno,
                                   f'non-ASCII byte 0x{b:02X} at byte offset {byte_idx}'))
            break  # report first occurrence only

    # Trailing-spaces check.
    # INCLUDE/NEEDS crashes if the last line ends with one or more spaces before
    # the newline, regardless of what non-space content precedes them.
    text = raw.decode('ascii', errors='replace')
    lines_raw = text.splitlines()
    total_lines = len(lines_raw)
    if lines_raw and lines_raw[-1].endswith(' '):
        diags.append(make_diag('ERROR', total_lines,
                               'last line has trailing spaces (INCLUDE/NEEDS will crash)'))

    # Build set of suppressed line numbers: lines containing '\ lint: ok'
    suppressed = {
        idx + 1
        for idx, line in enumerate(lines_raw)
        if r'\ lint: ok' in line
    }

    # --- Parse lines for structural / semantic checks ---
    lines = lines_raw  # already split

    in_colon        = False   # inside a : ... ; definition
    ctrl_depth      = 0       # control structure nesting depth inside colon def
    colon_start_line = 0
    marker_found    = False
    marker_checked  = False   # True once we have seen the first interpreter-level token
    needs_loaded    = set()   # word names for which NEEDS has been seen
    needs_warned    = set()   # avoid duplicate warnings per word

    i = 0
    while i < len(lines):
        lineno = i + 1
        line   = lines[i]
        i += 1

        # Column width check (raw line before stripping)
        if len(line) > 80:
            diags.append(make_diag('WARNING', lineno,
                                   f'line exceeds 80 columns ({len(line)})'))

        # Strip line comment
        code_part, _ = strip_line_comment(line)

        # Extract executable tokens (string contents already skipped)
        tokens = extract_tokens(code_part)

        # Process tokens
        t = 0
        while t < len(tokens):
            tok_upper, tok_orig = tokens[t]
            t += 1

            # ----------------------------------------------------------------
            # NEEDS at interpreter level: record the provided word(s)
            # ----------------------------------------------------------------
            if tok_upper == 'NEEDS' and not in_colon:
                if t < len(tokens):
                    word = tokens[t][0]
                    t += 1
                    needs_loaded.add(word)
                    # Also mark all words bundled by this NEEDS
                    if word in NEEDS_PROVIDES:
                        needs_loaded.update(NEEDS_PROVIDES[word])
                continue

            # ----------------------------------------------------------------
            # INCLUDE at interpreter level: consume filename token, no error
            # ----------------------------------------------------------------
            if tok_upper == 'INCLUDE' and not in_colon:
                if t < len(tokens):
                    t += 1  # consume filename
                continue

            # ----------------------------------------------------------------
            # NEEDS / INCLUDE inside colon definition: forbidden
            # ----------------------------------------------------------------
            if tok_upper in ('NEEDS', 'INCLUDE') and in_colon:
                diags.append(make_diag('ERROR', lineno,
                                       f'{tok_upper} inside colon definition'))
                if tok_upper == 'NEEDS' and t < len(tokens):
                    t += 1  # consume the word name anyway
                continue

            # ----------------------------------------------------------------
            # Words that quote their next token (POSTPONE, COMPILE, [COMPILE],
            # CHAR, [CHAR]) -- the following token is NOT in executable position.
            # ----------------------------------------------------------------
            if tok_upper in QUOTE_NEXT_TOKEN:
                if t < len(tokens):
                    t += 1  # skip the quoted token
                continue

            # ----------------------------------------------------------------
            # MARKER / NEWTASK check: first interpreter-level token must be
            # either MARKER NEWTASK  or  : NEWTASK (patch-requiring libraries
            # such as FLOATING use a colon definition instead of MARKER).
            # Must come BEFORE the ':' colon-opener check (which has continue).
            # ----------------------------------------------------------------
            if not marker_checked and not in_colon:
                if tok_upper == 'MARKER':
                    if t < len(tokens):
                        marker_name = tokens[t][0]
                        t += 1
                        if marker_name == 'NEWTASK':
                            marker_found = True
                        else:
                            diags.append(make_diag(
                                'WARNING', lineno,
                                f'MARKER name is {marker_name!r}, expected NEWTASK'))
                            marker_found = True
                    marker_checked = True
                    continue
                elif tok_upper == ':':
                    # Accept `: NEWTASK ...` as valid substitute for MARKER NEWTASK.
                    # Also open the colon definition here and continue.
                    if t < len(tokens) and tokens[t][0] == 'NEWTASK':
                        marker_found = True
                    marker_checked = True
                    in_colon = True
                    ctrl_depth = 0
                    colon_start_line = lineno
                    if t < len(tokens):
                        t += 1  # skip definition name
                    continue
                else:
                    marker_checked = True
                    # Will report after loop if marker_found is still False

            # ----------------------------------------------------------------
            # : opens a colon definition
            # ----------------------------------------------------------------
            if tok_upper == ':' and not in_colon:
                in_colon = True
                ctrl_depth = 0
                colon_start_line = lineno
                if t < len(tokens):
                    t += 1  # skip the definition name (not executable position)
                continue

            # ----------------------------------------------------------------
            # ; closes a colon definition
            # ----------------------------------------------------------------
            if tok_upper == ';':
                if in_colon:
                    if ctrl_depth != 0:
                        diags.append(make_diag(
                            'ERROR', lineno,
                            f'unbalanced control structure at ; '
                            f'(depth={ctrl_depth}, definition opened near line '
                            f'{colon_start_line})'))
                    in_colon = False
                    ctrl_depth = 0
                continue

            # ----------------------------------------------------------------
            # Control structure depth tracking (inside colon definitions only)
            # ----------------------------------------------------------------
            if in_colon:
                if tok_upper in CTRL_DEPTH_OPEN:
                    ctrl_depth += 1
                elif tok_upper in CTRL_DEPTH_CLOSE:
                    ctrl_depth -= 1
                    if ctrl_depth < 0:
                        diags.append(make_diag(
                            'ERROR', lineno,
                            f'unmatched {tok_upper} (no matching opener)'))
                        ctrl_depth = 0

            # ----------------------------------------------------------------
            # NEEDS dependency check: warn if a non-core word lacks NEEDS
            # ----------------------------------------------------------------
            if tok_upper in NEEDS_WORDS:
                if tok_upper not in needs_loaded and tok_upper not in needs_warned:
                    diags.append(make_diag(
                        'WARNING', lineno,
                        f'{tok_upper} used without NEEDS {tok_upper}'))
                    needs_warned.add(tok_upper)

    # End-of-file checks
    if not marker_found:
        if marker_checked:
            diags.append(make_diag(
                'ERROR', 1,
                'MARKER NEWTASK missing or not the first non-comment/non-blank line'))
        else:
            diags.append(make_diag('ERROR', 1, 'MARKER NEWTASK not found in file'))

    if in_colon:
        diags.append(make_diag(
            'ERROR', colon_start_line,
            f'colon definition opened on line {colon_start_line} never closed with ;'))

    # Filter out diagnostics on suppressed lines (\ lint: ok)
    diags = [d for d in diags if d[1] not in suppressed]

    return diags


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def fix_tabs(path):
    """Replace every TAB (0x09) with a single SPACE (0x20) in-place."""
    with open(path, 'rb') as fh:
        raw = fh.read()
    if b'\x09' not in raw:
        return False
    fixed = raw.replace(b'\x09', b'\x20')
    with open(path, 'wb') as fh:
        fh.write(fixed)
    return True


def main():
    strict = '--strict' in sys.argv
    fix    = '--fix'    in sys.argv
    args   = [a for a in sys.argv[1:] if not a.startswith('--')]

    # Locate repo root: this script lives in tools/, one level below repo root.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root  = os.path.dirname(script_dir)

    if args:
        files = args
    else:
        pattern = os.path.join(repo_root, 'tutorial', '*.f')
        files   = sorted(glob.glob(pattern))
        if not files:
            print(f'No tutorial/*.f files found under {repo_root}')
            sys.exit(0)

    total         = 0
    ok_count      = 0
    error_files   = 0
    warning_files = 0

    for fpath in files:
        total += 1
        if fix and fix_tabs(fpath):
            try:
                rel_fix = os.path.relpath(fpath, repo_root)
            except ValueError:
                rel_fix = fpath
            print(f'FIXED:  {rel_fix}  (TAB -> SPACE)')
        diags  = lint_file(fpath)

        try:
            rel = os.path.relpath(fpath, repo_root)
        except ValueError:
            rel = fpath

        errors   = [d for d in diags if d[0] == 'ERROR']
        warnings = [d for d in diags if d[0] == 'WARNING']

        has_error = bool(errors) or (strict and bool(warnings))

        print(f'FILE: {rel}')
        if diags:
            for level, lineno, msg in sorted(diags, key=lambda d: d[1]):
                print(f'  {level:<7} line {lineno:<5} : {msg}')
        else:
            print('  OK')

        if has_error:
            error_files += 1
        elif warnings:
            warning_files += 1
        else:
            ok_count += 1

    print()
    print(f'--- {total} files checked: {ok_count} OK, '
          f'{error_files} errors, {warning_files} warnings ---')

    sys.exit(1 if error_files > 0 else 0)


if __name__ == '__main__':
    main()
