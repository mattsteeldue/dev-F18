---
name: check-f18e
description: Verifica che src/F18e.f sia coerente col core assemblato (forth18e.bin + ram8.bin di project/vForth18_DOES) confrontando, con una mappa di rilocazione, il binario ottenuto compilando F18e.f UNA sola volta su CSpect. Sostituisce il vecchio confronto binario-binario a doppia compilazione. Usare dopo modifiche a src/F18e.f o al core, prima di un rilascio, o quando l'utente chiede /check-f18e.
---

# check-f18e: coerenza F18e.f <-> core assemblato

`src/F18e.f` e' la forma Forth leggibile del core; i sorgenti `.asm` sono
l'autorita'. Compilare `F18e.f` su CSpect e' la prova autentica che il sorgente
compila; il problema e' che il binario nasce a un'origine diversa (piu' in alto,
sopra `HERE` dopo un COLD normale), quindi gli indirizzi sono spostati e un
diff byte-a-byte non serve. Lo strumento `util/cmp-f18e.py` risolve questo
con una mappa di rilocazione. Lavorare da `tools/vForth/`.

## Prerequisito

Il riferimento deve essere aggiornato: `/build DOES` (o `/bump-build`) deve
essere stato eseguito DOPO l'ultima modifica ai sorgenti `.asm`, cosi'
`project/vForth18_DOES/output/forth18e.bin` e `ram8.bin` corrispondono al core.

## 0. Gate: la SD di CSpect deve avere il sorgente e il core correnti

CSpect legge dall'immagine SD, non dal PC: se l'immagine non e' allineata
l'utente compila un `F18e.f` vecchio (o su un core vecchio) e il confronto
esce falsato. **Prima** di chiedere la compilazione, con CSpect e MAME chiusi,
confrontare per MD5 PC e SD di questi tre file:

