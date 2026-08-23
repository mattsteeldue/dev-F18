# chomp-chomp: stato della revisione (agg. 2026-08-23, sessione 2)

Nota di ripresa per continuare il lavoro da un'altra sessione.
Piano approvato completo: `C:\Users\matteo\.claude\plans\glowing-mixing-haven.md`
(4 stadi: AI+pacing, colori ciclici, font in RAM, labirinti su Screen).

## Dove siamo

**Stadio 1 (AI dei fantasmi + pacing) — codice completo, aritmetica validata
dalla suite nell'emulatore, resta solo la prova di giocabilita' su CSpect.**
Stadi 2, 3 e 4 non iniziati.

Branch: `chomp-chomp-ghost-ai`. Il commit 44f1fc9 porta lo Stadio 1; sopra ci
sono le correzioni della suite descritte piu' sotto (non ancora committate).

| File | Stato |
|---|---|
| `demo/chomp-chomp.f` | Stadio 1 completo, invariato dal commit |
| `demo/README.txt` | voce riscritta: non dice piu' "ghosts movement are completely random" |
| `test/CHOMP-AI-TESTS.f` | ~45 asserzioni, **tutte verdi**, stack vuoto |
| `lib/ZAP.f`, `tutorial/059-standalone-executables.f` | corretto `ZAP CHOMP-CHOMP` -> `ZAP GAME` |

Non ancora fatto (previsto dal piano a fine lavoro): ricopiare il master su
`demo/chomp-chomp/chomp-chomp.f` (oggi divergono: la copia e' la versione
pre-modifica del 7 giugno) e rigenerare i `.bin` standalone con `ZAP GAME`
(solo a mano, da sessione vForth viva). **Vanno fatti insieme**: copiare il
sorgente senza rigenerare i binari renderebbe quella directory incoerente.
Resta anche la nota "superata" sullo Screen 600.

## Cosa e' verificato

- Nessun riferimento in avanti fra le nuove parole; nessuna collisione di nome
  con parole core.
- File ASCII a 7 bit, niente TAB, terminazione conforme alla regola di `INCLUDE`.
- **`INCLUDE demo/chomp-chomp.f` compila da cima a fondo nell'emulatore
  headless**, tutti i banner inclusi il nuovo `Chomp.f - scatter/chase`.
- **L'aritmetica dell'AI e' verificata**: run del 2026-08-23, 2443 s totali,
  tutte le asserzioni passano e `.S` finale non stampa nulla, cioe' stack
  vuoto. L'unico messaggio nel log e' `ERROR msg#4` = "has already been
  defined.", che e' benigno: `lib/testing.f:50` fa `: ERROR ERROR-XT @
  EXECUTE ;` e quindi ridefinisce l'`ERROR` del core. Un fallimento sarebbe
  stato rumoroso — il gestore vettorizzato `ERROR1` stampa la riga sorgente,
  poi `MESSAGE` (`msg#50` "Incorrect result." o `msg#54`) e `.S` — e non fa
  `QUIT`, quindi li avrebbe elencati tutti.

## Correzioni applicate alla suite (sessione 2)

I due difetti previsti, piu' un terzo che non era stato visto.

1. **Mancava `DECIMAL`.** Confermato: `lib/testing.f` finisce con
   `HEX 24 CONSTANT MAX-BASE` / `HEX 20 CONSTANT #BITS-UD` e non ripristina la
   base. Aggiunto `DECIMAL` subito dopo `NEEDS TESTING`, come fanno
   `FIXED88-TESTS.f` e `FLOATING-TESTS.f` (e come fa `CORE-TESTS.f` all'inverso,
   con un `HEX` esplicito).
2. **`DO...LOOP` in interpretazione.** Incapsulato in
   `: run-ticks ( n -- ) 0 ?do tick-phase loop ;`.
3. **La sezione 5 (`choose-dir`) era sbagliata in 3 asserzioni su 5** — errore
   nel file di test, non nel gioco. Le premesse sul labirinto erano false:
   (5,10) e' `.` e non un muro, quindi *up* vinceva; e (4,5), la presunta
   "sacca sigillata", e' `J`, cioe' **esso stesso un muro**.

   L'indicizzazione di `maze^` e': riga 1-based, colonna 1-based sul primo
   carattere visibile (l'offset 0 e' il byte di conteggio della stringa `,"`,
   il 23 e' il NUL; passo 24). Tre ancore indipendenti la confermano: le tre
   celle interne della casa dei fantasmi a (12,10..12), la porta `-` a
   (11,11) e il buco nei puntini dove parte Pac-Man a (14,12).

   Celle sostitutive, simulate prima di scriverle:
   - **(6,4)** — corridoio della riga 6 con `B` sopra e `C` sotto: solo
     sinistra/destra aperte. Copre "lato piu' vicino", "pareggio" e "niente
     inversione volontaria". Il pareggio vale ancora 26, come nel commento
     originale.
   - **(12,2)** — bocca del tunnel sinistro: per i fantasmi e' un vicolo cieco
     vero, perche' `/` sta in `?pac-trail` ma **non** in `?ghost-trail`.
4. L'intestazione prometteva "the suite calls init-all at the end" senza farlo.
   Ora lo fa davvero: `init-all` ripristina posizioni, accumulatori, `hunt` e
   le fasi, cioe' tutto quello che i test sporcano.

## Come far girare l'emulatore con questo gioco

`emu/repl.py` **non riesce** a caricare chomp-chomp con le impostazioni di
serie: usa due euristiche per capire quando è tornato al prompt
(`IDLE_INSTRS = 250_000`, `STEP_CAP = 60_000_000`) e il caricamento le supera,
per cui si ferma **in silenzio, senza errore**. Non è un difetto del sorgente:
anche la versione originale da git si ferma allo stesso modo.

Aggiro la cosa con un driver che importa `repl.py` e alza le soglie a
`IDLE_INSTRS = 5_000_000` / `STEP_CAP = 3_000_000_000`, passando i comandi in
`VF_LINES` separati da `|`. Un giro completo (boot + gioco + suite) ha impiegato
**2443 s, ~41 minuti** il 2026-08-23 (boot 236 s, gioco 282 s, suite 1289 s),
quindi va lanciato in background. Attenzione a non aspettarlo con un
`while pgrep -f <nome-script>`: la riga di comando del watcher contiene essa
stessa il nome dello script, quindi pgrep matcha se' stesso e il ciclo non
esce mai.

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

## Scoperte laterali

- **RISOLTO 2026-08-23.** `tutorial/059-standalone-executables.f` (riga 86) e
  l'intestazione di `lib/ZAP.f` documentavano `ZAP CHOMP-CHOMP`, ma quella
  parola non esiste: l'entry point e' `GAME`. Corretti entrambi in `ZAP GAME`.
  Era un'incoerenza interna al tutorial stesso, che gia' alla riga 104 diceva
  "produced by `ZAP GAME`" e elenca `game-core.bin`.
- (non toccato) `pill-on` (riga ~119 di `demo/chomp-chomp.f`) è codice morto:
  definito, mai chiamato.
- (non toccato) Esiste una terza copia del gioco residente nei blocchi (`600 LOAD` →
  601/610/630/650/660, maze su 615-616). Decisione presa: **dichiararla
  superata**, senza aggiornarla.
