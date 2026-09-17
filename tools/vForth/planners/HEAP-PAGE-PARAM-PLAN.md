# HEAP-PAGE-PARAM: rendere configurabile la pagina-base dell'HEAP

**Status**: Design Plan (non ancora implementato)
**Author**: Matteo Vitturi (con Claude)
**Date**: 2026-07-25

---

## Obiettivo

Oggi la HEAP memory facility (vedi `lib/CLAUDE.md` sez. "Heap Memory Facility")
usa le 8 pagine MMU7 **$20-$27** (32-39 decimale) come zona dedicata, cablate
per valore letterale in una decina di punti sparsi fra assembler del core e
libreria Forth. L'obiettivo e' **raccogliere in un solo posto** la scelta della
pagina-base, cosi' che un utente che ricompila vForth (varianti DOES e DOT)
possa spostare l'HEAP altrove (ad es. per liberare $20-$27 per un altro uso, o
per convivere con un allocatore di sistema che ha gia' assegnato quelle
pagine).

**Non e' un obiettivo di questo piano** rendere la scelta configurabile *a
runtime*: il dizionario stesso vive nell'HEAP fin dalla sua parte iniziale
(vedi `lib/CLAUDE.md`: "Heap-pointer format"), quindi la base deve restare
**cablata in fase di compilazione** — cambiarla richiede comunque di
ricompilare `forth18e.bin`/`ram8.bin` (DOES) o il dot-command (DOT), oltre a
rigenerare a mano i pochi file `inc/` coinvolti.

---

## Vincolo strutturale (non e' cablatura, e' il formato dati)

Il puntatore-heap `ha` e' una singola cella a 16 bit:
- **bit 15-13** (3 MSB): numero di pagina, **relativo alla base**
- **bit 12-0** (13 LSB): offset di byte da `$E000` dentro quella pagina

Questo fissa **il numero di pagine a 8** (valori relativi 0-7), qualunque sia
la base scelta. Solo la **pagina-base** e' liberamente rilocabile: cambiare il
conteggio di pagine richiederebbe di allargare il campo a 4 bit (16 pagine) o
piu', il che romperebbe il formato di `ha` ovunque (`<FAR`, `>FAR`, `HP@`,
`SKIP-HP-PAGE`, ...) — fuori scope per questo piano.

---

## Inventario dei punti cablati

### A. Nucleo assembler (richiede ricompilazione di DOES e/o DOT)

| File:riga | Routine | Cablatura attuale |
|---|---|---|
| `project/vForth18_DOES/source/L0.asm:470-485` | `TO_FAR_rout` (uso interno di `(find)` per risolvere i puntatori-heap dei nomi nel dizionario) | `and $07` / `add $20` |
| `project/vForth18_DOT/source/L0.asm:470-485` | idem, chiamata da `(find)` a riga 511 | stesso `and $07` / `add $20` |
| `project/vForth18_DOT/source/L2.asm:445-451` (`Set_forth_MMU`) | mappatura MMU a boot | `nextreg $57,$20` (MMU7=heap) e `$54-56, $28,$29,$2A` (MAIN = base+8..+10) |
| `project/vForth18_DOT/source/L2.asm:465-493` (`Restore_Reserve_MMU` / `Deallocate_MMU`) | riserva/rilascio pagine presso NextZXOS a ogni avvio/uscita | `ld l,$20` (prima pagina) + `ld h,8+3+1` (12 pagine: 8 heap + 3 main + 1 backup) via `M_P3DOS` |
| `project/vForth18_DOT/source/L2.asm:356-359` | backup di MMU2 | pagina di backup `$28` = base+8 |

Nota: **DOES non riserva le pagine presso il sistema operativo** — si affida
solo al loader BASIC (vedi punto B). **DOT** invece registra/rilascia
esplicitamente le 12 pagine (8 heap + 3 main + 1 backup) a ogni avvio/uscita.

### B. Loader BASIC (DOES) — richiede rigenerazione del `.bas`

`Forth18_loader.bas` (radice repo):
```
LOAD "ram8.bin" BANK 16
```
`BANK 16` e' un banco **16K** (vedi CLAUDE.md "Banks vs Pages"): banco *n* =
pagine 8K *2n* e *2n+1*. Banco 16 = pagine $20/$21. Questo e' il punto che
ancora `ram8.bin` (immagine compilata della prima pagina di heap, prodotta dal
build stesso via `SAVEBIN "output/ram8.bin", $E000, $2000` in
`project/vForth18_DOES/source/main.asm:174`) a un banco fisico preciso. Se si
sposta la base, **questo numero deve restare in sincronia** (banco =
base-pagina / 2 — quindi la base va scelta pari, cioe' allineata a 16K, non
solo a 8K).

### C. Libreria `inc/` — ricompilata dall'utente finale a ogni `NEEDS`

