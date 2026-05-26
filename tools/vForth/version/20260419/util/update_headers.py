#!/usr/bin/env python3
r"""
update_headers.py - Update vForth .f file headers in-place.

Replaces:
  \ v-Forth 1.8 - NextZXOS version - build <any-date>
  \ MIT License (c) 1990-<any-year> Matteo Vitturi

With:
  \ v-Forth 1.8 - NextZXOS version - build <NEW_BUILD>
  \ MIT License (c) 1990-<NEW_YEAR> Matteo Vitturi

Trailing whitespace on each line is preserved.
Files whose path contains a /version/ component are silently skipped
(they are historical snapshots and should not be modified).
Files whose path contains a /version/ component are silently skipped
(they are historical snapshots and should not be modified).

Usage:
  python3 update_headers.py [options] <directory>

Options:
  -b, --build  DATE   New build date  (default: 2026-04-15)
  -y, --year   YEAR   New copyright year (default: 2026)
  -n, --dry-run       Show what would change, do not write
  -v, --verbose       Print every matched line
  -h, --help          Show this help

Examples:
  python3 update_headers.py ../tools/vForth
  python3 update_headers.py --dry-run ../tools/vForth
  python3 update_headers.py -b 2026-06-01 -y 2026 ../tools/vForth
"""

import re
import os
import sys
import argparse

# -- regex patterns -------------------------------------------------------------

# Matches:  \ v-Forth 1.8 - NextZXOS version - build YYYY-MM-DD<trailing>
BUILD_RE = re.compile(
    r'(\\\ v-Forth 1\.8 - NextZXOS version - build )'
    r'(\d{4}-\d{2}-\d{2})'
    r'([ \t]*$)',
    re.MULTILINE
)

# Matches:  \ MIT License (c) 1990-YYYY Matteo Vitturi<trailing>
MIT_RE = re.compile(
    r'(\\\ MIT License \(c\) 1990-)'
    r'(\d{4})'
    r'( Matteo Vitturi)'
    r'([ \t]*$)',
    re.MULTILINE
)

# -- core logic -----------------------------------------------------------------

def process_file(path, new_build, new_year, dry_run, verbose):
    """Return True if the file was (or would be) modified."""
    try:
        with open(path, 'r', errors='replace') as fh:
            original = fh.read()
    except OSError as e:
        print(f"  WARNING: cannot read {path}: {e}", file=sys.stderr)
        return False

    changes = []

    def replace_build(m):
        old = m.group(2)
        if old == new_build:
            return m.group(0)
        changes.append(('build', old, new_build, m.start()))
        return m.group(1) + new_build + m.group(3)

    def replace_mit(m):
        old = m.group(2)
        if old == new_year:
            return m.group(0)
        changes.append(('year', old, new_year, m.start()))
        return m.group(1) + new_year + m.group(3) + m.group(4)

    updated = BUILD_RE.sub(replace_build, original)
    updated = MIT_RE.sub(replace_mit, updated)

    if not changes:
        return False

    rel = os.path.relpath(path)
    if verbose or dry_run:
        for kind, old_val, new_val, pos in changes:
            tag = '[DRY]' if dry_run else '     '
            print(f"  {tag} {rel}  {kind}: {old_val!r} -> {new_val!r}")
    else:
        print(f"  updated  {rel}")

    if not dry_run:
        try:
            with open(path, 'w') as fh:
                fh.write(updated)
        except OSError as e:
            print(f"  ERROR: cannot write {path}: {e}", file=sys.stderr)
            return False

    return True


def is_version_path(path):
    """Return True if any component of path is exactly 'version'."""
    return bool(re.search(r'(?:^|[/\\])version(?:[/\\]|$)', path))


def run(root, new_build, new_year, dry_run, verbose):
    total = modified = skipped = 0
    for dirpath, _, filenames in os.walk(root):
        for fn in sorted(filenames):
            if not fn.endswith('.f'):
                continue
            path = os.path.join(dirpath, fn)
            if is_version_path(path):
                skipped += 1
                if verbose:
                    print(f"  [SKIP] {os.path.relpath(path)}")
                continue
            total += 1
            if process_file(path, new_build, new_year, dry_run, verbose):
                modified += 1

    label = 'would update' if dry_run else 'updated'
    suffix = f"  ({skipped} skipped - version path)" if skipped else ""
    print(f"\n{label} {modified} of {total} .f files{suffix}.")


# -- CLI ------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Update vForth .f file headers in-place.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('directory',
                        help='Root directory to scan recursively')
    parser.add_argument('-b', '--build', default='2026-04-15',
                        metavar='DATE',
                        help='New build date, e.g. 2026-04-15 (default: %(default)s)')
    parser.add_argument('-y', '--year', default='2026',
                        metavar='YEAR',
                        help='New copyright year, e.g. 2026 (default: %(default)s)')
    parser.add_argument('-n', '--dry-run', action='store_true',
                        help='Show changes without writing files')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print every matched substitution')
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory!r} is not a directory.", file=sys.stderr)
        sys.exit(1)

    mode = 'DRY RUN' if args.dry_run else 'UPDATING'
    print(f"{mode}: build -> {args.build}, year -> {args.year}")
    print(f"Scanning: {os.path.abspath(args.directory)}\n")

    run(args.directory, args.build, args.year, args.dry_run, args.verbose)


if __name__ == '__main__':
    main()
