"""Convert a pdftotext dump of the ZX Spectrum Next manual to Markdown.

Usage:
    util/pdftotext.bat "<manual>.pdf"          (writes <manual>.txt)
    python util/txt2md.py <manual>.txt <manual>.md

Tuned on "ZX Spectrum Next Manual 3rd Ed A4 OCR.pdf" (318 pages): running
headers "Chapter N - Title" / "Appendix X - Title", footer "ZX Spectrum
Next - User Manual", printed page number equal to the PDF page number,
back matter (TAIL_TITLES) from page 307 on. Other books need those
constants and the SHORT_OK list revised.

Output: '#' per chapter/appendix, '##' per section (taken from the running
headers and from the book's own table of contents), '<!-- page N -->' at
each page start, prose re-joined into one line per paragraph, UTF-8.
"""
import difflib
import re
import sys
from collections import Counter, defaultdict

LONG = 70          # a line at least this long is a wrapped prose line
# short running titles the damaged TOC cannot confirm (checked by hand)
SHORT_OK = {'ELSE', 'LN', 'DIM', 'INKEY$', 'Tiling', 'TIME$', 'CP/M',
            'Windows'}
TAIL_TITLES = {
    'acknowledgements': 'Acknowledgements',
    'table of contents': 'Table of Contents',
    'index': 'Index',
    'zx spectrum next home computer - specifications':
        'ZX Spectrum Next Home Computer - Specifications',
}

RE_CHAP = re.compile(
    r'^(Chapter\s+\d+|Appendix\s+[A-D])\s*[\u2014\u2013-]+\s*(\S.*)$')
RE_APP_ALONE = re.compile(r'^Appendix\s+([A-D])$')
RE_FOOTER = re.compile(
    r'^ZX\s+S\w+\s+Next\s*[\u2014\u2013-]+\s*User\s+Manua\w*$', re.I)


def norm_key(s):
    return re.sub(r'\s+', ' ', s).strip()


