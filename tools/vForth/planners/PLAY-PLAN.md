# PLAY: le stringhe musicali di NextBASIC sui chip AY

> Stato: IN CORSO. Passo 1 (PLAY bloccante, `lib/PLAY.f`, `help/play.txt`,
> `help/play~.txt`, `test/PLAY-TESTS.f`, cap. 18 della guida) scritto e
> provato sull'emulatore headless il 2026-10-17; resta: ascolto su CSpect o
> sulla macchina, tutorial (o estensione del `034`), passo 2 (in background).

Origine: la voce "A PLAY library" di `TODO.md` (2026-10-17), nata scrivendo
il cap. 18 della guida basic-to-vforth. Fonte del linguaggio: il manuale Next,
cap. 18, pp. 147-153 (`doc/zx-spectrum-next-manual-3rd-ed.md`, "Enhanced Sound
and Music with PLAY").

## 1. Interfaccia

    a1 n1 ... ak nk k PLAY      \ k stringhe, da 1 a 9
    PLAY" testo"                \ una stringa letterale, canale A di AY1

Come in BASIC, la stringa i va al canale i: 1-3 = A, B, C di AY1, 4-6 = AY2,
7-9 = AY3. Con piu' di tre stringhe `PLAY` chiama `ENABLE-TURBOSOUND`. Una
stringa vuota (`PAD 0`) lascia muto il suo canale. `PLAY"` e' state-smart
come `S"`, su cui e' costruito: al prompt suona subito, in una definizione
compila la stringa e `1 PLAY`.

## 2. Decisioni del passo 1

- **Bloccante**, come in BASIC: `PLAY` ritorna a musica finita (o a `H`, o a
  BREAK). E' il primo passo indicato da `TODO.md`; il modo in background e'
  il passo 2 (sez. 5).
- **Tempo in unita' di 1/96 di semibreve**, cosi' anche le terzine sono
  intere: semicroma 6, croma 12, semiminima 24, semibreve 96; terzine 4, 8, 16.
  A T battiti al minuto un'unita' dura 2500/T ms. Il resto della divisione
  si riporta da un'attesa all'altra (`PL-REM`): la terzina di crome a T120
  esce 166, 167, 167 ms, senza deriva.
- **Un parser per canale**, con un record di campi (`PL-FIELD`, 50 byte a
  canale). A ogni giro ogni canale legge la sua stringa fino alla prossima
  nota o pausa; poi si attende la nota piu' corta e la si sottrae a tutte.
  Niente tempo assoluto, quindi niente overflow nelle ripetizioni infinite.
- **Attesa con `MS`** (a pezzi di 100 ms, controllando BREAK fra un pezzo e
  l'altro). `MS` e' un ciclo tarato sulla velocita' della CPU: il tempo di
  lettura delle stringhe si aggiunge, e a 3,5 MHz potrebbe sentirsi. Da
  misurare sulla macchina.
- **Altezze**: O5 `c` e' il Do centrale (nota MIDI 60, la stessa
  numerazione). Una tabella di 12 periodi, 1750000 / (16 f) per le note MIDI
  0-11, scorsa a destra di un bit per ottava con arrotondamento: La 440 = 249,
  Do centrale = 418. Sotto il periodo minimo dell'AY (4095, circa 27 Hz:
  parte di O0 e O1) la nota resta su 4095.
- **Rumore**: su un canale con il rumore acceso (`M`), la nota scrive anche
  il registro 6 con il periodo della nota limitato a 31 (le stesse unita' di
  16 cicli). Il manuale non dice come `PLAY` sceglie il periodo del rumore.
- **Inviluppo**: con `U` ogni nota riscrive il registro 13 e quindi riparte
  l'inviluppo; `V` lo spegne. `W0`-`W7` sono le forme 0, 4, 11, 13, 8, 12, 14,
  10 (tabella del cap. 18 della guida). `X` scrive i registri 11-12; il
  default e' 65535, "the longest".