| File | Cablatura |
|---|---|
| `inc/{far.f` (`<FAR`, codifica indirizzo+pagina -> `ha`) | `AND $07` — commento originale nel file stesso: *"questionable: it could be SUB $20"* |
| `inc/}far.f` (`>FAR`, decodifica `ha` -> indirizzo+pagina) | `add $20 <-- 32` |
| `inc/heap-dos.f` (`HEAP-DOS`, usata da `HEAP-INIT`/`HEAP-DONE`) | loop `28 20 DO ... LOOP` (riserva/libera $20-$27 via `M_P3DOS`) |
| `lib/heap.f` (righe 35-42) | 8 righe srotolate, stessa identica chiamata di alloc di `heap-dos.f` ma duplicata ed eseguita **incondizionatamente al solo caricamento del file** (non solo quando si chiama `HEAP-INIT`) — sembra codice morto/ridondante rispetto a `heap-dos.f`, da verificare se va rimosso in un secondo momento (non strettamente necessario per la parametrizzazione, ma la duplicazione andrebbe comunque sistemata quando si tocca questa zona) |

### D. Nota a margine (bug di documentazione, non di codice)

`inc/}far.f` e la copia in `src/F18e.f` (~riga 3420) riportano nel commento
"page number n between 64-71 (40h-47h)", ma sia il codice sia gli esempi
subito sotto nello stesso commento ("`0000 >FAR` gives `20.E000`" ... "`FFFF
>FAR` gives `27.FFFF`") confermano che il range restituito e' **32-39
($20-$27)**, non 64-71. E' un refuso nel commento, non un bug funzionale —
da correggere quando si tocca il file per altri motivi, non necessita di un
intervento dedicato.

---

## Proposta

1. Introdurre una costante simbolica unica, ad es. `HEAP_BASE_PAGE equ $20`,
   in `system.asm` (file condiviso da entrambe le varianti, incluso sia da
   `vForth18_DOES/source/main.asm` sia da `vForth18_DOT/source/main.asm`).
2. Sostituire tutti i letterali `$20` degli usi elencati nella tabella A con
   `HEAP_BASE_PAGE` (e i derivati `+8`, `+9`, `+10`, `+11` per MAIN/backup in
   `L2.asm` di DOT, gia' espressi come offset relativi nei commenti — vanno
   resi offset relativi anche nel codice).
3. In `inc/{far.f`, sostituire `AND $07` con `SUB HEAP_BASE_PAGE` (costo
   trascurabile, stessa dimensione in T-state) cosi' la base non deve piu'
   essere per forza multiplo di 8 — resta comunque richiesto che sia **pari**
   (vincolo del banco a 16K per il loader BASIC, punto B).
4. Documentare una checklist di rigenerazione manuale per i file che
   restano fuori dal binario compilato e vanno editati a mano un valore alla
   volta: `inc/{far.f`, `inc/}far.f`, `inc/heap-dos.f`, `lib/heap.f`,
   `Forth18_loader.bas` (e l'equivalente in `project/vForth18_DOT` se genera
   un proprio loader/parametro).
5. Aggiornare `lib/CLAUDE.md` (sezione "Heap Memory Facility") per
   documentare esplicitamente: base rilocabile/pari, conteggio pagine fisso a
   8, e puntare a questo piano per la procedura di modifica.

## Punti aperti da verificare prima di implementare

- **Persistenza dell'HEAP nella variante DOT**: `L2.asm` commenta "Loads
  vocabulary image to $E000 from persistent heap pages" — va capito se il
  contenuto dell'HEAP di DOT sopravvive fra un'esecuzione e l'altra del
  dot-command (pagine OS gia' popolate) o se viene sempre ricaricato da un
  file come per DOES; questo cambia cosa "spostare la base" comporta in
  pratica per DOT (rigenerare un'immagine vs. semplice ricompilazione).
- Decidere se questa funzionalita' va esposta come vero e proprio "profilo di
  build" (parametro passato a un futuro skill di rebuild) o resta una
  modifica manuale una-tantum per l'utente avanzato che vuole un'altra
  configurazione.

### E. Emulatore headless `emu/` (verificato 2026-07-25)

Non blocca l'implementazione (l'emulatore e' uno strumento di supporto, non
il core), ma va tenuto allineato per non rompere i test se si cambia la base:

| File | Cablatura | Natura |
|---|---|---|
| `emu/emulator.py:51` | `self._mmu7_page = 0x20  # Current heap page (initially page 32)` | default esplicito, generico (non deriva la base da altro) |
| `emu/test_words_stream.py:37` | `return getattr(self, "_mmu7_real", 0x20)` | stesso fallback, in un mock di test |
| `emu/small_emulator.md:100` | formula esplicita `page = 32 + (ha >> 13)` | documentazione |
| `emu/small_emulator.md:118-119` | pseudocodice: `if n == 32 ($20): already mapped -- do nothing / else: raise EmulatorError('multi-page heap not yet supported')` | **limite funzionale dichiarato**: il modello dell'emulatore supporta esplicitamente solo la pagina $20, non l'intero range $20-$27 |
| `emu/small_emulator.md:74,80-92,140,357,425-428` | base pagina / `BANK 16` ripetuti in prosa e in tabella riepilogativa | documentazione |

`emu/z80_instructions.py` (righe 1246-1259) e `emu/trace_words.py` instradano
`mmu7_page` genericamente via NextReg $57 senza assumere $20: non richiedono
modifiche. `emu/README.md` non cala mai il numero esplicitamente (parla solo
genericamente di "MMU7 page"): non richiede modifiche.
