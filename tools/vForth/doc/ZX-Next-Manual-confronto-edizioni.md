# ZX Spectrum Next User Manual: confronto tra edizione 2020 e terza edizione

Confronto eseguito il 2026-10-11 tra i due file:

- `doc/ZX Spectrum Next Manual Color ONLINE Edition.md` (edizione 2020)
- `doc/zx-spectrum-next-manual-3rd-ed.md` (terza edizione, 2020-2024)

**Fonti della terza edizione:**

- Manuale consultabile online:
  <https://explorer.specnext.dev/documentation/manual/rev3>
- Elenco online dei registri Next, con il dettaglio dei bit:
  <https://explorer.specnext.dev/registers>
- PDF di origine: <https://zxn.gg/zxnmanualrev3> (è il file
  `ZX Spectrum Next Manual 3rd Ed A4 OCR.pdf`, 318 pagine).
- `doc/zx-spectrum-next-manual-3rd-ed.md` è una trascrizione riparata di quel
  PDF: ogni pagina è stata ricontrollata sulla sua immagine, le tabelle sono
  vere tabelle, i punti illeggibili sono marcati `[?]` (73 in tutto, dopo la
  ricostruzione di pagina 242, vedi 6.6) e ogni pagina inizia con
  `<!-- PDF page N -->`.

Una prima stesura di questo confronto usava un `.md` ricavato dal solo testo
OCR del PDF (`util/pdftotext.bat` + `util/txt2md.py`): quel file è stato
eliminato perché superato, e il confronto è stato rifatto sulla trascrizione
riparata. Rispetto alla prima stesura sono cadute due conclusioni sbagliate
(la rimozione di I2S e l'assenza della Hardware Ports List) e si sono potute
confrontare anche le tabelle di riferimento.

**Precisazione sull'edizione più vecchia:** il suo colophon dice *FIRST
EDITION*, copyright 2020 (è la "Color ONLINE Edition"). Il confronto è quindi
tra l'edizione 2020 e la terza edizione, non tra una "seconda" e la terza.

## 1. Struttura generale

| | Edizione 2020 (online) | Terza edizione |
|---|---|---|
| Pagine | 345 | 318 (A4) |
| Capitoli | 26 + Foreword | 25 |
| Appendici | A-D | A-D (stessi titoli) |
| Parole nel corpo | circa 150.000 | circa 155.000 |
| Hardware descritto | solo Issue 2 | Issue 2 e Issue 4 |

- **Tolti**: il Foreword (storia del progetto e del Kickstarter), la dedica a
  Rick Dickinson e l'intero capitolo 1 "Introduction" (modelli, montaggio,
  tastiera, menu di avvio, editor NextBASIC). La terza edizione rimanda per
  questo a una *Quick Start Guide* separata.