- **Stereo**: `L`, `R`, `S` riscrivono la porta `$FFFD` con i bit 6 e 5 del
  chip; alla fine `PLAY` rimette entrambi i lati su ogni chip usato e
  riseleziona il chip di `AY` (o AY1).
- **Ripetizioni**: `(` spinge la posizione, il primo `)` torna li', il
  secondo prosegue; un `)` senza `(` aperta ripete dall'inizio una volta,
  quindi `))` in fondo ripete per sempre. Al massimo cinque `(` aperte.
- **`T`** solo nella prima stringa, come da manuale; nelle altre e' letto e
  ignorato. **`Y`, `Z`** (MIDI) letti e ignorati. Gli spazi sono ignorati.
- **Errori** con `?ERROR` e messaggi esistenti, nessun numero riservato:
  #19 "Syntax error." (carattere fuori dal linguaggio, piu' di cinque `(`),
  -24 "Invalid numeric argument." (numero fuori intervallo), #15 BREAK. Prima
  dell'errore i chip vengono zittiti. L'errore arriva quando il parser
  raggiunge il carattere: le note prima sono gia' suonate (BASIC, da
  verificare, potrebbe controllare la stringa prima).
- **Le stringhe devono restare leggibili** per tutta la musica: nel
  dizionario, o nello heap solo se stanno nella stessa pagina da 8K (due
  `S"` interpretati possono finire in pagine diverse).

## 3. Prova sull'emulatore (2026-10-17)

`MS` sostituito prima del caricamento da `: MS ." w" . ;` (stampa le attese)
e scritture sulle porte `$FFFD`/`$BFFD` registrate da Python
(`_bc_port_out`). Tutto come atteso:

| Stringa | Esito |
|---|---|
| `cdeC` | periodi 418, 372, 332, 209; 500 ms ciascuna |
| `11ACE5C 3_5A` | terzine 166/167 ms, `3_5A` 750 ms, `A` = 124 |
| `(((c)))`, `ab)` | 8 note; 4 note |
| `CDEFH` e `O3c))` | il basso ripete finche' `H` non ferma tutto |
| `M56UX5000W1O3c` | reg 7 = 7, reg 11-12 = 5000, reg 6 = 31, vol 16, forma 4 |
| `O5V10cT240 1c&c` | volume 10, 500 ms, poi 62/63 ms, la pausa a volume 0 |
| `cxd`, `V16c` | Syntax error / Invalid numeric argument, chip zittito |
| `: TUNE PLAY" O4ceg" ;` | compila e suona |

## 4. Resta del passo 1

- Ascolto su CSpect o sulla macchina: altezze, durate, stereo, inviluppi,
  rumore, nove canali con Turbosound. In particolare la durata reale di `MS`
  con il parser in mezzo, a 3,5 e a 28 MHz.
- Tutorial nuovo o estensione del `034`.
- Fatti il 2026-10-17: il cap. 18 della guida (con App. B e indice), e
  `test/PLAY-TESTS.f`, silenzioso: `AY!`, `AY!!`, `SHH`, `AYSELECT`,
  `ENABLE-TURBOSOUND`, il `P!` della selezione del chip e `MS` sostituiti
  prima di `INCLUDE lib/PLAY.f`, registri ombra controllati con `T{ }T`
  (altezze, durate, terzine, legature, ripetizioni, canali, inviluppo,
  rumore, stereo). Gli errori non si possono provare con `CATCH` (`ERROR`
  finisce in `QUIT`): elencati in un commento.

## 5. Passo 2: in background (da decidere)

Le stringhe lette in un buffer di scritture di registro, e l'interrupt
(`NEEDS INTERRUPTS`, o il gancio di frame di `NEEDS AFXFRAME`) che ne suona
un passo per frame mentre il programma va avanti. Da verificare che non si
scontri con AFXFRAME sullo stesso chip.
