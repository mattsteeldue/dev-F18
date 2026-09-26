# Piano: ambiguita' `ha` / indirizzo fisico -- eliminata l'euristica ?HEAP_PTR

> Stato: **APPLICATO 2026-09-26** (build 2026-09-26, non ancora committato)
> nella forma della sez. 0 -- NON la soglia `$E000` delle Fasi 1-3, superate.
> Verificato: `/check-f18e` COERENTE (CSpect, 2026-09-26, 0 byte non
> spiegati); CORE-TESTS 100% ok su CSpect.
> DOT provato su CSpect: funziona (2026-09-27).
> Resta: incollare nel .odt
> `products/manual-par-4.6-nfa-ambiguity.txt` e
> `products/manual-par-4.6-3.8-build-20260926.txt` (9 blocchi da aggiornare),
> Fase 4 (`WORDS`), bug preesistente di `lib/hide-word.f` (sez. 0.1).

## 0. Decisione finale (2026-09-26): nessuna soglia, contratto per posizione

Discutendo con l'autore: `?HEAP_PTR` / `?>HEAP` non servono piu'. L'archivio
`C:\Zx\Forth\F15\tools\vForth\version\2023\20230214.ZIP` (26 istantanee
`src/F16c_001..026.f`, v1.62) mostra che nascono in `F16c_007_heap.f`
(23-02-2023) per leggere un dizionario **misto** durante la transizione
1.6 (header nel dizionario) -> 1.7 (header in heap): in `F16c_026.f` `mcod`
scrive ancora l'header nel dizionario, mentre `(find)`, `<name`, `pfa`,
`id.`, `words`, `forget`, `marker` leggono entrambi i formati. La soglia
(`$4000`, poi `$6300` e `$6000` in `(FIND)`) voleva dire "appena sotto
l'ORIGIN" (`6100h or 6366h or 8000h` allora). Il caso "MMU7 = pagina 01" di
`PFA` serviva alla vecchia doppia compilazione. Nella 1.8 e' tutto morto.

Contratto adottato (lo stesso che gia' insegnava `tutorial/022`):

- **sempre `ha`**: contenuto di LFA, voc-cell, mirror a `cfa-2`, `HP`, celle
  di `MARKER`;
- **sempre risolto**: l'`nfa` sullo stack (`LATEST`, `NFA`, `<NAME`, `ID.`,
  `PFA`).

Applicato (DOES = DOT, e `src/F18e.f`):

- `(FIND)`: `FAR` incondizionato su testa e link;
- `<NAME`: `cell- @ FAR cell- 1- -1 TRAVERSE`;
- `ID.`, `PFA`: niente `?>HEAP`; `PFA` = `1 TRAVERSE 1+ CELL+ @ >BODY`;
- `MARKER` runtime: `FAR` prima di `PFA`; `FORGET` ripulito dai commenti;
- rimosse `?HEAP_PTR`, `?>HEAP`, `?IN_MMU7` (e i relativi `help/`); nessuna
  copia in `inc/doc/`: non sono piu' parole core;
