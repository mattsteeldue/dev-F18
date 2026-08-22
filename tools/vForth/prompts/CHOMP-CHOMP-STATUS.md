# chomp-chomp: stato della revisione (2026-08-23)

Nota di ripresa per continuare il lavoro da un'altra sessione.
Piano approvato completo: `C:\Users\matteo\.claude\plans\glowing-mixing-haven.md`
(4 stadi: AI+pacing, colori ciclici, font in RAM, labirinti su Screen).

## Dove siamo

**Stadio 1 (AI dei fantasmi + pacing) — codice completo, compila, non ancora
validato su CSpect.** Stadi 2, 3 e 4 non iniziati.

File modificati nel working tree, **non committati**:

| File | Stato |
|---|---|
| `demo/chomp-chomp.f` | Stadio 1 completo (+350 / -119 righe) |
| `demo/README.txt` | voce riscritta: non dice più "ghosts movement are completely random" |
| `test/CHOMP-AI-TESTS.f` | nuovo, ~45 asserzioni — **contiene 2 bug miei, vedi sotto** |

Non ancora fatto (previsto dal piano a fine lavoro): ricopiare il master su
`demo/chomp-chomp/chomp-chomp.f` (oggi divergono), rigenerare i `.bin`
standalone con `ZAP GAME` (solo a mano, da sessione vForth viva), e la nota
"superata" sullo Screen 600.

## Cosa è verificato

- Nessun riferimento in avanti fra le nuove parole; nessuna collisione di nome
  con parole core.
- File ASCII a 7 bit, niente TAB, terminazione conforme alla regola di `INCLUDE`.
- **`INCLUDE demo/chomp-chomp.f` compila da cima a fondo nell'emulatore
  headless**, tutti i banner inclusi il nuovo `Chomp.f - scatter/chase`.
- L'aritmetica dell'AI **non è ancora verificata**: la prima esecuzione della
  suite è fallita per due difetti del file di test, non del gioco.

## Prossimo passo immediato: correggere `test/CHOMP-AI-TESTS.f`

1. **Manca `DECIMAL`.** La catena `NEEDS TESTING` lascia BASE in **HEX**, quindi
   i letterali del test venivano letti in esadecimale mentre il gioco è
   compilato in decimale. È questo, e non l'AI, a spiegare il pattern strano dei
   fallimenti (`10 12 key-down step-cell` passa, `key-up` no: `11`=0x11 coincide,
   `9`≠0x0F). La prova è `FFFC` comparso nello stack residuo, cioè -4 in hex.
   Rimedio: `DECIMAL` subito **dopo** `NEEDS TESTING`.
   Da approfondire a parte: quale file della catena lascia BASE in hex. Il gioco
   non ne soffre perché `: game` fa `decimal` a runtime.
2. **`DO...LOOP` in interpretazione.** Le due asserzioni sulle fasi usano
   `70 0 do tick-phase loop` dentro `T{ ... }T`, ma `DO`/`LOOP` sono
   compile-only: l'emulatore dice `do? Can't be executed.`. Vanno incapsulate,
   es. `: run-phases ( n -- ) 0 ?do tick-phase loop ;` e poi `70 run-phases`.

Dopo la correzione, rieseguire la suite (vedi sotto) e solo allora passare a
CSpect.

## Come far girare l'emulatore con questo gioco

`emu/repl.py` **non riesce** a caricare chomp-chomp con le impostazioni di
serie: usa due euristiche per capire quando è tornato al prompt
(`IDLE_INSTRS = 250_000`, `STEP_CAP = 60_000_000`) e il caricamento le supera,
per cui si ferma **in silenzio, senza errore**. Non è un difetto del sorgente:
anche la versione originale da git si ferma allo stesso modo.

Aggiro la cosa con un driver che importa `repl.py` e alza le soglie a
`IDLE_INSTRS = 5_000_000` / `STEP_CAP = 3_000_000_000`, passando i comandi in
`VF_LINES` separati da `|`. Un giro completo (carica gioco + suite) impiega
~20 minuti, quindi conviene lanciarlo in background.

## Cosa resta da validare su CSpect (Stadio 1)

Lo avvia l'autore (`cspect.bat 4`, poi `Forth18_loader.bas`), la sandbox non può
lanciare GUI.

1. con `tick-frames`=5 la velocità è indistinguibile da prima;
2. i quattro fantasmi si comportano in modo visibilmente diverso;
3. al cambio scatter/chase si girano tutti, a un frame di distanza;
4. da spaventati vanno a caso **e** più lenti (conferma che il gate rotto della
   vecchia riga 1118 è chiuso);
5. nessuno resta incastrato nella casa centrale;
6. `3 TICK-FRAMES !` e `8 TICK-FRAMES !` scalano la velocità in modo pulito.

## Scoperte laterali (non toccate)

- `pill-on` (righa ~119 di `demo/chomp-chomp.f`) è codice morto: definito, mai
  chiamato.
- `tutorial/059-standalone-executables.f` (righe 85-86) e l'intestazione di
  `lib/ZAP.f` documentano `ZAP CHOMP-CHOMP`, ma quella parola non esiste:
  l'entry point è `GAME`. Bug di documentazione reale in due file.
- Esiste una terza copia del gioco residente nei blocchi (`600 LOAD` →
  601/610/630/650/660, maze su 615-616). Decisione presa: **dichiararla
  superata**, senza aggiornarla.