def squash(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


def escape(line):
    line = line.replace('\\', '\\\\')
    line = re.sub(r'([*_`<~])', r'\\\1', line)
    if re.match(r'^[=-]+\s*$', line) or line[:1] in '#>+':
        line = '\\' + line
    elif re.match(r'^-\s', line):
        line = '\\' + line
    else:
        line = re.sub(r'^(\d+)([.)])(\s|$)', r'\1\\\2\3', line)
    return line


def main(src, dst):
    text = open(src, encoding='utf-8').read().replace('\r\n', '\n')
    pages = text.split('\f')
    if pages and not pages[-1].strip():
        pages.pop()

    # ---- pass 1: strip running headers/footers, collect titles ----------
    body = []                    # per page: list of lines
    chap_of = []                 # per page: chapter key or None
    sect_of = []                 # per page: running section title or None
    chap_titles = defaultdict(Counter)
    first_page = {}              # chapter key -> first page index
    tail_of = []                 # per page: tail title key or None

    for idx, page in enumerate(pages):
        num = str(idx + 1)
        lines = [l.rstrip() for l in page.split('\n')]
        nb = [i for i, l in enumerate(lines) if l.strip()]
        drop = set()
        chap = sect = tail = None

        # footer / page number
        for i in nb:
            if RE_FOOTER.match(lines[i].strip()):
                drop.add(i)
        for i in nb[:4] + nb[-4:]:
            if lines[i].strip() == num:
                drop.add(i)

        head = [i for i in nb if i not in drop][:4]
        chap_i = None
        for i in head:
            m = RE_CHAP.match(lines[i].strip()) if idx < 306 else None
            if m:
                chap_i = i
                chap = norm_key(m.group(1))
                chap_titles[chap][norm_key(m.group(2))] += 1
                break
        if chap_i is not None:
            drop.add(chap_i)
            if chap in first_page:
                # the other of the first two lines is the running section
                others = [i for i in head[:2] if i != chap_i]
                if head.index(chap_i) >= 2:
                    others = [head[0]]
                    drop.update(head[1:head.index(chap_i)])   # OCR junk
                if others:
                    cand = lines[others[0]].strip()
                    if len(cand) < 60:
                        sect = norm_key(cand)
                        drop.add(others[0])
            else:
                first_page[chap] = idx
        elif head:
            first = lines[head[0]].strip()
            m = RE_APP_ALONE.match(first)
            if m:
                chap = 'Appendix ' + m.group(1)
                first_page.setdefault(chap, idx)
                drop.add(head[0])
            elif idx >= 300 and first.lower() in TAIL_TITLES:
                tail = first.lower()
                drop.add(head[0])
                # the title is often printed twice on the first page
                if len(head) > 1 and \
                        lines[head[1]].strip().lower() == tail:
                    drop.add(head[1])

        body.append([l for i, l in enumerate(lines) if i not in drop])
        chap_of.append(chap)
        sect_of.append(sect)
        tail_of.append(tail)

    canon = {k: max(c, key=lambda t: (c[t], len(t))).replace('Z30N', 'Z80N')
             for k, c in chap_titles.items()}
    for k, c in chap_titles.items():
        if len(c) > 1:
            print('title variants', k, dict(c))

    # appendix title pages: drop the split title lines after "Appendix X"
    for chap, idx in first_page.items():
        if not chap.startswith('Appendix') or chap not in canon:
            continue
        target = squash(canon[chap])
        lines = body[idx]
        acc = ''
        kill = []
        for i, l in enumerate(lines):
            if not l.strip():
                continue
            acc2 = acc + squash(l)
            if target.startswith(acc2) or len(acc2) <= len(target) and \
                    sum(a != b for a, b in zip(acc2, target)) <= 2:
                acc = acc2
                kill.append(i)
                if len(acc) >= len(target):
                    break
            else:
                break
        body[idx] = [l for i, l in enumerate(lines) if i not in kill]

    # ---- section headings: one per run of pages with the same title -----
    heading_at = {}              # (page, line index) -> title
    runs = []
    for idx, s in enumerate(sect_of):
        if not s:
            continue
        if runs and runs[-1][0] == s and idx - runs[-1][2] <= 2 \
                and chap_of[idx] == chap_of[runs[-1][1]]:
            runs[-1][2] = idx
        else:
            runs.append([s, idx, idx])
    for s, a, b in runs:
        lo = a - 1 if a > 0 and chap_of[a - 1] == chap_of[a] else a
        found = False
        tests = [lambda l: norm_key(l) == s,
                 lambda l: squash(l) == squash(s)]
        if len(squash(s)) >= 8:
            tests.append(lambda l: len(l) < 70 and difflib.SequenceMatcher(
                None, squash(l), squash(s)).ratio() >= 0.85)
        for test in tests:
            for p in range(lo, b + 1):
                for i, l in enumerate(body[p]):
                    if l.strip() and test(l) and (p, i) not in heading_at:
                        heading_at[(p, i)] = s
                        found = True
                        break
                if found:
                    break
            if found:
                break

    # ---- more section headings from the (OCR-damaged) table of contents --
    toc = set()
    toc_all = set()
    for idx, t in enumerate(tail_of):
        if idx < 306:
            continue
        if any(tail_of[k] == 'table of contents'
               for k in range(idx, 305, -1)) and                 not any(tail_of[k] == 'index' for k in range(306, idx + 1)):
            for l in body[idx]:
                for frag in re.split(r'\.\s*\.[.\s]*|\s\d+\s|[:;{]', l):
                    frag = re.sub(r'[\s\d.]+$', '', frag)
                    frag = re.sub(r'^[\s\d.]+', '', frag)
                    toc_all.add(squash(frag))
                    if len(squash(frag)) >= 8 and \
                            not frag.startswith(('Chapter', 'Appendix')):
                        toc.add(squash(frag))
    print('toc titles', len(toc))
    used = set(squash(v) + '@' + str(chap_of[p])
               for (p, i), v in heading_at.items())
    cur = None
    for p in range(len(body)):
        if p >= 306:
            break
        cur = chap_of[p] or cur
        if cur is None:
            continue
        nbl = [i for i, l in enumerate(body[p]) if l.strip()]
        for n_, i in enumerate(nbl):
            l = body[p][i].strip()
            if (p, i) in heading_at or len(l) >= 70 or l[-1] in '.,;':
                continue
            key = squash(l) + '@' + cur
            opening = (n_ == 0 and first_page.get(cur) == p and len(l) < 60
                       and l[:1].isupper() and len(squash(l)) >= 5
                       and (i + 1 >= len(body[p])
                            or not body[p][i + 1].strip()))
            if (squash(l) in toc or opening) and key not in used:
                used.add(key)
                heading_at[(p, i)] = norm_key(l)

    # ---- discard headings that are OCR junk ------------------------------
    cur = None
    chap_at = []
    for p in range(len(body)):
        cur = chap_of[p] or cur
        chap_at.append(cur)
    for (p, i), v in sorted(heading_at.items()):
        q = squash(v)
        ok = (chap_at[p] != 'Appendix A' and v[:1].isupper()
              and (len(q) >= 8 or q in toc_all or v in SHORT_OK)
              and not squash(canon.get(chap_at[p], '')).endswith(q))
        if not ok:
            print('rejected heading p%d: %r' % (p + 1, v))
            del heading_at[(p, i)]

    # ---- pass 2: emit ----------------------------------------------------
    out = []
    out.append('# ZX Spectrum Next \u2014 User Manual (Third Edition)')
    out.append('')
    out.append('> Markdown conversion of *ZX Spectrum Next Manual 3rd Ed A4 '
               'OCR.pdf* (318 pages), text extracted with poppler '
               '`pdftotext`. The source is an OCR scan: program listings, '
               'tables and figures are only approximately rendered. '
               '`<!-- page N -->` marks the start of each PDF page.')
    out.append('')
    out.append('## Contents')
    out.append('')
    for chap, idx in sorted(first_page.items(), key=lambda kv: kv[1]):
        title = canon.get(chap, '')
        sep = ' \u2014 ' if title else ''
        out.append('- %s%s%s (page %d)' % (chap, sep, title, idx + 1))
    seen_tail = set()
    for idx, t in enumerate(tail_of):
        if t and t not in seen_tail:
            seen_tail.add(t)
            out.append('- %s (page %d)' % (TAIL_TITLES[t], idx + 1))
    out.append('')

    seen_tail = set()
    stats = Counter()
    for idx, lines in enumerate(body):
        out.append('<!-- page %d -->' % (idx + 1))
        out.append('')
        chap = chap_of[idx]
        if chap and first_page.get(chap) == idx:
            title = canon.get(chap, '')
            sep = ' \u2014 ' if title else ''
            out.append('# %s%s%s' % (chap, sep, title))
            out.append('')
            stats['chapters'] += 1
        t = tail_of[idx]
        if t and t not in seen_tail:
            seen_tail.add(t)
            out.append('# ' + TAIL_TITLES[t])
            out.append('')

        para = []            # list of physical lines of current paragraph
        reflow = 4 <= idx < 306

        def flush():
            if not para:
                return
            buf = ''
            for k, l in enumerate(para):
                if k == 0:
                    buf = escape(l)
                elif reflow and len(para[k - 1]) >= LONG:
                    buf += ' ' + l.replace('\\', '\\\\')
                    buf = buf  # joined prose: escape below
                else:
                    buf += '  \n' + escape(l)
            out.append(buf)
            out.append('')
            para.clear()

        n = len(lines)
        i = 0
        while i < n:
            l = lines[i].strip()
            if (idx, i) in heading_at:
                flush()
                out.append('## ' + heading_at[(idx, i)])
                out.append('')
                stats['sections'] += 1
            elif not l:
                # a blank inside a wrapped sentence does not end it
                j = i + 1
                while j < n and not lines[j].strip():
                    j += 1
                cont = (reflow and para and len(para[-1]) >= LONG
                        and para[-1][-1] not in '.!?:;'
                        and j < n and lines[j].strip()[:1].islower()
                        and (idx, j) not in heading_at)
                if not cont:
                    flush()
                i = j - 1
            else:
                para.append(l)
            i += 1
        flush()

    text = '\n'.join(out)
    text = re.sub(r'\n{3,}', '\n\n', text).rstrip('\n') + '\n'
    open(dst, 'w', encoding='utf-8', newline='\n').write(text)
    print('pages', len(pages), dict(stats), 'runs', len(runs),
          'bytes', len(text.encode('utf-8')))
    missed = [(s, a + 1) for s, a, b in runs
              if s not in heading_at.values()]
    print('section titles never found in body:', len(missed))
    for m in missed[:40]:
        print('   ', m)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