| PC (`tools/vForth/`) | SD (`W:\tools\vForth\`) |
|---|---|
| `src/F18e.f` | `src\F18e.f` |
| `forth18e.bin` | `forth18e.bin` |
| `ram8.bin` | `ram8.bin` |

(W: si monta e smonta con `util\mountw.ps1`, ripristinando lo stato trovato.)
Se anche uno solo differisce -- o nel dubbio -- lanciare **`/sync-cspect`**,
che verifica tutto l'albero e smonta W: alla fine. Solo con l'esito "allineato"
si passa al punto 1. Se `F18e.f` su SD ha timestamp 1980 (editato dentro
CSpect) il sync lo protegge e non lo sovrascrive: fermarsi e chiedere
all'autore quale versione vale.

## 1. Compilare F18e.f su CSpect (lo fa l'utente)

Claude NON avvia CSpect (il sandbox blocca la GUI). Chiedere all'utente di:

1. avviare CSpect e portare vForth al prompt `ok` con un normale COLD;
2. eseguire `INCLUDE SRC/F18E.F` (circa 3 minuti e mezzo); `F18e.f` stampa
   `HERE` e `HP@` prima di partire (es. `9822 1BC3`): l'**origine** compilata
   e' `HERE + 3` (i 3 byte di `JP $0038` del vettore d'interrupt), qui `$9825`;
3. tornare a BASIC e salvare, ad esempio:
   `SAVE "forth18_.bin" CODE 38949,7754`  (38949 = `$9825`, 7754 = lunghezza
   reale del core). Usare una lunghezza maggiore e' innocuo: lo strumento
   confronta solo fino alla lunghezza del riferimento; una minore da'
   "COPERTURA PARZIALE".

**Il `SAVE` e' l'unico passaggio manuale dell'utente ed e' facilissimo da
sbagliare** (38948 al posto di 38949 e' gia' successo, 2026-09-20): l'indirizzo
e' in decimale, deve essere esattamente `HERE + 3` e basta una cifra sbagliata.
Quindi Claude, quando chiede il salvataggio:

- legge dall'utente il valore di `HERE` stampato all'inizio della compilazione
  (esadecimale, es. `9822`), calcola LUI `HERE + 3` e lo converte in decimale
  (es. `$9825` = 38949); non lascia all'utente il calcolo;
- consegna la riga BASIC completa da copiare, `SAVE "forth18_.bin" CODE
  <decimale>,7754`, e ricorda di ricontrollare l'indirizzo cifra per cifra;
- dopo il confronto, se lo strumento stampa `ATTENZIONE: ... sfasati`, lo dice
  all'utente con parole esplicite ("l'indirizzo del SAVE aveva un errore di
  battitura di N byte") e gli riporta la riga corretta che lo strumento
  stampa, invece di limitarsi a dare l'esito.

Il file salvato ha un header +3DOS con l'indirizzo di caricamento, che lo
strumento legge da se': non serve passare l'origine. Se l'indirizzo del `SAVE`
e' sbagliato di pochi byte (e' successo: 38948 al posto di 38949, 2026-09-20) i
dati risultano sfasati e senza rimedio il confronto sembrerebbe un disastro
(decine di differenze in ORIGIN, scarti dell'heap impossibili): lo strumento
cerca lo scostamento con piu' byte uguali al riferimento (da -8 a +8), lo
applica e stampa `ATTENZIONE: i dati risultano sfasati di +N byte`. In quel
caso l'esito resta valido, ma correggere l'indirizzo al `SAVE` successivo.

## 2. Eseguire il confronto

```
python util/cmp-f18e.py forth18_.bin --log forth18-cmp.log
```

(Su Windows preferire `C:\Users\matteo\AppData\Local\Python\pythoncore-3.14-64\python.exe`;
il bare `python` puo' essere lo stub WindowsApps.) Per un file senza header
aggiungere `--org HEX`. Codice di uscita: 0 coerente, 1 differenze non
spiegate, 2 errore d'uso.

## 3. Come funziona (per capire il log)

- I confini delle parole vengono dall'heap del riferimento (`ram8.bin`), letto
  come catena di voci `[len|$80][nome][link][xt]`; la parola di nome NUL
  (un solo byte `$80`) va accettata.
- **Codice**: ogni valore a 16 bit che differisce deve valere
  `riferimento + T` con `T = ORG - $6366` (una sola costante per tutto il
  codice: le due compilazioni hanno le stesse dimensioni).
- **Heap**: il mirror-pointer di 2 byte prima di ogni CFA da' lo scarto
  dell'heap per quella parola; i valori a 16 bit possono valere
  `riferimento + scarto`. Lo scarto NON e' costante: parte da `$1B51`
  (l'assemblatore compilato prima occupa l'heap) e fa uno scalino di
  +258 byte a `LSHIFT`: e' il salto alla seconda pagina 8K dell'heap,
  `page-watermark = $1EFF` (`skip-hp-page`) lascia 257 byte di "grazia" e HP
  passa da `$1F00` a `$2002`. Uno scalino cosi' e' atteso; un salto diverso
  segnala definizioni ausiliarie aggiunte o tolte nel sorgente.

## 4. Differenze attese (5 byte, gia' filtrate dallo strumento)

| Dove | Motivo |
|---|---|
| `ORIGIN+008` (2 byte) | saved Basic SP: dipende dall'ambiente di compilazione |
| `ORIGIN+030` (2 byte) | Return Stack Pointer (R0) dell'ambiente |
| `AUTOEXEC`, literal (1 byte) | `10 0 +origin 32768 u< 1 and +`: 11 sotto `$8000`, 10 sopra |

`LATEST` (`ORIGIN+00C`) e `HP` (`ORIGIN+026`) NON sono differenze: valgono
riferimento + scarto finale dell'heap e lo strumento li rileva come rilocati.
Se una nuova differenza legittima compare, aggiungerla al dizionario `EXPECTED`
di `util/cmp-f18e.py` CON il motivo scritto; non allargare mai le regole di
rilocazione per farla passare.

## 5. Interpretare l'esito

- `ESITO: COERENTE`: nessuna differenza non spiegata; riportarlo all'utente
  citando parole confrontate, byte rilocati e scalini dell'heap.
- `DIFFERENZE DA ESAMINARE`: il log elenca `[parola] +offset ($indirizzo)
  rif=.. nuovo=..`. Cercare l'indirizzo in `project/vForth18_DOES/list/main.lst`
  e la parola in `src/F18e.f`; le cause tipiche sono un uso non rinominato
  (e' successo con `mcod` -> `code`, 2026-09-20), un ramo condizionale
  dipendente dall'origine, o un sorgente `.asm` cambiato senza aggiornare
  `F18e.f` (o viceversa).
- Se la compilazione su CSpect si ferma con un errore (`xxx? msg#n`), il token
  stampato e' la parola non risolta: e' un bug di `F18e.f`, non del confronto.

## Note

- Non committare `forth18_.bin` ne' i log: sono artefatti temporanei.
- Il vecchio metodo (compilare due volte e confrontare i binari) non serve
  piu' e non va ripristinato: non c'e' abbastanza spazio per compilare due
  volte l'ASSEMBLER incluso in `F18e.f`.
- Il compilatore nell'emulatore headless (`emu/`) produce lo stesso binario
  (verificato byte per byte, 2026-09-20) ma impiega circa 20 minuti contro i
  3-4 di CSpect; i tasti per i `KEY` vanno iniettati a mano nel polling di
  `Key_Wait`. Preferire CSpect.
