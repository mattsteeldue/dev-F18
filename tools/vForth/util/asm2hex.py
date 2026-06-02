#!/usr/bin/env python3
"""
asm2hex.py -- Convert vForth ASSEMBLER vocabulary CODE definitions
              to raw hex C, literals suitable for inc/ release files.

Usage:
    python3 util/asm2hex.py  input.f           (stdout)
    python3 util/asm2hex.py  input.f -o out.f  (file)

Lines outside CODE...C; blocks pass through unchanged.
C; is replaced by SMUDGE.  NEXT becomes $DD C, $E9 C,.
Address-dependent operands (AA, consuming a Forth expression such as
' WORD >BODY, or HOLDPLACE/DISP,/BACK,) are preserved as-is.
Unrecognised patterns are passed through with a \\ WARN comment.

Case convention: mnemonics and register specifiers are lowercase in the
source (as per CLAUDE.md); this script accepts both cases.
"""

import sys, re, argparse

# --------------------------------------------------------------------------
# Register / flag encoding tables
# --------------------------------------------------------------------------

R8   = {'b|':0,'c|':1,'d|':2,'e|':3,'h|':4,'l|':5,'(hl)|':6,'a|':7}
R8D  = {"b'|":0,"c'|":1,"d'|":2,"e'|":3,"h'|":4,"l'|":5,"(hl)'|":6,"a'|":7}
R16  = {'bc|':0,'de|':1,'hl|':2,'sp|':3}
R16PP= {'bc|':0,'de|':1,'hl|':2,'af|':3}   # push / pop
FLAG = {'nz|':0,'z|':1,'nc|':2,'cy|':3,'po|':4,'pe|':5,'p|':6,'m|':7}
FJRP = {"nz'|":0x20,"z'|":0x28,"nc'|":0x30,"cy'|":0x38}
BIT  = {f'{n}|':n for n in range(8)}

# --------------------------------------------------------------------------
# Simple opcodes (no operands) -- mnemonic -> byte list
# --------------------------------------------------------------------------

SIMPLE = {
    'halt':[0x76],'nop':[0x00],'exx':[0xD9],'exafaf':[0x08],
    'exdehl':[0xEB],'ex(sp)hl':[0xE3],'ex(sp)iy':[0xFD,0xE3],
    'rla':[0x17],'rlca':[0x07],'rra':[0x1F],'rrca':[0x0F],
    'rld':[0xED,0x6F],'rrd':[0xED,0x67],
    'cpl':[0x2F],'daa':[0x27],'scf':[0x37],'ccf':[0x3F],
    'ei':[0xFB],'di':[0xF3],
    'ret':[0xC9],'reti':[0xED,0x4D],'retn':[0xED,0x45],'neg':[0xED,0x44],
    'ldi':[0xED,0xA0],'ldd':[0xED,0xA8],'ldir':[0xED,0xB0],'lddr':[0xED,0xB8],
    'cpi':[0xED,0xA1],'cpd':[0xED,0xA9],'cpir':[0xED,0xB1],'cpdr':[0xED,0xB9],
    'ini':[0xED,0xA2],'ind':[0xED,0xAA],'inir':[0xED,0xB2],'indr':[0xED,0xBA],
    'outi':[0xED,0xA3],'outd':[0xED,0xAB],'otir':[0xED,0xB3],'otdr':[0xED,0xBB],
    'ldsphl':[0xF9],'ldspix':[0xDD,0xF9],'ldspiy':[0xFD,0xF9],
    'jphl':[0xE9],'jpix':[0xDD,0xE9],'jpiy':[0xFD,0xE9],
    'next':[0xDD,0xE9],
    'ldia':[0xED,0x47],'ldai':[0xED,0x57],'ldra':[0xED,0x4F],'ldar':[0xED,0x5F],
    # Z80N
    'mul':[0xED,0x30],'swapnib':[0xED,0x23],'mirrora':[0xED,0x24],
    'setae':[0xED,0x95],'pixelad':[0xED,0x94],'pixeldn':[0xED,0x93],
    'outinb':[0xED,0x90],
    'addhl,a':[0xED,0x31],'addde,a':[0xED,0x32],'addbc,a':[0xED,0x33],
    'brlcde,b':[0xED,0x2C],'bslade,b':[0xED,0x2B],'bsrade,b':[0xED,0x28],
    'bsrfde,b':[0xED,0x29],'bsrlde,b':[0xED,0x2A],'jp(c)':[0xED,0x98],
    'ldix':[0xED,0xA4],'lddx':[0xED,0xAC],'ldirx':[0xED,0xB4],
    'lddrx':[0xED,0xBC],'ldpirx':[0xED,0xB7],'ldws':[0xED,0xA5],
}

