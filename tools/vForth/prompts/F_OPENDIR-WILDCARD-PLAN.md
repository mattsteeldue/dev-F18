# F_OPENDIR: abilitare il filtro wildcard NextZXOS (mode $30)

**Status**: Design Plan (non ancora implementato)
**Author**: Matteo Vitturi (con Claude)
**Date**: 2026-07-25 (revisionato dopo verifica su hardware/emulatore reale)

---

## Contesto

Tentativo iniziale (superato): far accettare a `F_OPENDIR` un secondo
parametro `wc` (wildcard z-string), con firma `( a wc -- fh f )` invece
dell'attuale `( a -- fh f )`. Questo avrebbe rotto lo stack-effect di una
CODE word core gia' documentata/pubblicata in 1.8, richiedendo un bump a
1.9 (vedi versione precedente di questo piano, sostituita da questa).

**Verifica su hardware/emulatore reale**: NextZXOS applica il filtro
wildcard leggendo il pattern **al momento di `F_READDIR`**, non di
`F_OPENDIR`. Basta che l'apertura richieda il modo
`esx_mode_lfn_only | esx_mode_use_wildcards` ($30 invece di $10); il
pattern stesso lo riceve gia' `F_READDIR` tramite il suo parametro
esistente `a2`, correttamente instradato in `DE` sia in DOES sia in DOT
(nessuna modifica li' necessaria, mai lo e' stata).

