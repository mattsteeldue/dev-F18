#!/usr/bin/env python
"""cmp-f18e.py -- coerenza tra src/F18e.f e il core assemblato (DOES).

Confronta il binario prodotto compilando src/F18e.f UNA sola volta (SAVE da
CSpect, oppure un dump) con forth18e.bin + ram8.bin generati dal progetto
project/vForth18_DOES/, tenendo conto degli indirizzi spostati:

  * codice: tutti gli indirizzi sono spostati della stessa costante
        T = ORG_NUOVO - $6366
  * heap:   i puntatori nell'heap sono spostati di uno scarto che cresce a
        scalini (definizioni ausiliarie del sorgente, salto di pagina 8K
        dovuto a PAGE-WATERMARK); lo scarto e' letto dal mirror-pointer
        che precede il CFA di ogni parola.

I confini delle parole vengono dall'heap del riferimento (ram8.bin), letto
come catena di voci [len|$80][nome][link][xt].

Uso:   python util/cmp-f18e.py forth18_.bin [--log out.log] [--org HEX]
Uscita: 0 coerente, 1 differenze non spiegate, 2 errore d'uso/dati.
File ASCII a 7 bit.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFDIR = os.path.join(ROOT, 'project', 'vForth18_DOES', 'output')
ORG_REF = 0x6366


def die(msg):
    print("ERRORE: " + msg)
    sys.exit(2)


args = sys.argv[1:]
if not args or args[0].startswith('--'):
    die("uso: cmp-f18e.py candidato.bin [--log file] [--org HEX]")
cand_path = args[0]
log_path = args[args.index('--log') + 1] if '--log' in args else None
org_opt = int(args[args.index('--org') + 1], 16) if '--org' in args else None

out = []


def P(s=''):
    out.append(s)


ref_full = open(os.path.join(REFDIR, 'forth18e.bin'), 'rb').read()
heap = open(os.path.join(REFDIR, 'ram8.bin'), 'rb').read()
raw = open(cand_path, 'rb').read()

if raw[:8] == b'PLUS3DOS':                   # SAVE da BASIC: header di 128 byte
    org = raw[18] | raw[19] << 8              # indirizzo di caricamento
    cand = raw[128:]
else:
    if org_opt is None:
        die("file senza header PLUS3DOS: indicare l'origine con --org HEX")
    org, cand = org_opt, raw

REF_LEN = max(i for i in range(len(ref_full)) if ref_full[i]) + 1

# Un SAVE partito da un indirizzo sbagliato di pochi byte sfasa tutto e darebbe
# un falso disastro: si cerca lo scostamento con piu' byte uguali al riferimento.
scores = {}
for s in range(-8, 9):
    d = cand[s:] if s >= 0 else bytes(-s) + cand
    scores[s] = sum(1 for i in range(min(len(d), REF_LEN)) if d[i] == ref_full[i])
best = max(scores, key=scores.get)
if best != 0 and scores[best] > 3 * scores[0]:
    print("ATTENZIONE: i dati risultano sfasati di %+d byte rispetto all'origine "
          "dichiarata ($%04X): probabile errore di battitura nell'indirizzo del "
          "SAVE. Uso $%04X." % (best, org, org + best))
    print("            Al prossimo salvataggio: SAVE \"nome.bin\" CODE %d,%d"
          % (org + best, REF_LEN))
    print()
    cand = cand[best:] if best >= 0 else bytes(-best) + cand
    org += best

N = min(len(cand), REF_LEN)                   # oltre REF_LEN ci sono residui
ref = ref_full[:N]
cand = cand[:N]
T = org - ORG_REF


def rd(buf, a):
    return buf[a] | buf[a + 1] << 8


# --- parole del riferimento: scansione dell'heap validata dalla catena dei link
words = []
p, prev = 2, None
while p < len(heap) - 8:
    b = heap[p]
    if b & 0x80:
        ln = b & 0x1F
        q = p + 1 + ln
        name = heap[p + 1:q]
        ok = ln and name[-1] & 0x80 and all(
            32 <= (c & 0x7F) < 127 or (ln == 1 and c == 0x80) for c in name)
        if ok:
            link, xt = rd(heap, q), rd(heap, q + 2)
            if ORG_REF <= xt < ORG_REF + REF_LEN and (prev is None or link == prev):
                nm = '<NUL>' if name == bytes([0x80]) else ''.join(
                    chr(c & 0x7F) for c in name)
                words.append((nm, xt))
                prev = p
                p = q + 4
                continue
    p += 1

words = [w for w in words if w[0] and w[1] - 2 - ORG_REF < N]
words.sort(key=lambda w: w[1])
if not words:
    die("nessuna parola trovata nel riferimento")
first_mirror = words[0][1] - 2 - ORG_REF
last_m = words[-1][1] - 2 - ORG_REF
DH_FINAL = (rd(cand, last_m) - rd(ref, last_m)) & 0xFFFF

# --- differenze note e attese (offset dal riferimento -> motivo)
EXPECTED = {}
for o in (0x08, 0x09):
    EXPECTED[o] = 'ORIGIN+008 saved Basic SP: dipende dall ambiente di compilazione'
for o in (0x30, 0x31):
    EXPECTED[o] = 'ORIGIN+030 Return Stack Pointer: dipende dall ambiente (R0)'
for nm_, xt_ in words:
    if nm_ == 'AUTOEXEC':
        # CALL Enter_Ptr (3 byte) + dw LIT (2 byte) + valore: 10 sopra $8000, 11 sotto
        EXPECTED[xt_ - ORG_REF + 3 + 2] = (
            'AUTOEXEC: 10 0 +origin 32768 u< 1 and + vale 11 sotto $8000, 10 sopra')

P("Candidato : %s" % cand_path)
P("Origine   : $%04X  (riferimento $%04X)  spostamento codice T = +$%04X"
  % (org, ORG_REF, T))
P("Lunghezza : %d byte confrontati su %d del riferimento%s"
  % (N, REF_LEN, '' if N == REF_LEN else '   ** COPERTURA PARZIALE **'))
P("Parole    : %d nel riferimento" % len(words))
P("Scarto finale dell heap (LATEST/HP): $%04X" % DH_FINAL)
P()


def compare(a0, a1, dh):
    """ref[a0:a1] contro cand[a0:a1]: (uguali, rilocati, offset diversi)."""
    same = reloc = 0
    diffs = []
    i = a0
    while i < a1:
        if cand[i] == ref[i]:
            same += 1
            i += 1
            continue
        if i + 1 < a1:
            a, b = rd(ref, i), rd(cand, i)
            if (a + T) & 0xFFFF == b or (a + dh) & 0xFFFF == b:
                reloc += 2
                i += 2
                continue
        diffs.append(i)
        i += 1
    return same, reloc, diffs


tot_same = tot_reloc = 0
bad = []                                     # (nome, offset)
s, r, d = compare(0, first_mirror, DH_FINAL)
tot_same += s
tot_reloc += r
P("== Area ORIGIN/USER (+0000..+%04X): uguali %d, rilocati %d, diversi %d"
  % (first_mirror - 1, s, r, len(d)))
bad += [('<ORIGIN>', i) for i in d]

P()
P("== Progressione dello scarto sull heap (mirror nuovo - mirror rif.)")
P("   Un salto = heap consumato in piu' nel sorgente tra la parola precedente e")
P("   questa: definizioni ausiliarie, oppure salto alla pagina 8K successiva")
P("   (PAGE-WATERMARK = $1EFF: +258 byte = da $1F00 a $2002).")
prev_dh, prev_name, n_ok = None, '<inizio>', 0
for k, (nm, xt) in enumerate(words):
    m0 = xt - 2 - ORG_REF
    m1 = words[k + 1][1] - 2 - ORG_REF if k + 1 < len(words) else N
    dh = (rd(cand, m0) - rd(ref, m0)) & 0xFFFF
    if dh != prev_dh:
        P("   %-14s dopo %-14s scarto $%04X%s" % (
            nm, prev_name, dh,
            '' if prev_dh is None else '   (%+d byte)' % (dh - prev_dh)))
        prev_dh = dh
    prev_name = nm
    s, r, d = compare(m0 + 2, m1, dh)
    tot_same += s + 2
    tot_reloc += r
    if d:
        bad += [(nm, i) for i in d]
    else:
        n_ok += 1

exp = [b for b in bad if b[1] in EXPECTED]
bad = [b for b in bad if b[1] not in EXPECTED]
P()
P("== Riepilogo")
P("   byte uguali        : %d" % tot_same)
P("   byte rilocati      : %d   (indirizzi codice +T, puntatori heap +scarto)"
  % tot_reloc)
P("   differenze attese  : %d byte" % len(exp))
P("   byte NON spiegati  : %d in %d parole/aree"
  % (len(bad), len({b[0] for b in bad})))
P("   parole senza differenze: %d su %d" % (n_ok, len(words)))
P()
if exp:
    P("== Differenze attese")
    for nm, i in exp:
        P("   +%04X ($%04X) rif=%02X nuovo=%02X   %s"
          % (i, ORG_REF + i, ref[i], cand[i], EXPECTED[i]))
    P()
if bad:
    P("== Differenze NON spiegate (offset dal riferimento; indirizzo nel riferimento)")
    cur = None
    for nm, i in bad:
        if nm != cur:
            P("   [%s]" % nm)
            cur = nm
        P("      +%04X ($%04X) rif=%02X nuovo=%02X" % (i, ORG_REF + i, ref[i], cand[i]))
    P()
P("ESITO: " + ("COERENTE" if not bad else "DIFFERENZE DA ESAMINARE"))

text = '\n'.join(out)
if log_path:
    open(log_path, 'w').write(text + '\n')
print(text)
sys.exit(0 if not bad else 1)