- **Rinumerazione**: tutti i capitoli scalano di uno (il vecchio 2 "Basic
  Programming Concepts" è ora l'1, e così via fino a 26 -> 25).
- **Volume**: le 25 pagine introduttive tolte sono state più che rimpiazzate
  da contenuto tecnico nuovo.
- **Aggiunti in coda**: Acknowledgements e una scheda tecnica doppia, Issue 2
  e Issue 4.

### Corrispondenza dei capitoli

| Edizione 2020 | Terza edizione | Titolo |
|---|---|---|
| Foreword | -- | (tolto) |
| 1 | -- | Introduction (tolto, ora nella Quick Start Guide) |
| 2 | 1 | Basic Programming Concepts |
| 3 | 2 | Decisions |
| 4 | 3 | Looping |
| 5 | 4 | Procedures and Subroutines |
| 6 | 5 | READ, DATA, RESTORE |
| 7 | 6 | Expressions |
| 8 | 7 | Strings |
| 9 | 8 | Functions |
| 10 | 9 | Mathematical Functions |
| 11 | 10 | Random Numbers |
| 12 | 11 | Arrays |
| 13 | 12 | Conditions |
| 14 | 13 | The Character Set |
| 15 | 14 | More about PRINT and INPUT |
| 16 | 15 | Colours |
| 17 | 16 | Graphics |
| 18 | 17 | Time and Motion |
| 19 | 18 | Sound and Music |
| 20 | 19 | NextZXOS and alternatives |
| 21 | 20 | Channels, Streams, Drivers and Windows |
| 22 | 21 | Optional Features |
| 23 | 22 | IN, OUT and the Next Registers |
| 24 | 23 | The Memory |
| 25 | 24 | The System Variables |
| 26 | 25 | Using Machine Code |

## 2. Novità di NextBASIC (assenti nell'edizione 2020)

I numeri di capitolo sono quelli della terza edizione.

- **Cap. 1**: sezione "Labels" (etichette `@nome` come destinazione di salto:
  18 occorrenze contro 1), assegnazioni multiple con `LET` facoltativo (`LET`
  compare 43 volte contro 233).
- **Cap. 2 Decisions**: selezione di caso con `ON`, operatore di selezione
  `?`, `ENDIF`.
- **Cap. 3 Looping**: `EXIT` per uscire in modo pulito da un ciclo.
- **Cap. 4 Procedures**:
  - `PRIVATE` e `PRIVATE CLEAR` (variabili persistenti tra le chiamate);
  - passaggio per riferimento con `REF`;
  - parametri extra letti con `DATA`/`READ`;
  - sezione "Trapping errors locally".
- **Cap. 5**: `DATA` usata come funzione (tipo del prossimo dato).
- **Cap. 6**: sezione "Order of mathematical calculations".
- **Cap. 7 Strings**: moltiplicazione di stringa `a$*n`, modificatori in coda
  `a$[...]` (maiuscole/minuscole, trim, bit 7), tokenizzazione con `{a$}`.
- **Cap. 8 e 11**: sezioni "Order of calculations using functions" e
  "VAL and VAL$"; `DIM` come funzione (dimensioni di un array).
- **Cap. 14**: sezione "Using INPUT for game controllers" (`INPUT n` come
  funzione che legge lo stato di un controller).
- **Cap. 17**: `TIME` come comando e funzione, `TIME$`.
- **Compare anche** `USR$`, assente nel 2020.

## 3. Grafica, sprite, suono

- **Sprite (cap. 17)**: è la parte più ampliata. Nel 2020 non compaiono
  affatto:
  - `SPRITE MOVE`, `SPRITE MOVE INT`, `SPRITE RUN`;
  - modalità batch (`SPRITE STOP`);
  - movimento automatico: `SPRITE CONTINUE`, `SPRITE PAUSE`;
  - funzioni sprite: `SPRITE CONTINUE s`, `SPRITE AT(s,c)`,
    `SPRITE OVER(...)` per le collisioni;
  - sprite compositi e unificati.
- **Grafica (cap. 16)**: nuova sezione "Accessing non-supported graphics
  modes", cioè come usare Layer 2 320x256 e 640x256 da BASIC con `REG` e
  `BANK POKE`.
- **Suono (cap. 18)**: la riproduzione WAV passa da `.wavplay` a
  `.wavplay32`.
- **I2S**: invariato (17 occorrenze contro 18); sparisce solo il registro
  `$A3` (vedi punto 6).

## 4. NextZXOS (cap. 19)

- La voce di menu "48K BASIC" è sostituita da "ZX80 and ZX81 BASIC"
  (emulatori di Paul Farrow).
- **Dot-command**: la sezione "NextZXOS dot commands" ne descrive 16 contro
  9. Nuovi: `.browseprefs`, `.editprefs`, `.cpm`, `.guide` (`.gde`),
  `.zip`, `.unzip`; nessuno di quelli del 2020 è stato tolto. Altrove nel
  testo compaiono anche `.nexload`, `.playpt3`, `.nxmod`.
- Nei crediti compaiono software nuovi: NextPi2, SPUI, QE, NextGuide, Odin,
  ZXDB-dl, SpectraMon.

## 5. Hardware (cap. 21-22)

- **Issue 4**: il cap. 21 distingue ora le due schede (18 menzioni contro
  zero). Su Issue 4 RTC, WiFi e 2 MB di RAM sono di serie e l'FPGA è un
  Artix-7 XC7A15T anziché Spartan-6 XC6SLX16. Sezioni nuove: "Installation
  (for Issue 2 mainboards)", "Raspberry Pi Zero installation on the Issue 4
  mainboard", "Using .time and .date".
- **Cap. 22**: nuove sezioni "Accessing the ZX Spectrum Next features with
  NextREG" (porte `$243B` / `$253B`) e "Memory Mapping Modes". Le menzioni di
  "Pentagon" passano da 3 a 27.
- **"The ZX Spectrum Next Hardware Ports List"**: presente in entrambe le
  edizioni, due facciate (pagine 273-274 nel 2020, 244-245 nella terza). La
  prima facciata è sostanzialmente uguale; la seconda ha porte in più:

  | Porta | Nome | Nota |
  |---|---|---|
  | 49141 (`$BFF5`) | PSG Info | nuova |
  | 5691 (`$163B`) | UART Frame | nuova |
  | 11 (`$0B`) | Z80DMA | affianca la 107 (`$6B`) zxnDMA, già presente |

  Cambia anche la nota delle porte non elencate: si aggiunge 61431 (`$EFF7`)
  e c'è un rinvio al documento `ports.txt` della distribuzione System/Next.
- **Registri Next**: 42 nuovi e uno tolto; confronto completo al punto 6.
- **Interrupt**: il CTC a 8 canali è nominato 37 volte contro zero, e le
  menzioni di DMA passano da 12 a 30.

## 6. I registri Next in dettaglio ("The Next Registers")

Metodo: l'elenco della terza edizione è stato letto a vista dalle pagine
234-242 del PDF, rese in immagine con `pdftoppm`, e poi riscontrato sulla
trascrizione riparata: coincide. Alcuni titoli sono tagliati nella scansione
stessa (in cima alle colonne e sul margine sinistro di pagina 242); quei
registri sono stati identificati dal contenuto delle tabelle e, per pagina
242, dall'elenco online (vedi 6.6).

### 6.1 Numeri

| | Edizione 2020 | Terza edizione |
|---|---|---|
| Pagine dedicate | 7 (266-272) | 9 (234-242) |
| Registri documentati | 105 | 146 |
| Registri nuovi | -- | 42 |
| Registri tolti | -- | 1 |

Tutti i registri del 2020 sono ancora presenti, tranne uno.

### 6.2 Registri nuovi (assenti nel 2020)

| NextREG | Nome | Cosa fa |
|---|---|---|
| `$0A` (10) | Peripheral 5 Settings | risoluzione e scambio tasti del mouse, divMMC automap, tipo di Multiface |
| `$0B` (11) | Joystick Port Mode Selection | porte joystick in modo I/O: bit bang, clock, UART |
| `$0F` (15) | Board ID | revisione scheda: Issue 2, 3, 4 |
| `$20` (32) | Maskable Interrupt Generation | genera via software interrupt CTC 0-3, ULA, Line |
| `$24` (36) | Reserved | protezione contro `OUT $3B,A` (interfaccia DISCiPLE) |
| `$64` (100) | Vertical Line Count Offset | sposta il conteggio di linea per Copper e line interrupt |
| `$70` (112) | Layer 2 Resolution Control | 256x192 8bpp, 320x256 8bpp, 640x256 4bpp; offset palette |
| `$71` (113) | Layer 2 Horizontal Scroll Control MSB | nono bit dello scroll X (0-511) |
| `$8E` (142) | ZX Spectrum 128K Memory Mapping | accesso unificato alle porte `$7FFD`, `$DFFD`, `$1FFD` |
| `$8F` (143) | Memory Mapping Mode Control | standard 128K/+3, Pentagon 512K, Pentagon 1024K |
| `$A8` (168) | ESP WiFi GPIO Output Control | abilita l'uscita su GPIO0/GPIO2 |
| `$A9` (169) | ESP WiFi GPIO Control | lettura/scrittura di GPIO0/GPIO2 |
| `$B0` (176) | Extended Keys 0 | stato dei tasti freccia e dei tasti di punteggiatura |
| `$B1` (177) | Extended Keys 1 | EXTEND, CAPS LOCK, GRAPH, TRUE/INV VIDEO, BREAK, EDIT, DELETE |
| `$B2` (178) | Extended MD Pad Buttons | pulsanti MODE/X/Y/Z dei due pad Mega Drive |
| `$B8` (184) | divMMC Entry Points 0 | automap sugli indirizzi `$0000`-`$0038` |
| `$B9` (185) | divMMC Entry Points Valid 0 | validità dei punti d'ingresso |
| `$BA` (186) | divMMC Entry Points Timing Control 0 | mappatura immediata o ritardata |
| `$BB` (187) | divMMC Entry Points 1 | `$0066`, trappole nastro, `$1FF8`-`$1FFF`, `$3Dxx` |
| `$C0` (192) | Interrupt Control | modo IM2 hardware, parte programmabile del vettore, NMI stackless |
| `$C2` (194) | NMI Return Address LSB | |
| `$C3` (195) | NMI Return Address MSB | |
| `$C4` (196) | Interrupt Enables 0 | ULA, Line, bus di espansione |
| `$C5` (197) | Interrupt Enables 1 | CTC canali 0-7 |
| `$C6` (198) | Interrupt Enables 2 | UART 0 e 1 (Rx, Rx near-full, Tx) |
| `$C7` (199) | Reserved | |
| `$C8` (200) | Interrupt Status 0 | titolo tagliato nella scansione, vedi 6.6 |
| `$C9` (201) | Interrupt Status 1 | |
| `$CA` (202) | Interrupt Status 2 | |
| `$CB` (203) | Reserved | |
| `$CC` (204) | DMA Interrupt Enables 0 | quali interrupt possono interrompere il DMA |
| `$CD` (205) | DMA Interrupt Enables 1 | |
| `$CE` (206) | DMA Interrupt Enables 2 | |
| `$CF` (207) | Reserved | scrivere 0; titolo tagliato nella scansione, vedi 6.6 |
| `$D8` (216) | I/O Traps (Experimental) | trappola sulle porte del FDC +3 |
| `$D9` (217) | I/O Traps Write (Experimental) | dato scritto nel ciclo intrappolato |
| `$DA` (218) | I/O Trap Cause (Experimental) | causa della trappola |
| `$F0` (240) | XDEV | solo Issue 4: selezione DNA / XADC Xilinx |
| `$F8` (248) | XADC Register | solo Issue 4 |
| `$F9` (249) | XADC D0 | solo Issue 4 |
| `$FA` (250) | XADC D1 | solo Issue 4 |
| `$FF` (255) | Reserved (Internal Use Only) | |

Raggruppati per tema:

- **Interrupt**: `$20`, `$C0`, `$C2`-`$CE`. È il blocco più consistente e non
  esisteva affatto nel 2020: IM2 hardware con vettore per sorgente (Line,
  UART, CTC 0-7, ULA), abilitazioni, stato, interazione col DMA.
- **Layer 2**: `$70` e `$71`. Nel 2020 il registro di risoluzione non c'era:
  i modi 320x256 e 640x256 non erano documentati a livello di registri.
- **Memoria**: `$8E`, `$8F`.
- **Tastiera e controller**: `$0B`, `$B0`-`$B2`.
- **divMMC**: `$B8`-`$BB`.
- **Periferiche e scheda**: `$0A`, `$0F`, `$A8`, `$A9`, `$F0`, `$F8`-`$FA`.

### 6.3 Registro tolto

| NextREG | Nome nel 2020 |
|---|---|
| `$A3` (163) | Pi0 I2S Clock Divide (Master Mode) |

### 6.4 Registri comuni con contenuto cambiato

Differenze rilevate confrontando le tabelle dei bit; l'elenco non è
esaustivo.

| NextREG | Differenza |
|---|---|
| `$00` Machine ID | via DE1A, DE2A, FBLABS, VTRUCCO, WXEDA, Multicore; entrano UnAmiga, UnAmiga Reloaded, SiDi, MiST, MiSTer, ZX-DOS/gomaDOS |
| `$02` Reset | nuovi bit per sorgente e generazione di NMI divMMC e Multiface, legati agli I/O trap |
| `$05` Peripheral 1 | nuovo modo joystick "User Defined Keys" (programmato via keymap PS/2); i tasti associati a Sinclair 1 e 2 sono scambiati rispetto al 2020 (ora Sinclair 2 = 12345, Sinclair 1 = 67890) |
| `$06` Peripheral 2 | sparisce il bit "DMA Mode" (zxnDMA/Z80DMA: ora la scelta è la porta, `$6B` o `$0B`); nuovo bit "Internal Speaker BEEP"; il bit 4 riguarda solo il pulsante NMI divMMC (l'automap passa a `$0A`); gli hotkey diventano F5/F6/F8 |
| `$09` Peripheral 4 | intensità scanline 50 / 25 / 12,5% (erano 75 / 50 / 25%) |
| `$16` Layer 2 X Scroll | diventa "LSB", con MSB in `$71` |
| `$22` Line Interrupt Control | i bit di abilitazione sono dichiarati alias di `$C4` |
| `$28` Keymap Address MSB | nuovo bit di selezione "PS/2 keymap / key joystick" |
| `$68` ULA Control | nuovo bit "Extended keys in 8x5 matrix" (annulla l'inserimento in matrice); la miscelazione colore passa da 1 a 2 bit (ULA, ULA+Tilemap, Tilemap, nessuna) |
| `$85`, `$89` Port Decoding 4/4 | oltre a ULAplus compaiono DMA su porta `$0B` (Z80DMA), memoria Pentagon 1024 (`$EFF7`), CTC (`$183B`-`$1F3B`), modo di reset del registro |
| `$8A` I/O Propagate | aggiunta la porta `$EFF7` |
| `$A0` PI Peripheral Enable | nota nuova: GPIO 16/17 come RTR/CTS col controllo di flusso hardware |

Cambia anche la nomenclatura: "Layer 3" diventa ovunque "Layer 3 (Tilemap)"
e "Megadrive" diventa "MD" / "Mega Drive".

### 6.5 Ricadute su vForth

- `$C0`, `$C4`-`$C6`: sono i registri che `dev/IM2-HW.f` usa; la terza
  edizione è la prima a documentarli, insieme a stato (`$C8`-`$CA`) e
  generazione software (`$20`).
- `$CC`-`$CE` e la porta `$0B`: rilevanti per `lib/DMA.f` (interrupt durante
  un trasferimento, scelta zxnDMA / Z80DMA).
- `$70`, `$71`: i registri dei modi `LAYER22` e `LAYER24`
  (`lib/LAYER22-GRAPHICS.f`, `lib/LAYER24-GRAPHICS.f`).
- `$B0`, `$B1`: tasti estesi leggibili direttamente, alternativa alla
  scansione di matrice della libreria `KEYBOARD`; il bit 4 di `$68` impedisce
  che quei tasti entrino nella matrice 8x5.

### 6.6 Ricostruzione della pagina 242 (margine tagliato)

Nel PDF la pagina 242 ha il margine sinistro tagliato: della colonna di
sinistra mancano la colonna "Group Name" e l'inizio dei titoli. Il contenuto
è stato ricostruito dall'elenco online dei registri,
<https://explorer.specnext.dev/registers>, e coincide con i bit visibili nella
pagina (numero e posizione dei bit, bit riservati).

| NextREG | Nome | Bit |
|---|---|---|
| `$C8` (200) | Interrupt Status 0 | 7:2 riservati (0); 1 Line; 0 ULA |
| `$C9` (201) | Interrupt Status 1 | 7:0 CTC canali 7-0 (zero count / time-out) |
| `$CA` (202) | Interrupt Status 2 | 7 riservato; 6 UART1 Tx empty; 5 UART1 Rx half full; 4 UART1 Rx available; 3 riservato; 2 UART0 Tx empty; 1 UART0 Rx half full; 0 UART0 Rx available |
| `$CB` (203) | Reserved | scrivere `$FF` |
| `$CC` (204) | DMA Interrupt Enables 0 | 7 NMI; 1 Line; 0 ULA |
| `$CD` (205) | DMA Interrupt Enables 1 | 7:0 CTC canali 7-0 |
| `$CE` (206) | DMA Interrupt Enables 2 | stessa disposizione di `$CA` (UART1 nei bit 6:4, UART0 nei bit 2:0) |
| `$CF` (207) | Reserved | scrivere 0 |

- **Registri di stato** (`$C8`-`$CA`): in lettura un bit a 1 indica che il
  dispositivo ha generato un interrupt o ne ha uno pendente; scrivere 1
  azzera lo stato. In modo IM2 hardware lo stato resta a 1 finché la
  condizione pendente non cessa.
- **Registri DMA** (`$CC`-`$CE`): un bit a 1 permette a quell'interrupt di
  interrompere un'operazione DMA, in modo IM2 hardware. Reset a 0.

L'elenco online usa nomi abbreviati ("INT EN 0", "INT Status 0", "DMA INT EN
0") e dà `$F0` e `$F8`-`$FA` come validi per "Issues 4 & 5", dove il manuale
dice "Issue 4 only".

#### Cosa è stato ripristinato nella trascrizione

La ricostruzione è stata riportata anche in
`doc/zx-spectrum-next-manual-3rd-ed.md`: la pagina 242 non ha più nessun
`[?]` (nel file ne restano 73, erano 148). In cima alla pagina un commento
HTML ("Reconstruction note") dichiara la ricostruzione e le sue fonti, così
resta distinguibile dalla trascrizione fedele.

| Parte tagliata | Ripristinata come | Fonte |
|---|---|---|
| Titoli di `$C8`-`$CE` | `NextREG 200 (C8h) – Interrupt Status 0` ... `NextREG 206 (CEh) – DMA Interrupt Enables 2` | elenco online, nella forma dei titoli di pagina 241 |
| Titolo di `$CF` | `NextREG 207 (CFh) – Reserved` | elenco online (nel PDF il titolo manca del tutto) |
| Intestazione della prima colonna | `Group Name` | tabelle di `$C4`-`$C6` a pagina 241 |
| Nomi di `$C8` | ULA, Line, Reserved | elenco online |
| Nomi di `$C9` e `$CD` | CTC Channel 0-7 ZC/TO | stile di `$C5` a pagina 241 |
| Nomi di `$CA` e `$CE` | UART 0 / UART 1: Rx available, Rx near-full, Tx empty; due Reserved | stile di `$C6` a pagina 241 |
| Nomi di `$CB` | Reserved | elenco online |
| Nomi di `$CC` | ULA, Line, NMI | elenco online |
| Inizio delle righe di nota | vedi sotto | senso della frase |

Bit, colori delle celle, descrizioni e valori di reset non sono stati
toccati: sono quelli stampati sulla pagina.

#### Differenze tra manuale ed elenco online

- **Nomi dei registri**: il manuale li scrive per esteso ("Interrupt Status
  0", "DMA Interrupt Enables 0"), l'elenco online li abbrevia ("INT Status
  0", "DMA INT EN 0"). Nella trascrizione vale la forma del manuale.
- **Soglia di ricezione UART**: l'elenco online dice "Rx half full", il
  manuale a pagina 241 (`$C6`) dice "Rx near-full". Nella trascrizione è
  stata usata la dizione del manuale.
- **Canali CTC**: nella trascrizione hanno la forma che il manuale usa per
  `$C5` a pagina 241, "CTC Channel n ZC/TO" (zero count / time-out), una
  riga per canale.
- **`$CF`**: nel PDF la tabella c'è ma è senza titolo; il numero e il nome
  "Reserved" vengono solo dall'elenco online e dalla posizione nella pagina,
  tra `$CE` e `$D8`.
- **Schede**: "Issues 4 & 5" online contro "Issue 4 only" nel manuale per
  `$F0` e `$F8`-`$FA` (pagina 242, colonna destra, non tagliata).

#### Parti congetturali

Del testo stampato restava solo la coda di ogni riga, quindi le parole
iniziali delle note sono ricostruite dal senso e non sono il testo certo del
manuale:

| Resto leggibile sulla pagina | Ricostruito come |
|---|---|
| "...g, set bits indicate that the device generated an interrupt..." | "When reading, set bits indicate..." |
| "..., set bits clear the status." | "When writing, set bits clear the status." |
| "...ate the corresponding interrupt will interrupt a DMA operation..." | "Set bits indicate the corresponding interrupt..." |
| "...Fh)" (nota di `$CB`) | "Write 255 (FFh)" |
| "...upt" su due righe (note 1 e 2 di `$CA`) | "Shared interrupt", per analogia con `$C6` |

Sotto la tabella di `$CE` la pagina non riporta note numerate: i nomi UART
sono quindi senza richiami di nota, a differenza di `$CA`.

## 7. Tabelle di riferimento (cap. 24 e Appendice B)

### 7.1 Variabili di sistema

Le tabelle hanno 114 voci nel 2020 e 111 nella terza. Differenze:

| Indirizzo | Edizione 2020 | Terza edizione |
|---|---|---|
| `$5B58` (23384) | `TARGET` | `CACHEBNK` (pagina 8K con i dati di programma in cache) |
| `$5C0B` (23563) | `DEFADD` | `RETVARS` (indirizzo delle variabili locali sullo stack di ritorno) |
| `$5C3F` (23615) | `LISTSP` | riservato al sistema |
| `$5C44` (23620) | `NSPPC` | riservato al sistema |
| `$5C6C` (23660) | `S_TOP` | riservato al sistema |

Nel 2020 `NXTLIN` (23637) è dato in esadecimale come `$5C57`; la terza lo dà
come `$5C55`, che è il valore giusto per 23637: era un refuso.

### 7.2 Messaggi d'errore

Due rapporti nuovi nella tabella "General Errors": `No ENDIF` e `No label`.
Il resto della tabella coincide.

### 7.3 Parole chiave e funzioni

La tabella "NextBASIC Keywords and Functions" della terza edizione elenca
anche le funzioni classiche (`SIN`, `COS`, `TAN`, `LN`, `SQR`, `SGN`, `INT`,
`LEN`, `STR$`, `VAL`, `VAL$`, `PEEK`, `DPEEK`, `PEEK$`, `INKEY$`, `BIN`,
`PI`), che nella tabella del 2020 non c'erano.

## 8. Cosa non è stato confrontato

- **Registri Next**: l'elenco al punto 6 è completo, ma il confronto bit per
  bit dei registri comuni copre solo quelli citati lì; gli altri possono
  avere differenze minori non rilevate.
- **Prosa**: il confronto è per titoli, parole chiave e tabelle. I capitoli
  9, 10, 12, 13, 23 e 25 e le appendici A, C, D (numerazione della terza)
  hanno gli stessi titoli di sezione e non mostrano differenze evidenti, ma
  la prosa non è stata confrontata paragrafo per paragrafo.
- **Set di caratteri e mnemonici Z80N** (Appendice A): non confrontati.