- libreria: `lib/see.f` (`DEB-LFA ... FAR ID.`), `lib/hide-word.f`
  (`@ FAR PFA`), `inc/.vocab.f` (`CELL-` invece di `CELL- CELL-`: bug
  preesistente, prima mascherato dall'euristica, ora bloccava `?VOCAB`),
  `inc/_noname.f` (tolto il ramo 1.7, compila la cella mirror);
- core piu' piccolo: dizionario +86 byte liberi, heap +38.

Verifica: `emu/test_nfa_contract.py` 20/20 (nomi con `HP` a `$5F00`,
`$6400`, `$C000`, `$E400`; `<NAME`, `ID.`, `NFA`/`PFA`, `LFA @ FAR`,
`FORGET`, `MARKER`, `:NONAME`, `SEE`, `?VOCAB`); controprova sui binari di
build 2026-09-25: dopo `5F00 HP ! : W5` il dizionario non trova piu' nulla.
`test_emulator`, `test_extended`, `test_words_stream` ok.

## 0.1 Bug preesistente trovato: `HIDE-WORD` non nasconde nulla

`lib/hide-word.f`: il ciclo trova l'LFA della parola che segue quella da
nascondere e lascia due valori sullo stack senza scrivere nulla; il file
termina con un `; DECIMAL` spurio (`;? Can't be executed` al caricamento).
Da riscrivere a parte (non legato all'euristica).

Riferimenti: `products/manual-par-4.6-nfa-ambiguity.txt` (bozza par. 4.6.1
del manuale, da correggere -- Fase 5), `planners/HEAP-PAGE-PARAM-PLAN.md`
(pagine heap $20-$27 cablate: ortogonale, ma tocca le stesse routine).

---

## 1. Il problema in una riga

Un `ha` (heap-pointer, bit 15-13 = pagina $20-$27, bit 12-0 = offset da
`$E000`) e un indirizzo fisico gia' risolto con `FAR` hanno lo stesso tipo di
cella. Il core li distingue con una soglia numerica, e la soglia e' scritta in
**tre** punti con **due** valori diversi.

## 2. Mappa dei punti euristici (build 2026-09-25)

Layout di un header (tutti gli header stanno in heap dalla 1.8):

```
heap:        [len|flag][nome...][LFA: ha nfa precedente][xt: -> CFA]
dizionario:  [mirror: ha della cella xt]  CFA: codice ...
```

| # | Punto | Test | Cosa classifica |
|---|---|---|---|
| A | `?>HEAP` (`L1.asm:533`) usato da `ID.` (`L1.asm:1540`) e `PFA` (`L1.asm:635`) | `dup if $6300 u< then` | l'argomento `nfa`: qui entrano davvero entrambe le rappresentazioni |
| B | `?HEAP_PTR` dentro `<NAME` (`L1.asm:594`) | come sopra | il **contenuto del mirror** a `cfa-2`: sceglie fra layout 1.8 (header in heap) e layout 1.7 (header in linea nel dizionario, ramo ormai morto) |
| C | `(FIND)` in macchina (`L0.asm:506`; `F18e.f:801`, gia' marcato `*# /!\ #*`) | `ld a,d / sub $60 / jr nc` | testa della vocabulary e ogni link |

Sicure (FAR incondizionato): `LATEST`, `WORDS` (ogni link), `CODE`,
`SPLASH`.

Chi passa da A/B/C:

- core: `-FIND`, `'`, `INTERPRET`, `NEEDS` (C); `NFA`, `LFA`, `FORGET`,
  `MARKER` (B); `CODE` (warning "isn't unique": `<NAME ID.`), `WORDS` (`ID.`
  su fisico), `MARKER` runtime (`PFA` su `ha` salvato) (A);
- libreria: `.WORD`, `.VOCAB`, `RENAME`, `SEE` (`DEB-NFA`, `DEB-LFA` -> `ID.`
  su un `ha` di link), `hide-word` (`@ PFA` su un `ha`), `set-fence`,
  `LOCALS` (`LATEST PFA LFA @`), `:NONAME`.

**Perche' anche le parole a `cfa`:** il `cfa` non e' ambiguo; lo e' il
passaggio `cfa -> nfa`, che passa solo da `<NAME` e dal test B sul mirror.
Parole che non risalgono al nome (`EXECUTE`, `>BODY`, `COMPILE,`) sono immuni.

## 3. Fatto nuovo: il limite reale e' `$6000`, non `$62FF`

Verificato nell'emulatore (DOES): con `HP` a `$6000` o `$6100`, `: ZZ ;`
rompe gia' la ricerca (`;? is undefined`) per via di C. Con `$5F00` funziona,
ma `SKIP-HP-PAGE` porta subito `HP` a `$6002`. Quindi i nomi hanno oggi
~24K (pagine $20-$22), non ~24.75K.

## 4. Semantica della soglia `$E000`

- `ha < $E000` (pagine $20-$26), escluso `0` = fine catena: e' un
  heap-pointer, va risolto con `FAR`.
- valore `>= $E000`: e' un indirizzo **gia' risolto**, nella finestra MMU7.

Precisazione: la soglia garantisce che il valore e' *convertito*, **non**
che la pagina in MMU7 sia *ancora quella giusta*. Il valore non porta con se'
la pagina: e' valido solo finche' nessuno rimappa MMU7 (un altro `FAR`, un
accesso `HEAP`, un `MMU7!` utente, +3DOS -- quest'ultimo coperto da
`(EMITC)` dal 2026-06-12). Questo resta disciplina del chiamante (Fase 4).

Residuo: gli `ha` di pagina 7 (`$E000-$FFFF`) coincidono con i fisici. Si
chiude vietando i **nomi** in pagina 7 (Fase 2); i dati a runtime possono
usarla, perche' passano sempre da `FAR` esplicito.

Nel DOT la soglia `$E000` smette anche di sovrapporsi al codice
(`$2000-$3FFF`), che con `$6300` le stava tutto sotto.

**Prova a runtime (emulatore, 2026-09-26):** `E0` in `' (FIND) $A +` e
`$E000` in `' ?HEAP_PTR $B +`, poi nomi con `HP` a `$6400` e `$C000`:
`<NAME`, `ID.`, giro `NFA PFA CFA`, `FORGET` (ripristina `HP` a `$C000`),
`WORDS` tutti corretti.

## 5. Fasi

### Fase 1 -- soglia unica `$E000` (core) -- SUPERATA dalla sez. 0

- DOES e DOT, `L1.asm` `?HEAP_PTR`: `LIT, $6300` -> `LIT, $E000`; commenti
  di `?HEAP_PTR` / `?>HEAP` aggiornati ("below $E000 ... heap-pointer").
- DOES e DOT, `L0.asm` `(FIND)`: `sub $60` -> `sub $E0`; commento.
- `src/F18e.f`: `[ HEX 6300 ] Literal` (riga ~3393) e `SUBN HEX 060 N,`
  (riga 801) -> `E000` / `0E0`; commenti (righe ~800, ~3400).
- Stessa dimensione: nessuno spostamento di indirizzi, quindi i testi del
  par. 4.6 generati da `util/gen-dict-structure.py` non cambiano (da
  confermare con `/regen-doc-dict-structure`, atteso "INVARIATI").
- `/bump-build`, `/check-f18e` (compilazione su CSpect a cura dell'autore).
- Test: nuovo `emu/test_heap_threshold.py` (nomi con `HP` a `$5F00`,
  `$6400`, `$C000`, `$DF00`; `<NAME`, `ID.`, `NFA`/`PFA`, `FORGET`,
  `MARKER`, `WORDS`), piu' `SEE` e `hide-word` caricati via `NEEDS`.

### Fase 2 -- guardia sui nomi in pagina 7 -- SUPERATA (nessuna ambiguita' residua)

- In `CODE` (unico costruttore di header del core), prima di scrivere
  l'header: `HP@ $E000 U< 0= n ?ERROR`. Stima: 5 celle + ~1 riga di
  messaggio.
- Costo: **sposta gli indirizzi** -> rigenerare il par. 4.6 e aggiornare la
  tabella del boot in `CLAUDE.md`. Valutare se accorparla alla Fase 1 (un
  solo bump) o farla dopo.
- Serve un numero di messaggio libero nel block file (Screen 4-8, o area
  negativa Screen 2-3): scegliere e documentare come fa `lib/LOCALS.f`.
- Alternativa senza costo nel core: solo documentazione ("non definire nomi
  con `HP@` >= `$E000`"). Da decidere con l'autore.

### Fase 3 -- (facoltativa) togliere l'euristica dove il tipo e' noto -- FATTA, anche per A (sez. 0)

- C: in `(FIND)` testa e link sono sempre `ha` -> `FAR` incondizionato
  (si risparmiano i 3 byte di test; sposta indirizzi).
- B: in `<NAME` il mirror e' sempre un `ha` -> `@ FAR cell-` incondizionato,
  eliminando il ramo del layout 1.7.
- Prerequisito: `inc/_noname.f` oggi **non compila il mirror** prima
  dell'xt, quindi `<NAME` su un xt di `:NONAME` da' gia' spazzatura; va
  aggiunto il `HP@ CELL- ,` come fa `CODE` (e tolto il ramo 1.7).
- A resta euristico per scelta: `ID.` e `PFA` ricevono davvero entrambe le
  forme, e cambiarne il contratto romperebbe codice utente.

### Fase 4 -- (ortogonale) `WORDS` senza fisici attraverso l'output

- Applicare il redesign del 2026-07-12: leggere il link successivo subito
  dopo `FAR`, prima di qualunque `EMIT`. Non dipende dalle fasi 1-3.

### Fase 5 -- documentazione

- `products/manual-par-4.6-nfa-ambiguity.txt`: correggere "every word with
  `( cfa -- )`" (solo `cfa -> nfa`), il limite `$62FF` -> `$6000` (o il nuovo
  limite dopo la Fase 1), la frase "the two call sites that use ?HEAP_PTR"
  (sono tre punti, uno in macchina) e il capoverso "No low-cost, complete fix
  is known". Formato: un paragrafo per riga, CRLF (regole `products/`).
- `lib/CLAUDE.md` (Heap Memory Facility): limite dei nomi.
- `HISTORY.txt` alla release.

## 6. Rischi da verificare

- Qualcuno passa a `ID.`/`PFA` un indirizzo fisico **sotto** `$E000`?
  Nel layout 1.8 no (header solo in heap); il ramo `ELSE` di `_noname.f` e'
  per la 1.7. Da riconfermare con grep su `demo/`, `tutorial/`, `test/`.
- `PFA` salta il fetch dell'xt se `MMU7@` = 1 (`L1.asm:643`): verificare che
  resti coerente con fisici `>= $E000` a pagina 1 mappata (caso DEBUGGING).
- `HEAP-PAGE-PARAM-PLAN`: se la base heap diventa configurabile, la soglia
  `$E000` resta valida (dipende dalla finestra MMU7, non dalla pagina-base).
