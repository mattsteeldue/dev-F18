# ZAP: stato dell'arte e piano di messa a punto

> Stato: IN CORSO (sessione chiusa il 2026-10-07, ripresa da qui).
> FATTE: fase 0 (test headless), fase 1 (`lib/ZAP.f`, confermata su CSpect con
> chomp-chomp), fase 2 (loader con `DPEEK`, confermata su CSpect), fase 3 lato
> Forth (`SAVE-BANK`, verde in emulatore, non ancora su CSpect).
> RESTA, in ordine: (a) fase 3 lato loader -- righe BASIC nell'esito della fase 3;
> (b) chomp-chomp Stadio 5, senza il quale lo standalone si ferma al secondo
> schema (vedi "Sessione 2026-10-07" qui sotto); (c) fase 4 in poi;
> (d) `util/bas2txt.py`. Decisioni D1-D4 in sez. 5. Build core 2026-09-26.

## Sessione 2026-10-07: cosa si è visto su CSpect

- `demo/chomp-chomp/game-*.bin` rigenerati con core e `ZAP` correnti (`R0` 53652,
  `WARNING` 0, `COLD`/`ERROR`/`ABORT` -> `BYE`) e `game.bas` con `DPEEK`: il gioco
  carica e funziona, punteggio compreso.
