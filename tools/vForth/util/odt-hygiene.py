#!/usr/bin/env python3
"""
odt-hygiene.py -- report (and optionally remove) the Microsoft Word
bookmark residue that accumulates inside an OpenDocument text file.

Word marks every heading it puts in a Table Of Contents field with a
bookmark named _TocNNNNNNNN (and _HlkNNNNNNNN for hyperlinks).  When the
document is round-tripped through another application the field loses
track of its own anchors, so the next "update TOC" in Word lays down a
fresh set and leaves the previous one behind as ordinary user bookmarks.
Copy-pasting a section that already carries such a bookmark adds another
copy with a digit appended to the name.  Nothing ever removes them.

vForth1.8-core-en-20260817.odt had 18 such generations stacked on top of
each other: 18617 bookmarks, 883 KB, 30% of content.xml, for zero
typographic effect -- and every release inherited them, because each
build starts as a copy of the previous .odt.

The native ODF index anchors (__RefHeading__, __RefNumPara__) are
*replaced* on update rather than accumulated, and are never touched here.

Usage (from tools/vForth):

    python3 util/odt-hygiene.py doc/vForth1.8-core-en-20260817.odt
    python3 util/odt-hygiene.py --fix doc/vForth1.8-core-en-20260817.odt

Exit status: 0 clean (or successfully fixed), 1 residue found in report
mode, 2 error.  The report-mode status is what makes it usable as a
release gate.

--fix rewrites the file in place, keeping a <name>.bak alongside unless
--no-backup is given.  It only ever touches content.xml, it asserts that
the visible text comes out byte-identical, and it re-validates the
result before replacing the original.  Because the visible text and the
page layout do not change, an already exported .pdf stays valid.
"""
import argparse
import os
import re
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET

# self-closing bookmark tags only; the (?=[\s/>]) guard keeps
# <text:bookmark-ref>, which is a real cross-reference, out of the match
BOOKMARK_TAG = re.compile(r'<text:bookmark(?:-start|-end)?(?=[\s/>])[^>]*/>')
NAME_ATTR = re.compile(r'text:name="([^"]*)"')
WORD_NAME = re.compile(r'^_(?:Toc|Hlk)[0-9]+$')
TAGS = re.compile(r'<[^>]*>')

# Word's TOC counter is monotonic, so the leading digits date each
# generation; _Hlk names come from a different counter and are left out
# of the count, which is an estimate either way
GENERATION = re.compile(r'^_Toc([0-9]{4})')

REDUNDANT_SPAN = '<text:span text:style-name="Default_20_Paragraph_20_Font">'


def visible_text(xml):
    """The document text with every tag stripped -- the invariant of a fix."""
    return TAGS.sub('', xml)


def strip_word_bookmarks(content):
    """Return (cleaned_xml, [removed names])."""
    removed = []

    def drop(match):
        name = NAME_ATTR.search(match.group(0))
        if name and WORD_NAME.match(name.group(1)):
            removed.append(name.group(1))
            return ''
        return match.group(0)

    return BOOKMARK_TAG.sub(drop, content), removed


def survey(content):
    """Everything the report prints, gathered in one pass."""
    names = [m.group(1) for m in NAME_ATTR.finditer(content)]
    word = [n for n in names if WORD_NAME.match(n)]
    generations = {m.group(1) for m in (GENERATION.match(n) for n in word)
                   if m}
    text = visible_text(content)
    return {
        'content': len(content),
        'text': len(text),
        'ratio': len(content) / len(text) if text else 0.0,
        'word_bookmarks': len(word),
        'generations': len(generations),
        'native_anchors': sum(1 for n in names if n.startswith('__Ref')),
        'redundant_spans': content.count(REDUNDANT_SPAN),
    }


def report(path, s):
    print(path)
    print('  content.xml          : %9d byte' % s['content'])
    print('  testo visibile       : %9d byte  (rapporto %.1fx)'
          % (s['text'], s['ratio']))
    print('  segnalibri Word      : %9d  in ~%d generazioni'
          % (s['word_bookmarks'], s['generations']))
    print('  ancore ODF native    : %9d  (__Ref*, mai toccate)'
          % s['native_anchors'])
    print('  span ridondanti      : %9d  (residuo Word, non rimosso: '
          'tocca la formattazione)' % s['redundant_spans'])


def rewrite(src_path, dst_path, content):
    """Write a copy of src_path with content.xml replaced.

    Preserves entry order and metadata, and keeps 'mimetype' first,
    stored uncompressed and without extra field, as ODF requires.
    """
    data = content.encode('utf-8')
    with zipfile.ZipFile(src_path, 'r') as src:
        with zipfile.ZipFile(dst_path, 'w') as dst:
            for info in src.infolist():
                payload = (data if info.filename == 'content.xml'
                           else src.read(info.filename))
                out = zipfile.ZipInfo(info.filename, date_time=info.date_time)
                out.external_attr = info.external_attr
                out.internal_attr = info.internal_attr
                out.create_system = info.create_system
                out.compress_type = (zipfile.ZIP_STORED
                                     if info.filename == 'mimetype'
                                     else info.compress_type)
                dst.writestr(out, payload)