# CB-prefixed bit/rotate/shift operations (r operand from R8)
CB_ROT  = {'rlc':0x00,'rrc':0x08,'rl':0x10,'rr':0x18,
           'sla':0x20,'sra':0x28,'sl1':0x30,'srl':0x38}

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def parse_num(s):
    s = s.strip()
    if s.startswith('$'):  return int(s[1:], 16)
    if s.startswith('%'):  return int(s[1:], 2)
    if s.startswith('#'):  return int(s[1:])
    return int(s)

def is_num(s):
    try: parse_num(s); return True
    except Exception: return False

def fmtb(b):
    return f'${b:02X} C,'

def emit_bytes(bs, indent='    ', comment=''):
    body = '  '.join(fmtb(b) for b in bs)
    line = indent + body
    if comment:
        line = line.ljust(36) + f'  \\ {comment}'
    return line

# --------------------------------------------------------------------------
# Per-instruction converters  (tokens already lowercased)
# --------------------------------------------------------------------------

def convert(tokens, raw_comment, indent):
    """Return a string (one or more lines) for the instruction, or None."""
    if not tokens:
        return ''

    t = tokens       # convenience alias
    t0 = t[0]

    # ---- Forth meta-words: pass through unchanged -------------------------
    if t0 in ('here','holdplace','back,','disp,','swap','constant',
              'smudge','c;'):
        # restore original case from raw_comment context -- just rejoin
        return indent + ' '.join(t) + (f'  \\ {raw_comment}' if raw_comment else '')

    # ---- NEXT (Forth inner interpreter = jp (ix)) -------------------------
    if t0 == 'next':
        return emit_bytes([0xDD, 0xE9], indent, raw_comment or 'jp (ix)')

    # ---- Simple opcodes (no operands) -------------------------------------
    if t0 in SIMPLE and len(t) == 1:
        return emit_bytes(SIMPLE[t0], indent, raw_comment or t0)

    # ---- push / pop -------------------------------------------------------
    if t0 in ('push', 'pop') and len(t) == 2:
        rr = t[1]
        base = 0xC5 if t0 == 'push' else 0xC1
        if rr in R16PP:
            return emit_bytes([base | (R16PP[rr] << 4)], indent,
                              raw_comment or f'{t0} {rr[:-1]}')
        pfx = {'ix|': 0xDD, 'iy|': 0xFD}.get(rr)
        if pfx:
            return emit_bytes([pfx, base | (2 << 4)], indent,
                              raw_comment or f'{t0} {rr[:-1]}')

    # ---- retf f| ----------------------------------------------------------
    if t0 == 'retf' and len(t) == 2:
        f = FLAG.get(t[1])
        if f is not None:
            return emit_bytes([0xC0 | (f << 3)], indent,
                              raw_comment or f'ret {t[1][:-1]}')

    # ---- Arithmetic / logic  r|  -----------------------------------------
    ARITH = {'adda':0x80,'adca':0x88,'suba':0x90,'sbca':0x98,
             'anda':0xA0,'xora':0xA8,'ora':0xB0,'cpa':0xB8}
    if t0 in ARITH and len(t) == 2:
        r = R8.get(t[1])
        if r is not None:
            return emit_bytes([ARITH[t0] | r], indent,
                              raw_comment or f'{t0[:-1]} {t[1][:-1]}')

    # ---- inc / dec  r'| ---------------------------------------------------
    if t0 in ('inc', 'dec') and len(t) == 2:
        r = R8D.get(t[1])
        if r is not None:
            op = (0x04 if t0 == 'inc' else 0x05) | (r << 3)
            return emit_bytes([op], indent,
                              raw_comment or f'{t0} {t[1][:-2]}')

    # ---- incx / decx  rr| ------------------------------------------------
    if t0 in ('incx', 'decx') and len(t) == 2:
        rr = t[1]
        base = 0x03 if t0 == 'incx' else 0x0B
        if rr in R16:
            return emit_bytes([base | (R16[rr] << 4)], indent,
                              raw_comment or f'{t0} {rr[:-1]}')
        pfx = {'ix|': 0xDD, 'iy|': 0xFD}.get(rr)
        if pfx:
            op = 0x23 if t0 == 'incx' else 0x2B
            return emit_bytes([pfx, op], indent,
                              raw_comment or f'{t0} {rr[:-1]}')

    # ---- addhl / adchl / sbchl  rr| --------------------------------------
    if t0 == 'addhl' and len(t) == 2:
        rr = t[1]
        if rr in R16:
            return emit_bytes([0x09 | (R16[rr] << 4)], indent,
                              raw_comment or f'add hl, {rr[:-1]}')
    if t0 == 'adchl' and len(t) == 2:
        rr = t[1]
        if rr in R16:
            return emit_bytes([0xED, 0x4A | (R16[rr] << 4)], indent,
                              raw_comment or f'adc hl, {rr[:-1]}')
    if t0 == 'sbchl' and len(t) == 2:
        rr = t[1]
        if rr in R16:
            return emit_bytes([0xED, 0x42 | (R16[rr] << 4)], indent,
                              raw_comment or f'sbc hl, {rr[:-1]}')

    # ---- addix / addiy  rr| ----------------------------------------------
    if t0 in ('addix', 'addiy') and len(t) == 2:
        pfx = 0xDD if t0 == 'addix' else 0xFD
        rr = t[1]
        rr_map = {'bc|':0,'de|':1,'ix|':2,'iy|':2,'sp|':3}
        r = rr_map.get(rr)
        if r is not None:
            return emit_bytes([pfx, 0x09 | (r << 4)], indent,
                              raw_comment or f'add {t0[3:]}, {rr[:-1]}')

    # ---- ld  r'|  r| -----------------------------------------------------
    if t0 == 'ld' and len(t) == 3:
        rd = R8D.get(t[1]); rs = R8.get(t[2])
        if rd is not None and rs is not None:
            return emit_bytes([0x40 | (rd << 3) | rs], indent,
                              raw_comment or f'ld {t[1][:-2]}, {t[2][:-1]}')

    # ---- ldn  r'|  n  N, -------------------------------------------------
    if t0 == 'ldn' and len(t) == 4 and t[3] == 'n,':
        rd = R8D.get(t[1])
        if rd is not None and is_num(t[2]):
            val = parse_num(t[2]) & 0xFF
            return emit_bytes([0x06 | (rd << 3), val], indent,
                              raw_comment or f'ld {t[1][:-2]}, {t[2]}')

    # ---- ldx  rr|  nn  NN, -----------------------------------------------
    if t0 == 'ldx' and len(t) == 4 and t[3] == 'nn,':
        rr = t[1]
        if rr in R16 and is_num(t[2]):
            nn = parse_num(t[2]) & 0xFFFF
            return emit_bytes([0x01 | (R16[rr] << 4),
                                nn & 0xFF, nn >> 8], indent,
                              raw_comment or f'ld {rr[:-1]}, {t[2]}')
        pfx = {'ix|': (0xDD, 0x21), 'iy|': (0xFD, 0x21)}.get(rr)
        if pfx and is_num(t[2]):
            nn = parse_num(t[2]) & 0xFFFF
            return emit_bytes([pfx[0], pfx[1],
                                nn & 0xFF, nn >> 8], indent,
                              raw_comment or f'ld {rr[:-1]}, {t[2]}')

    # ---- CB rotate / shift  r| -------------------------------------------
    if t0 in CB_ROT and len(t) == 2:
        r = R8.get(t[1])
        if r is not None:
            return emit_bytes([0xCB, CB_ROT[t0] | r], indent,
                              raw_comment or f'{t0} {t[1][:-1]}')

    # ---- bit / set / res  b|  r| -----------------------------------------
    if t0 in ('bit', 'set', 'res') and len(t) == 3:
        b = BIT.get(t[1]); r = R8.get(t[2])
        if b is not None and r is not None:
            base = {'bit':0x40,'set':0xC0,'res':0x80}[t0]
            return emit_bytes([0xCB, base | (b << 3) | r], indent,
                              raw_comment or f'{t0} {b}, {t[2][:-1]}')

    # ---- in(c) / out(c)  r'| ---------------------------------------------
    if t0 == 'in(c)' and len(t) == 2:
        r = R8D.get(t[1])
        if r is not None:
            return emit_bytes([0xED, 0x40 | (r << 3)], indent,
                              raw_comment or f'in {t[1][:-2]}, (c)')
    if t0 == 'out(c)' and len(t) == 2:
        r = R8D.get(t[1])
        if r is not None:
            return emit_bytes([0xED, 0x41 | (r << 3)], indent,
                              raw_comment or f'out (c), {t[1][:-2]}')

    # ---- ina / outa  n  P, -----------------------------------------------
    if t0 == 'ina' and len(t) == 3 and t[2] == 'p,' and is_num(t[1]):
        return emit_bytes([0xDB, parse_num(t[1]) & 0xFF], indent,
                          raw_comment or f'in a, ({t[1]})')
    if t0 == 'outa' and len(t) == 3 and t[2] == 'p,' and is_num(t[1]):
        return emit_bytes([0xD3, parse_num(t[1]) & 0xFF], indent,
                          raw_comment or f'out ({t[1]}), a')

    # ---- nextreg  r  P,  n  N, -------------------------------------------
    if t0 == 'nextreg' and len(t) == 5 and t[2] == 'p,' and t[4] == 'n,':
        if is_num(t[1]) and is_num(t[3]):
            return emit_bytes([0xED, 0x91,
                                parse_num(t[1]) & 0xFF,
                                parse_num(t[3]) & 0xFF], indent,
                              raw_comment or f'nextreg {t[1]}, {t[3]}')

    # ---- nextrega  r  P, -------------------------------------------------
    if t0 == 'nextrega' and len(t) == 3 and t[2] == 'p,':
        if is_num(t[1]):
            return emit_bytes([0xED, 0x92, parse_num(t[1]) & 0xFF], indent,
                              raw_comment or f'nextreg {t[1]}, a')

    # ---- Z80N  addhl,/addde,/addbc,  nn  NN, ----------------------------
    Z80N_ADD = {'addhl,': (0xED, 0x34),
                'addde,': (0xED, 0x35),
                'addbc,': (0xED, 0x36)}
    if t0 in Z80N_ADD and len(t) == 3 and t[2] == 'nn,' and is_num(t[1]):
        pfx, op = Z80N_ADD[t0]
        nn = parse_num(t[1]) & 0xFFFF
        return emit_bytes([pfx, op, nn & 0xFF, nn >> 8], indent,
                          raw_comment or f'{t0[:-1]} {t[1]}')

    # ---- djnz  d  D, (numeric displacement) ------------------------------
    if t0 == 'djnz' and len(t) == 3 and t[2] == 'd,' and is_num(t[1]):
        d = parse_num(t[1])
        if d < 0: d &= 0xFF
        return emit_bytes([0x10, d], indent,
                          raw_comment or f'djnz {t[1]}')

    # ---- jrf  f'|  HOLDPLACE  (forward conditional JR placeholder) -------
    if t0 == 'jrf' and len(t) == 3 and t[2] == 'holdplace':
        op = FJRP.get(t[1])
        if op is not None:
            line1 = emit_bytes([op], indent, raw_comment or f'jr {t[1][:-1]}, ?')
            line2 = indent + 'HOLDPLACE'
            return line1 + '\n' + line2

    # ---- jrf  f'|  d  D, (numeric displacement) --------------------------
    if t0 == 'jrf' and len(t) == 4 and t[3] == 'd,' and is_num(t[2]):
        op = FJRP.get(t[1])
        if op is not None:
            d = parse_num(t[2]); d = d & 0xFF if d < 0 else d
            return emit_bytes([op, d], indent,
                              raw_comment or f'jr {t[1][:-1]}, {t[2]}')

    # ---- jr  BACK, -------------------------------------------------------
    if t0 == 'jr' and len(t) == 2 and t[1] == 'back,':
        return (emit_bytes([0x18], indent, raw_comment or 'jr back')
                + '\n' + indent + 'BACK,')

    # ---- jr  d  D, (numeric) ---------------------------------------------
    if t0 == 'jr' and len(t) == 3 and t[2] == 'd,' and is_num(t[1]):
        d = parse_num(t[1]); d = d & 0xFF if d < 0 else d
        return emit_bytes([0x18, d], indent, raw_comment or f'jr {t[1]}')

    # ---- jp  AA,  (backward jump consuming HERE address from stack) ------
    if t0 == 'jp' and len(t) == 2 and t[1] == 'aa,':
        body = fmtb(0xC3) + '  ,'
        cmt  = ('  \\ ' + (raw_comment or 'jp addr'))
        return indent + body + cmt

    # ---- jpf  f|  AA,  (backward conditional jump, HERE on stack) --------
    if t0 == 'jpf' and len(t) == 3 and t[2] == 'aa,':
        f = FLAG.get(t[1])
        if f is not None:
            op   = 0xC2 | (f << 3)
            body = fmtb(op) + '  ,'
            cmt  = '  \\ ' + (raw_comment or f'jp {t[1][:-1]}, addr')
            return indent + body + cmt

    # ---- jpf  f|  <expr>  AA,  (labeled or forward jump) ----------------
    if t0 == 'jpf' and len(t) >= 4 and t[-1] == 'aa,':
        f = FLAG.get(t[1])
        if f is not None:
            op = 0xC2 | (f << 3)
            expr = ' '.join(t[2:-1])
            line1 = emit_bytes([op], indent,
                               raw_comment or f'jp {t[1][:-1]}, {expr}')
            line2 = indent + expr + '  AA,'
            return line1 + '\n' + line2

    # ---- jp  <expr>  AA, -------------------------------------------------
    if t0 == 'jp' and len(t) >= 3 and t[-1] == 'aa,':
        expr = ' '.join(t[1:-1])
        line1 = emit_bytes([0xC3], indent, raw_comment or f'jp {expr}')
        line2 = indent + expr + '  AA,'
        return line1 + '\n' + line2

    # ---- call  AA, -------------------------------------------------------
    if t0 == 'call' and len(t) == 2 and t[1] == 'aa,':
        body = fmtb(0xCD) + '  ,'
        return indent + body + '  \\ ' + (raw_comment or 'call addr')

    # ---- call  <expr>  AA, -----------------------------------------------
    if t0 == 'call' and len(t) >= 3 and t[-1] == 'aa,':
        expr = ' '.join(t[1:-1])
        line1 = emit_bytes([0xCD], indent, raw_comment or f'call {expr}')
        line2 = indent + expr + '  AA,'
        return line1 + '\n' + line2

    # ---- callf  f|  <expr>  AA, -----------------------------------------
    if t0 == 'callf' and len(t) >= 4 and t[-1] == 'aa,':
        f = FLAG.get(t[1])
        if f is not None:
            op = 0xC4 | (f << 3)
            expr = ' '.join(t[2:-1])
            line1 = emit_bytes([op], indent,
                               raw_comment or f'call {t[1][:-1]}, {expr}')
            line2 = indent + expr + '  AA,'
            return line1 + '\n' + line2

    # ---- lda(x) / ld(x)a  rr| (Z80 ld a,(rr) / ld (rr),a) --------------
    if t0 == 'lda(x)' and len(t) == 2:
        ops = {'bc|': [0x0A], 'de|': [0x1A]}
        if t[1] in ops:
            return emit_bytes(ops[t[1]], indent,
                              raw_comment or f'ld a, ({t[1][:-1]})')
    if t0 == 'ld(x)a' and len(t) == 2:
        ops = {'bc|': [0x02], 'de|': [0x12]}
        if t[1] in ops:
            return emit_bytes(ops[t[1]], indent,
                              raw_comment or f'ld ({t[1][:-1]}), a')

    # ---- addn / subn / cpn / andn / xorn / orn  n  N, -------------------
    IMM8 = {'addn':0xC6,'adcn':0xCE,'subn':0xD6,'sbcn':0xDE,
            'andn':0xE6,'xorn':0xEE,'orn':0xF6,'cpn':0xFE}
    if t0 in IMM8 and len(t) == 3 and t[2] == 'n,' and is_num(t[1]):
        return emit_bytes([IMM8[t0], parse_num(t[1]) & 0xFF], indent,
                          raw_comment or f'{t0[:-1]} {t[1]}')

    # ---- rst  a| ---------------------------------------------------------
    if t0 == 'rst' and len(t) == 2:
        RST = {'00|':0,'08|':1,'10|':2,'18|':3,
               '20|':4,'28|':5,'30|':6,'38|':7}
        idx = RST.get(t[1])
        if idx is not None:
            return emit_bytes([0xC7 | (idx << 3)], indent,
                              raw_comment or f'rst {t[1][:-1]}')

    # ---- pushn  nn  LH, (Z80N PUSH nn) ----------------------------------
    if t0 == 'pushn' and len(t) == 3 and t[2] == 'lh,' and is_num(t[1]):
        nn = parse_num(t[1]) & 0xFFFF
        hi, lo = nn >> 8, nn & 0xFF
        return emit_bytes([0xED, 0x8A, hi, lo], indent,
                          raw_comment or f'push {t[1]}')

    # ---- Fallback: preserve the original line with a warning -------------
    original = ' '.join(t)
    warn = f'WARN: not converted -- {raw_comment}' if raw_comment else 'WARN: not converted'
    return indent + original + f'  \\ {warn}'