- **Alla fine del primo schema esce a BASIC** con `bye? msg#45` (#45 = "NextZXOS
  Pos error") e poi lo `STOP` della riga 1220. Non è un difetto di `ZAP`: dallo
  Stadio 4 `set-maze-run` chiama `BLOCK` per i livelli >= 1 e lo standalone non
  apre `!Blocks-64.bin` (`CHOMP-CHOMP-PLAN.md`, nota alla sez. 6.4). L'uscita con
  `BYE` è la decisione D1 che lavora; il messaggio resta leggibile a schermo.
  Rimedio: Stadio 5 (labirinti nel banco 19, poi `19 SAVE-BANK` dopo `ZAP GAME`
  e una riga `LOAD ... BANK 19` in `game.bas`).
- `ZAP` scrive i `.bin` nella directory da cui è partito vForth, non accanto al
  sorgente: vanno spostati a mano in `demo/chomp-chomp/` (lo risolve la fase 5).
- `game-core.bin` è passato da 16023 a 21038 byte: `ZAP` (circa 0,9 KB) più le
  utility caricate all'avvio. Fino alla fase 4, lanciare `ZAP GAME` da una
  sessione senza utility.

Piano ombrello su `ZAP` (tre `.bin` + loader BASIC) e `ZAP"` (`.nex`).
Il progetto di dettaglio del loader generato e dello Screen interpretativo resta in
`planners/ZAP-BASIC-LOADER-PLAN.md` (rev. 3 del 2026-09-17): qui se ne riusa il
contenuto valido e si segnalano i punti che il core ha nel frattempo superato (sez. 6).

---

## 1. Stato dell'arte (verificato oggi sui binari correnti)

Misure fatte con `emu/repl.py` su build 2026-09-26, sessione pulita, parola di prova
`: ZZT 65 EMIT ;`, poi `NEEDS ZAP` e `ZAP ZZT`.

| Fatto | Valore | Come è stato verificato |
|---|---|---|
| `lib/ZAP.f` si carica e gira | scrive `ZZT-core.bin` 8316, `ZZT-user.bin` 3692, `ZZT-heap.bin` 16384 | file prodotti e ispezionati |
| Patch di `COLD` | corpo = `[xt ZZT] [BYE] LIT ...` al posto di `NOOP NOOP` (slot previsto apposta in `L3.asm`) | letto in `ZZT-core.bin` a `$75CD` |
| Costo di `NEEDS ZAP` | 611 byte di code space, 234 di heap | `HERE` 33151 -> 33762, `HP@` 3330 -> 3564 |
| `ZAP` finisce dentro il deliverable | sì: `SAVE-CORE` salva fino a `HERE` | 8316 = 33762 - 25446 |
| `ORIGIN` / `R0 @` / `S0 @` / `FIRST @` | 25446 / **53652** / 53492 / 53732 | emulatore |
| Indirizzo di `user.bin` nel loader | **53640** in `Standard-Loader.bas` e in `demo/chomp-chomp/game.bas` | detokenizzati (riga 1160) |
| Buffer nello snapshot | BLOCK 11-16 più **BLOCK 1** (pinnato, perché `NEEDS` è un `INCLUDE`) | intestazioni dei 7 buffer in `ZZT-user.bin` |
| `ZAP"`: PC nell'header `.nex` | `$7634` cablato; oggi `ColdRoutine` è `$762B` e `$7634` cade **a metà** di `ld sp,(S0_origin)` (`$7632`) | `list/main.lst` |
| `ZAP"`: patch di `COLD` | commentata: l'xt resta sullo stack | sorgente |
| Documentazione | tutorial 059 presente; **nessun** `help/zap.txt` né per `ZAP"`; `help/open}.txt` descrive `OPEN>` come "parte di ZAP" | `ls help` |

## 2. Difetti, in ordine di gravità

1. **Il loader carica `user.bin` all'indirizzo sbagliato.** Il file parte da `R0 @`
   (53652 oggi; 54168 nello snapshot chomp-chomp del 2026-08-23, i cui primi byte
   contengono proprio `R0 = $D398`), ma entrambi i `.bas` dicono 53640. Lo scarto è 12
   byte oggi, 528 in agosto. `ColdRoutine` prende `SP`/`RP` da `ORIGIN`, ma il `COLD`
   patchato **salta** la copia delle variabili utente da `ORIGIN` (i 22 byte dopo lo
   slot), quindi `BASE`, `DP`, `WARNING`... valgono ciò che il loader ha messo a `R0`:
   byte sfasati. `ZAP` stampa l'indirizzo giusto (`SAVE "USER" CODE 53652 3692`), ma
   nessuno lo riporta nel loader. *Dedotto dai byte, non osservato su macchina*: lo
   standalone di chomp-chomp risulta "confermato", quindi o è stato provato con un
   loader corretto a mano e mai salvato nel repo, o il gioco tollera il danno. È la
   prima cosa da chiarire (fase 0).
2. **`ZAP"` produce un `.nex` che non può partire** (PC a metà istruzione) e che
   comunque non lancerebbe la parola scelta (patch commentata).
3. **Messaggi d'errore nello standalone: ne restano 6 blocchi su 10.** `17 8 DO`
   legge i BLOCK 8..16 (il 17 manca) in 7 buffer di cui uno occupato dal BLOCK 1:
   sopravvivono 11-16, cioè i messaggi #24-#71. Mancano #0-#23. Per un messaggio
   assente `MESSAGE` chiama `BLOCK`, che legge da `BLK-FH`: handle **della sessione di
   sviluppo**, mai riaperto perché `BLK-INIT` è saltato. Esito non verificato.
4. **Nessun `FLUSH` prima dello snapshot.** Un buffer marcato `UPDATE` congelato in
   `user.bin` verrebbe riscritto, allo sfratto, su quell'handle stantio.
5. **`COLD` resta patchato nella sessione viva**: dopo `ZAP` la sessione è da buttare
   e `ZAP` non è ripetibile. I due valori originali sono noti (`NOOP NOOP`).
6. **Heap: un solo banco 16K**, il 16. I blocchi per 17/18/19 sono commentati e le
   loro guardie usano `<` con segno (sbagliano oltre 32K). Blocca lo Stadio 5 di
   chomp-chomp (labirinti nel banco 19, `CHOMP-CHOMP-PLAN.md` Parte 10).
7. **Headroom**: i 611 byte servono a dizionario già pieno, e `PAD` = `HERE`+68 si
   sposta col dizionario. Oggi non morde (chomp-chomp lascia ~12 KB), ma non ha
   rimedio a posteriori.
8. **Pulizia**: `FILENAME`, `FH`, `S-HEAP-1..3` sono codice morto; `OPEN>` omonimo di
   `inc/open}.f` con stack e numero d'errore diversi; nessun controllo sulla
   lunghezza del nome in `FN` (48 byte); intestazioni `lib/zap.f` / `inc/zap~.f`
   imprecise; `MARKER TASK` invece di `NO-ZAP`.

## 3. Prospettive

Tre direzioni, non alternative ma in sequenza di rischio crescente:

- **A. Rendere affidabile ciò che c'è** (`lib/ZAP.f` + loader): difetti 1, 3, 4, 5, 8.
  Interventi piccoli, tutti provabili in emulatore. È ciò che propongo per stasera.
- **B. Deliverable pulito e scalabile**: heap multi-banco, `ZAP` fuori dal binario
  (limite al `MARKER`), directory per gioco, loader copiato anziché editato, Screen
  interpretativo quando l'headroom diventerà un problema vero. È il piano del
  2026-09-17, da riprendere dopo A.
- **C. `ZAP"` come deliverable a file unico**: un `.nex` si lancia dal Browser senza
  loader né indirizzi da tenere allineati, ed è il formato che un utente Next si
  aspetta. Ma congela anche il banco 5 (variabili di sistema e canali della sessione
  di sviluppo) e `BYE` non ha un BASIC a cui tornare: sperimentale, con go/no-go su
  CSpect.

## 4. Fasi

**Fase 0 -- banco di prova headless.** `emu/test_zap_standalone.py`: sessione 1
definisce una parola che stampa un marcatore e `BASE @ .`, poi `ZAP`; sessione 2
parte da RAM vergine, carica i tre file come farebbe il loader (core a `ORIGIN`, user
a un indirizzo parametrico, heap nelle pagine 8K `$20`/`$21`), entra a `ORIGIN` con
carry azzerato e confronta l'output. Lanciato con 53640 e con `R0 @` dice
oggettivamente se il difetto 1 è reale, e diventa il test di regressione di tutte le
fasi successive. In parallelo l'autore prova `game.bas` su CSpect **da avvio a freddo**.

> **Esito (2026-10-07).** `python emu/test_zap_standalone.py` (opzioni `--fill BYTE`
> per il contenuto iniziale della RAM, `--keep` per conservare i `.bin`):
>
> | `user.bin` caricato a | Esito | Output della parola di prova |
> |---|---|---|
> | 53652 (`R0 @`) | PASS, arriva a `BYE` | `ZZ10 12345 33798 33640 Z` |
> | 53640 (`Standard-Loader.bas`) | **FAIL, non arriva a `BYE`** | `ZZ-; p 0  Z` |
>
> Stesso esito con RAM iniziale a `$00` e a `$FF`. **Il difetto 1 è reale** sulla
> build corrente: con 12 byte di sfasamento `BASE` e `DP` sono spazzatura e il
> ritorno a BASIC non avviene. Il test esce con 0 se passa la riga `R0 @`; la riga
> del loader è informativa finché la fase 2 non lo corregge.
>
> **Conferma su CSpect (autore, 2026-10-07)**: `demo/chomp-chomp/game.bas` parte,
> ma l'high score è scritto male. Lo snapshot di agosto è salvato da 54168 e
> caricato a 53640 (528 byte sotto): sull'area utente finisce il testo di un
> buffer dei messaggi. `BASE` si salva perché `play-level` esegue `decimal`;
> `DP` vale `$2E72`, quindi `PAD` cade in ROM e `<# ... #>` stampa spazzatura.
> Il passaggio da 6 a 7 buffer spiega 54168 -> 53652, non il 53640 del loader,
> che risale a un layout precedente (il `.bas` è del novembre 2023).

**Fase 1 -- correttezza di `lib/ZAP.f`.**
- `FLUSH` in testa a `SAVE-USER`.
- Messaggi: vedi decisione D1.
- Ripristino di `NOOP NOOP` in `COLD` subito dopo `SAVE-CORE`: sessione riusabile.
- Controllo lunghezza del nome (errore numerato, non overrun) e pulizia del punto 8.
- Verifica: fase 0 verde; `ZAP` due volte di fila nella stessa sessione.

> **Esito (2026-10-07), verificato in emulatore, da confermare su CSpect.**
> - **Tre slot patchati solo per la durata della scrittura di `core.bin`**, poi
>   ripristinati: `COLD-SLOT` (`xt`, `BYE`), `ERROR-SLOT` (il `QUIT` finale di
>   `ERROR` -> `BYE`), `ABORT-SLOT` (il `NOOP` ex `AUTOEXEC` prima del `QUIT` di
>   `ABORT` -> `BYE`). Così `ERROR`, `ABORT` e `ABORT"` escono tutti con `BYE`,
>   senza toccare il core. Gli indirizzi sono cercati nel corpo delle parole al
>   caricamento (`CELL-OF`), non cablati: oggi `$75CD`, `$7347`, `$75BB`,
>   coincidenti con `main.lst`. La ricerca va a byte, non a celle: `ERROR`
>   contiene la stringa inline `"? "` che sfasa le celle (la prima stesura a
>   celle patchava un indirizzo sbagliato; il test l'ha preso). Controllo al
>   caricamento: dopo il `QUIT` trovato deve esserci `EXIT`, altrimenti #14.
> - `WARNING` a 0 solo durante la scrittura di `user.bin`; `FLUSH` prima; il
>   ciclo dei `BLOCK` dei messaggi è stato tolto.
> - Nessun `?ERROR` può scattare mentre la sessione è patchata: il file si apre
>   prima, l'esito di `F_WRITE` si controlla dopo il ripristino.
> - `?PATCHED 14 ?ERROR` in testa a `ZAP`: rifiuta di partire se `COLD`/`ABORT`
>   non sono nello stato atteso.
> - Corretto un difetto non in elenco: `F_WRITE` lascia sullo stack anche il
>   conteggio dei byte, e `WRITE-CLOSE` non lo toglieva (quattro celle perse a
>   ogni `ZAP`).
> - Pulizia: `MARKER NO-ZAP`, `OPEN>` -> `ZAP-OPEN`, via `FILENAME` e `FH`.
>   Il controllo sulla lunghezza del nome non serve: `WIDTH` limita i nomi a 31
>   caratteri e `FN` ne tiene 48 (il tutorial 059 sez. 5 dice il contrario).
>   `S-HEAP-1..3` e i blocchi commentati restano fino alla fase 3.
> - Il test ora verifica anche: errore dentro l'immagine (`Z? msg#33` e poi
>   `BYE`), sessione viva intatta dopo due `ZAP` (`?PATCHED` 0, `WARNING` 1,
>   stack vuoto), `heap.bin` uguale alle due pagine heap.
> - Da sapere: `ZAP-PATCH`, `ZAP-UNPATCH` e `?PATCHED` sono i pezzi che `ZAP"`
>   riuserà (D3). Gli altri due `QUIT` del core stanno in `INTERPRET` e
>   `AUTOEXEC`, che uno standalone non esegue.

**Fase 2 -- loader indipendente dal build.** Dopo aver caricato `core.bin`,
l'indirizzo di `user.bin` si legge dal core stesso: `R0_origin` sta a `ORIGIN+$14`
(25466), quindi `LOAD d$ CODE DPEEK 25466` (NextBASIC; sintassi da confermare sulla
macchina). Sparisce l'unico numero che cambia a ogni build, senza patch né
tokenizzatore. La riga va riscritta in BASIC dall'autore su `Standard-Loader.bas`
(cambia lunghezza: non è una patch in place), poi si rigenera
`demo/chomp-chomp/game.bas`. Si consolida `util/bas2txt.py` (oggi non esiste in
`util/`) per verificare header, checksum e listato dei `.bas`.

> **Esito (2026-10-07).** L'autore ha riscritto la riga 1160 in
> `Standard-Loader.bas` e `demo/chomp-chomp/game.bas`:
> `LOAD d$ CODE DPEEK 25466` (token `$8A`), più un `PAUSE 50` alla 1115.
> NextBASIC accetta la sintassi e chomp-chomp parte regolarmente su CSpect.
> Header e checksum dei due `.bas` verificati; il test della fase 0 ora legge
> la riga 1160, segue il `DPEEK` nel core appena salvato ed esige che entrambe
> le righe passino (tutto verde).
> **Aperto**: nel repo i tre `demo/chomp-chomp/game-*.bin` sono ancora quelli
> del 2026-08-23 (`R0` 54168, `WARNING` 1, nessuna patch a `ERROR`/`ABORT`).
> Con il loader nuovo si caricano all'indirizzo giusto, ma non contengono le
> novità della fase 1: vanno rigenerati con `ZAP GAME` e riportati nel repo.
> (Ricontrollato dopo lo scarico dall'immagine SD: i tre file sono **identici
> byte per byte** a quelli già in git. L'immagine SD ha ancora il core a 6
> buffer e/o lo `ZAP` vecchio: serve un `/sync-cspect` prima di rigenerare.)
> `util/bas2txt.py` resta da consolidare.

**Fase 3 -- heap multi-banco.** Fattorizzare `n SAVE-BANK` (un banco 16K = due
pagine 8K, `FAR` immediatamente prima di ogni `F_WRITE`); `SAVE-HEAP` = ciclo sui
banchi occupati secondo `HP@` (confronto senza segno); banchi dati espliciti a mano
(`19 SAVE-BANK` per chomp-chomp Stadio 5, che `HP@` non vede). Nel loader, una riga
`LOAD ... BANK n` per file: vedi decisione D2.

> **Esito lato Forth (2026-10-07), verde in emulatore.**
> - `n SAVE-BANK` (n = 16..19, numero di banco BASIC; fuori intervallo -> #10)
>   scrive `cccc-heap.bin` per il 16 e `cccc-heapU.bin` per il banco 16+U.
>   Ogni pagina 8K è mappata con `FAR` subito prima della sua scrittura.
> - `HEAP-BANKS` = `HP@ 14 RSHIFT 1+` (senza segno); `SAVE-HEAP` cicla su quelli.
> - `OPEN-FN` copia anche il NUL del suffisso: un suffisso più corto dopo uno
>   più lungo non lascia code nel nome.
> - Banchi dati oltre `HP` (chomp-chomp Stadio 5): a mano dopo `ZAP`,
>   `19 SAVE-BANK`, e una riga dedicata nel loader di quel gioco.
> - Test: sonda `ZZH` definita con `HP` a `$4100`; `ZAP` scrive anche
>   `ZZH-heap1.bin` e la sessione 2, che carica tanti banchi quanti ne dice
>   l'`HP` letto da `user.bin`, ritrova il nome nel secondo banco.
>
> **Resta il lato loader** (D2), da scrivere in BASIC sulla macchina. `HP` è la
> variabile utente a offset 26, quindi si legge dopo aver caricato `user.bin`:
>
> ```
> 1160 LET r=DPEEK 25466: LOAD d$ CODE r
> 1170 LOAD h$ BANK 16
> 1180 FOR i=1 TO INT (DPEEK (r+26)/16384): LOAD f$+"-heap"+STR$ i+".bin" BANK 16+i: NEXT i
> ```
>
> Con un solo banco il `FOR 1 TO 0` non esegue il corpo. Da provare su CSpect
> con un heap portato oltre i 16K (`HEX 4100 HP ! DECIMAL` prima di definire la
> parola da lanciare).

**Fase 4 -- `ZAP` fuori dal deliverable.** `SAVE-CORE` si ferma al `DP` precedente
al `MARKER`, con ripristino di `HP`/`LATEST`/vocabolari prima di salvare e guardia
`xt < limite` (dettagli e trappola `PAD` nel piano del 2026-09-17, sez. 8). È
l'intervento più delicato di `lib/ZAP.f`: per questo viene dopo le fasi 1-3.

**Fase 5 -- directory, loader copiato, Screen interpretativo.** Come da piano del
2026-09-17 sez. 3-6 e 10, con le correzioni della sez. 6 qui sotto.

**Fase 6 -- `ZAP"`.** PC = `0 +ORIGIN` (entra dal `and a / jp ColdRoutine`, quindi
cold garantito e nessun indirizzo cablato); patch di `COLD` riattivata con ripristino;
preparazione dello snapshot (`FLUSH`, messaggi) condivisa con `ZAP`; banchi heap dalla
stessa logica della fase 3. Da decidere cosa fa `BYE` sotto `.nex` (reset). Prova:
solo CSpect/hardware.

**Fase 7 -- documentazione.** Tutorial 059 (sei buffer -> sette, blocchi 8-15,
analisi di `$7634`, sezione 6 sul loader), `help/zap.txt` e `help/zap~.txt`,
correzione di `help/open}.txt`, `.bin` di `demo/chomp-chomp/` rigenerati, testo per
il manuale sez. 2.8 in `products/` (l'`.odt` lo tocca solo l'autore).

## 5. Decisioni dell'autore (2026-10-07)

- **D1 -- messaggi nello standalone: `0 WARNING !` nello snapshot.** `MESSAGE`
  stampa `msg#n` e non tocca mai `BLOCK`; il ciclo `17 8 DO I BLOCK DROP LOOP`
  sparisce. **Su errore lo standalone deve fare `BYE`, non `QUIT`**: il meccanismo
  è da progettare in fase 1 (`ERROR` finisce in `QUIT` nel core; con `WARNING` a -1
  passa da `ABORT`), senza modificare il core se possibile.
- **D2 -- banchi heap: il loader legge `HP` con `DPEEK`** e ne ricava il numero di
  pagine 8K da caricare. Attenzione: `HP` è una variabile utente, quindi il valore
  corrente sta in `user.bin`, mentre la copia a `ORIGIN` in `core.bin` è quella di
  avvio. O il loader la legge dall'area utente dopo aver caricato `user.bin`, o `ZAP`
  la riporta nello slot di `ORIGIN` prima di `SAVE-CORE` (fase 3). Le pagine dati
  oltre `HP` (chomp-chomp Stadio 5) restano fuori da questo conteggio.
- **D3 -- `ZAP"` è il traguardo**: un creatore di `.nex` è il risultato finale,
  "quasi commerciale". La fase 6 non è più un esperimento facoltativo: le fasi 1 e 3
  vanno scritte in modo che la preparazione dello snapshot sia condivisa fra `ZAP`
  e `ZAP"`, e la fase 5 (directory, Screen interpretativo) passa in coda.
- **D4 -- marker: `NO-ZAP`.**

## 6. Cosa cambia rispetto al piano del 2026-09-17

- Sez. 1 e 2.1: "`R0 @` = 53640 nella build misurata" non regge: 53640 è solo il
  numero scritto nel loader. Lo snapshot di agosto ha `R0` = 54168, oggi 53652.
- Sez. 2 e 5.1: i buffer sono **sette** dalla build 2026-09-25 e `HERE` pulito è 33138
  (20286 byte liberi).
- Sez. 4.2: l'argomento "Screen, non file" poggiava sullo sfratto del BLOCK 1, che
  dalla build 2026-09-25 non può più avvenire. Lo Screen conserva gli altri vantaggi
  (`(LINE)` come buffer fuori dal dizionario, `EDIT`), ma non è più obbligato.
- Sez. 6.2: la patch dei numeri a 5 byte nel `.bas` è superata dalla lettura con
  `DPEEK` (fase 2), se la sintassi regge.
- Sez. 9.3: confermato e misurato (sez. 1 qui sopra).
- Sez. 12, punto 1: `inc/F_MKDIR.f` **esiste** (commit db48c4b, 2026-07-30), insieme
  a `F_CHDIR`, `F_GETCWD`, `F_RMDIR`: non c'è nessuna `CODE` word da scrivere.
- Sez. 11: `util/bas2txt.py` non è mai stato consolidato in `util/`.

## 7. File toccati (fasi 0-3)

| File | Natura |
|---|---|
| `emu/test_zap_standalone.py` | nuovo -- banco di prova e regressione |
| `lib/ZAP.f` | modificato -- fasi 1 e 3 |
| `Standard-Loader.bas`, `demo/chomp-chomp/game.bas` | riscritti **dall'autore in BASIC** -- fase 2 |
| `util/bas2txt.py` | nuovo -- detokenizzatore di verifica |
| `demo/chomp-chomp/*.bin` | rigenerati con `ZAP GAME` da sessione viva |
| `tutorial/059-standalone-executables.f`, `help/` | fase 7 |