def validate(original, candidate):
    """Re-open the rewritten file and prove it is a sound ODF twin.

    Returns a list of failures; empty means the candidate can replace
    the original.
    """
    bad = []
    with zipfile.ZipFile(original) as a, zipfile.ZipFile(candidate) as b:
        if b.testzip() is not None:
            bad.append('archivio zip corrotto')
        names_a = [i.filename for i in a.infolist()]
        names_b = [i.filename for i in b.infolist()]
        if names_a != names_b:
            bad.append('elenco o ordine delle entry alterato')
        first = b.infolist()[0]
        if (first.filename != 'mimetype'
                or first.compress_type != zipfile.ZIP_STORED
                or first.extra):
            bad.append("'mimetype' non e' la prima entry STORED senza extra")
        for name in names_b:
            if name.endswith(('.xml', '.rdf')):
                blob = b.read(name)
                if not blob:
                    continue        # empty entries exist in the original too
                try:
                    ET.fromstring(blob)
                except ET.ParseError as exc:
                    bad.append('XML non valido in %s: %s' % (name, exc))
            if name != 'content.xml' and a.read(name) != b.read(name):
                bad.append('modificato un file diverso da content.xml: %s'
                           % name)
        ca = a.read('content.xml').decode('utf-8')
        cb = b.read('content.xml').decode('utf-8')
        if visible_text(ca) != visible_text(cb):
            bad.append('IL TESTO VISIBILE E CAMBIATO')
        for tag in ('<text:p', '<text:h ', '<text:span', '<table:table ',
                    '<draw:frame', '<text:table-of-content'):
            if ca.count(tag) != cb.count(tag):
                bad.append('conteggio %s cambiato: %d -> %d'
                           % (tag, ca.count(tag), cb.count(tag)))
        if survey(cb)['word_bookmarks']:
            bad.append('segnalibri Word ancora presenti')
    return bad


def lock_file(path):
    """The .~lock.<name># OpenOffice/LibreOffice drops beside an open file."""
    head, tail = os.path.split(os.path.abspath(path))
    return os.path.join(head, '.~lock.%s#' % tail)


def fix(path, keep_backup):
    lock = lock_file(path)
    if os.path.exists(lock):
        print('  APERTO IN OPENOFFICE/LIBREOFFICE (%s)'
              % os.path.basename(lock))
        print('  chiudi il documento e rilancia: sostituirlo adesso lo farebbe'
              ' sovrascrivere al primo salvataggio')
        return False

    with zipfile.ZipFile(path) as z:
        content = z.read('content.xml').decode('utf-8')
    cleaned, removed = strip_word_bookmarks(content)
    if not removed:
        print('  gia pulito, niente da fare')
        return True

    tmp = path + '.tmp'
    rewrite(path, tmp, cleaned)
    failures = validate(path, tmp)
    if failures:
        os.remove(tmp)
        print('  VALIDAZIONE FALLITA -- originale non toccato:')
        for f in failures:
            print('    X %s' % f)
        return False

    if keep_backup:
        shutil.copy2(path, path + '.bak')
        print('  backup               : %s.bak' % os.path.basename(path))
    os.replace(tmp, path)
    print('  rimossi              : %d segnalibri' % len(removed))
    print('  content.xml          : %d -> %d byte (-%.1f%%)'
          % (len(content), len(cleaned.encode('utf-8')),
             100.0 * (len(content) - len(cleaned)) / len(content)))
    print('  file                 : %d byte' % os.path.getsize(path))
    return True


def main():
    ap = argparse.ArgumentParser(
        description='Report or remove Word bookmark residue in .odt files.')
    ap.add_argument('odt', nargs='+', help='OpenDocument text file(s)')
    ap.add_argument('--fix', action='store_true',
                    help='rewrite the file in place (validated)')
    ap.add_argument('--no-backup', action='store_true',
                    help='with --fix, do not keep a .bak copy')
    args = ap.parse_args()

    dirty = False
    for path in args.odt:
        if not os.path.isfile(path):
            print('%s: non trovato' % path, file=sys.stderr)
            return 2
        try:
            with zipfile.ZipFile(path) as z:
                content = z.read('content.xml').decode('utf-8')
        except (zipfile.BadZipFile, KeyError) as exc:
            print('%s: non e un .odt leggibile (%s)' % (path, exc),
                  file=sys.stderr)
            return 2

        s = survey(content)
        report(path, s)
        if s['word_bookmarks']:
            if args.fix:
                if not fix(path, not args.no_backup):
                    return 2
            else:
                dirty = True
                print('  --> DA RIPULIRE: rilancia con --fix')
        else:
            print('  --> OK')
        print()

    return 1 if dirty else 0


if __name__ == '__main__':
    sys.exit(main())