# --------------------------------------------------------------------------
# Source-file processor
# --------------------------------------------------------------------------

def leading_indent(line):
    m = re.match(r'^(\s*)', line)
    return m.group(1)

def tokenize_line(line):
    """Return (tokens_lower, raw_comment, indent) from a source line."""
    indent = leading_indent(line)
    # split comment
    body, _, comment = line.partition('\\')
    tokens = body.split()
    return [t.lower() for t in tokens], comment.strip(), indent

def process_file(lines):
    out = []
    in_code = False
    code_header = ''

    for raw_line in lines:
        line = raw_line.rstrip('\n')
        tokens_lo, comment, indent = tokenize_line(line)

        if not in_code:
            # Look for CODE word start (case-insensitive)
            if tokens_lo and tokens_lo[0] == 'code':
                in_code = True
                code_header = line
                out.append(line)    # pass CODE name line unchanged
                continue
            out.append(line)
            continue

        # Inside CODE block -------------------------------------------------
        if not tokens_lo:
            out.append(line)        # blank / comment-only lines preserved
            continue

        t0 = tokens_lo[0]

        # End of CODE block
        if t0 == 'c;':
            out.append(indent + 'SMUDGE')
            in_code = False
            continue

        # NEXT: already handled as a simple opcode (next -> DD E9)
        # HERE, HOLDPLACE, BACK,, DISP,, SWAP, CONSTANT: pass through
        PASSTHRU = {'here','holdplace','back,','disp,','swap','constant'}
        if t0 in PASSTHRU or (tokens_lo and tokens_lo[-1] in PASSTHRU):
            out.append(line)
            continue

        # Try to convert
        result = convert(tokens_lo, comment, indent)
        if result is not None:
            out.append(result)
        else:
            out.append(line + '  \\ WARN: unconverted')

    return out

# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
             formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input', help='source .f file with ASSEMBLER CODE blocks')
    ap.add_argument('-o', '--output', help='output file (default: stdout)')
    args = ap.parse_args()

    with open(args.input, 'r', encoding='ascii', errors='replace') as f:
        lines = f.readlines()

    result = process_file(lines)

    out_text = '\n'.join(result) + '\n'
    if args.output:
        with open(args.output, 'w', encoding='ascii') as f:
            f.write(out_text)
    else:
        sys.stdout.write(out_text)

if __name__ == '__main__':
    main()