Di conseguenza:
- `F_OPENDIR` **non cambia stack-effect**: resta `( a -- fh f )`.
- **Nessun bump di versione necessario** (non e' una breaking change).
- L'unica modifica al core e' interna al corpo della CODE word: il byte
  di modo passato in `B` cambia da `$10` a `$30`. Identica in DOES e DOT
  (nessuna delle asimmetrie DOES/DOT segnalate nella versione precedente
  di questo piano si applica piu': non tocchiamo il flusso dei registri,
  solo un letterale).

`lib/dir.f` e' gia' stato aggiornato dall'utente in coerenza con questo:
`DIR-TO-HEAP` chiama `F_OPENDIR` con un solo parametro (riga 182), e lo
shadow sperimentale `INCLUDE inc/f_opendir.f` e' gia' stato rimosso.

---

## Modifiche

### 1. Core asm -- DOES

`project/vForth18_DOES/source/next-opt0.asm:224` (dentro il blocco
`F_OPENDIR`, righe 218-229): cambiare

```asm
                ld      b, $10              // file-mode
```
in
```asm
                ld      b, $30              // lfn_only | use_wildcards
```

Aggiornare il commento della word (riga 218) da `a1 -- u f` resta
invariato come firma (nessun cambio di stack-effect), ma va aggiornata la
frase descrittiva sotto per menzionare il filtro wildcard, es.:

```asm
// f_opendir    a1 -- u f
// open a directory, request NextZXOS-side wildcard filtering (mode $30);
// the pattern itself is supplied later via F_READDIR's a2 parameter
```

### 2. Core asm -- DOT

`project/vForth18_DOT/source/next-opt0.asm:232` (stesso blocco, righe
222-236): identica modifica `ld b,$10` -> `ld b,$30`. Nessun'altra riga
tocca, nessuna differenza di trattamento fra le due varianti per questa
modifica (a differenza della versione precedente del piano).

**Aggiunta (gotcha trovato rileggendo l'asm DOT): manca il `di` prima
della syscall in ENTRAMBE le word, sia in `F_OPENDIR` sia in `F_READDIR`**,
a differenza della DOES dove e' presente in entrambe. Questo e' incoerente
con la politica generale della DOT (project/CLAUDE.md, "ROM Call Strategy"
-- avvolgere le chiamate ROM/syscall con `di`/`ei` perche' l'ambiente
dot-command puo' essere interrotto dall'OS). Da correggere in questo
stesso intervento, non e' legato al cambio wildcard ma va sistemato ora
che si tocca questa zona:

- `project/vForth18_DOT/source/next-opt0.asm` blocco `F_OPENDIR` (righe
  222-236): aggiungere `di` subito prima di `rst $08` (riga con
  `db $A3`), cioe' fra `ld a, "C"` e `rst $08`.
- `project/vForth18_DOT/source/next-opt0.asm` blocco `F_READDIR` (righe
  241-257): aggiungere `di` subito prima di `rst $08` (riga con
  `db $A4`), cioe' subito dopo l'ultimo `exx` (riga 254) e prima di `rst
  $08` (riga 255).

**Verificato (non serve piu' "da controllare"): l'`ei` di pareggio esiste
gia' ed e' condiviso, nessun nuovo `ei` va aggiunto.** Sia in DOES sia in
DOT lo schema e' identico: ogni word fa il proprio `di` poi la syscall poi
salta (`jr`) in una catena condivisa:

```
F_OPENDIR  --di, rst $08-->  jr F_Open_Exit
F_READDIR  --di, rst $08-->  jr F_Open_Exit
F_OPEN     --di, rst $08-->  (cade in) F_Open_Exit:
                                 // ei   <- commentato: "removed because
                                 //         is repeated in f_read_exit"
                                 ld e,a / ld d,0
                                 jr F_Read_Exit
F_READ     --di, rst $08-->  (cade in) F_Read_Exit:
                                 ei                    <-- il vero, unico ei
                                 exx / pop bc,de,ix / ...
                                 next
```

(DOT: `F_Open_Exit` a riga 210, `F_Read_Exit` a riga 131; DOES: rispettivamente
riga 204 e riga 129 -- stessa identica struttura in entrambe le varianti).
Quindi l'unico `ei` reale del gruppo vive in `F_Read_Exit` e viene
raggiunto da tutte e quattro le word (F_OPEN/F_OPENDIR/F_READDIR via
`F_Open_Exit`, F_READ direttamente) tramite la catena di `jr`. Aggiungere
il `di` mancante in `F_OPENDIR`/`F_READDIR` (DOT) le allinea semplicemente
allo stesso schema gia' seguito da `F_OPEN`/`F_READ` nella stessa DOT e da
tutte e quattro le word nella DOES -- nessun'altra modifica all'exit path
e' necessaria.

### 3. `src/F18e.f`

Non serve piu' un file separato per una linea "1.9" (non c'e' bump).
La modifica va direttamente in `src/F18e.f`, riga ~1778
(`LDN B'| HEX 10 N,` dentro `CODE f_opendir ( a -- fh f )`):

```forth
        LDN     B'|   HEX 30   N,
```

`src/F19e.f` (copia manuale preparata in previsione del bump, non piu'
necessaria): **eliminare**.

### 4. `inc/f_opendir.f`

Documentava la firma a due parametri `( a wc -- fh f )`, ormai priva di
riscontro reale (ne' nel core attuale ne' in quello futuro). **Eliminare
il file** (nessuna copia in `inc/doc/`: non c'e' nulla di corretto da
preservare come riferimento).

### 5. `lib/dir.f` -- rifinitura commenti

Il codice e' gia' corretto (`F_OPENDIR` a un parametro, `WILDCARD-SPEC
... F_READDIR` a valle), ma restano due commenti non aggiornati rispetto
al nuovo schema (il filtro avviene in F_READDIR, non in F_OPENDIR):

- Riga 178: `\ matching WILDCARD-SPEC (filtered by NextZXOS itself, see
  f_opendir.f).` -- il riferimento a `f_opendir.f` non ha piu' senso
  (file da eliminare, punto 4). Riformulare, es.: `\ matching
  WILDCARD-SPEC (filtered by NextZXOS itself via F_READDIR's a2 --
  F_OPENDIR just requests wildcard mode).`
- Riga 190: `\ a a2 -- same pattern given to F_OPENDIR` -- impreciso, il
  pattern non va a F_OPENDIR. Correggere in qualcosa come `\ a a2 --
  pattern read by F_READDIR (NextZXOS applies the filter here)`.

### 6. `help/f_opendir.txt`

Stack-effect invariato (`a -- fh f`), ma la semantica e' cambiata
(richiede ora il modo wildcard): aggiornare la descrizione, es.:

```
    F_OPENDIR  a -- fh f

Open directory at path a, requesting NextZXOS-side wildcard
filtering mode. Returns directory handle and error flag.
The actual pattern is supplied later via F_READDIR's a2.
```

`help/f_readdir.txt` resta invariato (gia' corretto).

---

## Ordine di esecuzione

1. Core asm DOES -- punto 1.
2. Core asm DOT -- punto 2 (cambio mode byte + aggiunta `di` mancante in
   `F_OPENDIR` e `F_READDIR`).
3. `src/F18e.f` -- punto 3; eliminare `src/F19e.f`.
4. Eliminare `inc/f_opendir.f` -- punto 4.
5. Rifinitura commenti `lib/dir.f` -- punto 5.
6. `help/f_opendir.txt` -- punto 6.
7. Rebuild (`/build DOES`, `/build DOT`).
8. Verifica in emulatore/CSpect.

## Verifica

- Ricompilare entrambe le varianti (`/build DOES`, `/build DOT`).
- Nell'emulatore headless: boot completo, `NEEDS DIR`, poi `WILDCARD *.F`
  seguito da `DIR lib` (o path equivalente) su un'immagine con file misti
  -- verificare che l'elenco risultante contenga solo `.f`.
- Verifica finale su CSpect reale/hardware resta a carico dell'utente
  (gia' fatta in parte, secondo quanto riportato).
- Verifica dedicata per la DOT dopo l'aggiunta dei due `di`: eseguire
  `DIR`/`WILDCARD` nel dot-command in emulatore, per confermare che gli
  interrupt restino correttamente disabilitati durante la syscall e
  riabilitati una sola volta nel percorso di uscita condiviso (nessuna
  regressione sul resto del boot/REPL della DOT).

## Fuori scope

- Nessun bump di versione: questo intervento non tocca ne' i banner
  SPLASH, ne' `CLAUDE.md` ("Current version" / "Breaking Changes"), ne'
  gli skill di release.
