#!/usr/bin/env python3
"""Download the figures of the ZX Spectrum Next manual, 3rd edition.

doc/zx-spectrum-next-manual-3rd-ed.md links its figures as
    zx-spectrum-next-manual-3rd-ed-figures/FILE.png
and that folder is listed in .gitignore, so on a fresh clone (or on another
workstation) the pictures are missing. This script reads the links from the
manual and fetches each file from the online edition:
    https://explorer.specnext.dev/documentation/manual/rev3/figures/FILE.png

Usage:
    python util/fetch-next-manual-figures.py            missing files only
    python util/fetch-next-manual-figures.py --force    download all again
    python util/fetch-next-manual-figures.py --check    report only
    python util/fetch-next-manual-figures.py -o DIR     other destination

Exit status: 0 when every linked figure is present and is a valid PNG,
1 otherwise. Only the Python standard library is used.
"""

import argparse
import os
import re
import sys
import urllib.error
import urllib.request

BASE_URL = 'https://explorer.specnext.dev/documentation/manual/rev3/figures/'
FIG_DIR = 'zx-spectrum-next-manual-3rd-ed-figures'
MANUAL = 'zx-spectrum-next-manual-3rd-ed.md'
PNG_MAGIC = b'\x89PNG\r\n\x1a\n'

LINK = re.compile(r'!\[[^\]]*\]\(' + re.escape(FIG_DIR) + r'/([^)\s]+)\)')


def linked_figures(manual_path):
    """Return the sorted list of figure file names linked by the manual."""
    with open(manual_path, encoding='utf-8') as f:
        return sorted(set(LINK.findall(f.read())))


def is_png(path):
    try:
        with open(path, 'rb') as f:
            return f.read(len(PNG_MAGIC)) == PNG_MAGIC
    except OSError:
        return False


def fetch(name, dest):
    """Download one figure; return None on success or an error string."""
    req = urllib.request.Request(BASE_URL + name,
                                 headers={'User-Agent': 'vForth-doc-fetch'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except (urllib.error.URLError, OSError) as e:
        return str(e)
    if not data.startswith(PNG_MAGIC):
        return 'not a PNG (%d bytes)' % len(data)
    tmp = dest + '.part'
    with open(tmp, 'wb') as f:
        f.write(data)
    os.replace(tmp, dest)
    return None


def main():
    doc = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       os.pardir, 'doc')
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--force', action='store_true',
                    help='download every figure again')
    ap.add_argument('--check', action='store_true',
                    help='report missing or invalid files, download nothing')
    ap.add_argument('-o', '--out', default=os.path.join(doc, FIG_DIR),
                    help='destination folder (default: doc/%s)' % FIG_DIR)
    ap.add_argument('--manual', default=os.path.join(doc, MANUAL),
                    help='manual to read the links from')
    args = ap.parse_args()

    names = linked_figures(args.manual)
    if not names:
        print('no figure link found in', args.manual)
        return 1
    if not args.check:
        os.makedirs(args.out, exist_ok=True)

    done = kept = 0
    bad = []
    for name in names:
        dest = os.path.join(args.out, name)
        if is_png(dest) and not args.force:
            kept += 1
        elif args.check:
            bad.append((name, 'missing or not a PNG'))
        else:
            err = fetch(name, dest)
            if err:
                bad.append((name, err))
            else:
                done += 1
                print('  got', name)

    print('%d linked, %d already there, %d downloaded, %d failed'
          % (len(names), kept, done, len(bad)))
    for name, err in bad:
        print('  FAILED %s: %s' % (name, err))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
