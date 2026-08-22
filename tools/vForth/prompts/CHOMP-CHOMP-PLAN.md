# Revisione di demo/chomp-chomp.f — personalita' dei fantasmi, pacing esplicito, colori ciclici, labirinti per livello

## Context

`demo/chomp-chomp.f` e' un Pac-Man in vForth per ZX Spectrum, scritto in modalita'
legacy 48K (UDG, ROM BEEP, `.AT`/`.INK`, LAYER11 a 32 colonne). Funziona, ma ha
quattro limiti strutturali, tutti verificati nel sorgente:

1. **I quattro fantasmi non inseguono nessuno.** `demo/README.txt` lo dice:
   *"Ghosts movement are completely random"*. Il word `ghost-decision` che
   sceglierebbe una direzione esiste (righe 918-930) ma e' **codice morto**: in
   `move-four-ghosts` la chiamata e' commentata (riga 1119). I fantasmi vanno dritti
   finche' non sbattono, poi svoltano a caso con `2 choose`. Inky, Pinky, Blinky e
   Ted hanno nomi diversi e comportamento identico.

2. **La velocita' del gioco e' un effetto collaterale del disegno.** Ogni
   `sprite-put` chiama `sync-emit`, che inizia con `sync-vid` (`halt`). Cinque sprite
   per `heart-beat` = cinque frame = ~10 Hz. Non e' un parametro: e' il conteggio
   degli sprite sullo schermo.

3. **Il budget dei glifi e' saturo e c'e' un solo labirinto.** I 21 UDG dello
   Spectrum (codici 144-164) sono usati **tutti**: 14 muri (A-N), 1 pillola, 4
   Pac-Man, 1 fantasma, 1 ciliegia — verificato, 168 byte esatti = 21x8, zero liberi.
   I 14 glifi muro danno angoli, orizzontali, verticali e tappi ma **non raccordi a T
   ne' croci**: per questo ogni muro del tracciato attuale e' un rettangolo o una
   barra isolata, mai una forma ramificata. Ed esiste una sola tabella `,"` (righe
   406-428) che `set-maze-run` ricopia sempre identica.

4. **Il colore e' statico, e il lampeggio esistente e' opaco.** I fantasmi spaventati
   sono bianchi fissi (`Ghost-white`, colore 7) invece che blu come nell'arcade, e il
   lampeggio di fine effetto e' scritto come **cinque `if` in cascata** in
   `count-down` (righe 1067-1076) che vengono valutati **tutti**, cosicche' vince
   l'ultimo vero. Funziona, ma e' illeggibile e la durata del lampeggio e' cablata
   nella sequenza dei test.

Obiettivo: dare a ciascun fantasma la personalita' canonica dell'arcade, rendere il
pacing un parametro esplicito, introdurre una facility generale di colore ciclico,
sbloccare il budget dei glifi e permettere un tracciato diverso a ogni schema —
**mantenendo invariata la sensazione di gioco attuale** come punto di partenza.

Il gioco resta 48K-legacy: questa e' la **Fase 1**. La riscrittura con Sprite
hardware e grafica hires del Next e' la **Fase 2**, gia' in `TODO.md`
("chomp-chomp: write a Next-like capstone tutorial") — e questa revisione e'
precisamente il "before" con cui quel capstone fara' contrasto.

**Decisioni gia' prese con l'autore:** pacer disaccoppiato dal disegno;
personalita' + scatter/chase, niente Cruise Elroy; baco storico di Pinky riprodotto
e documentato; solo i colori allineati al canone (il nome "Ted" resta); alternanza
bianco/blu per i fantasmi spaventati, generalizzata a facility riusabile; set
caratteri ridefinito via CHARS; labirinti su Screen editabili; dimensioni fisse
21x21; la copia residente nei blocchi (Screen 600-66x) dichiarata superata.

---

## Parte 0 — Due bug reali e un prerequisito

**a) Il rallentamento dei fantasmi spaventati non ha mai funzionato.**
Riga 1118: `23672 @ -1 and hunt @ - 1- if`. `23672` e' FRAMES; `-1 and` e'
l'identita', quindi l'espressione vale `frames - hunt - 1`, vera per tutti i valori
tranne uno su 65536. L'intento era `1 and`:

| `hunt` | `frames&1 - hunt - 1` | effetto |
|---|---|---|
| `1` (normale) | `-2` / `-1` | sempre vero → velocita' piena |
| `-1` (spaventati) | `0` / `1` | vero a frame alterni → **meta' velocita'** |

Ma c'e' un secondo difetto nascosto: FRAMES viene riletto **dentro** il ciclo
`4 0 do`, e fra un fantasma e l'altro `sprite-put` attende un frame — i quattro
leggono valori diversi e con `1 and` si otterrebbe una scacchiera (0 e 2 si muovono,
1 e 3 no), non un dimezzamento. La correzione giusta e' un **contatore di tick unico
per `heart-beat`**, che il rework del pacing introduce comunque.

**b) La direzione di Pac-Man non viene mai aggiornata — prerequisito obbligatorio.**
In `go-right`/`go-left`/`go-up`/`go-down` la riga `sprite@ dir c!` e' **commentata
in tutte e quattro** (verificato). `pacman-init` scrive `dir`=56 una volta sola e
nessuno lo tocca piu'. Pinky e Inky mirano entrambi "davanti a Pac-Man": senza `dir`
manutenuto puntano per sempre a destra. Va sistemato **prima** di qualunque logica di
targeting, altrimenti due personalita' su quattro falliscono in silenzio.

---

## Parte 1 — Mappatura delle coordinate (da fissare prima di tutto)

E' il punto in cui e' piu' facile sbagliare senza accorgersene: una mappatura errata
specchia il baco di Pinky e l'ordine di tie-break **senza produrre nessun errore
visibile**.

| | Convenzione arcade (Pac-Man Dossier) | Questo gioco |
|---|---|---|
| orizzontale | `x` = colonna | **`y-pos`** |
| verticale | `y` = riga (cresce in basso) | **`x-pos`** |

Cioe' **`x-pos` e' la RIGA e `y-pos` e' la COLONNA** — invertito rispetto all'arcade.
Tre prove indipendenti nel sorgente: `go-right` incrementa `y-pos`; `go-down`
incrementa `x-pos`; `maze^ ( x y -- a )` calcola `maze-run + y + (x-1)*24`; e
`sprite-put` emette `22 x y`, dove il codice di controllo 22 = `AT riga, colonna`.

**Tutto il piano usa la convenzione nativa del gioco `(r, c)` = `(x-pos, y-pos)`**,
con le regole arcade gia' tradotte. Geometria: righe `1..21`, colonne `2..22`
(colonne 1 e 23 = spaziature di bordo; il byte 0 di ogni riga e' il count di `,"`,
stride 24).

Vettori direzione: `up` = `r-1`, `down` = `r+1`, `left` = `c-1`, `right` = `c+1`.

**Codifica direzioni** (gia' esistente): `key-left`=53, `key-down`=54, `key-up`=55,
`key-right`=56. Proprieta' utile: `53+56 = 54+55 = 109`, quindi **l'inversione e'
`109 SWAP -`** — una riga per la regola del "mai invertire".

---

## Parte 2 — L'algoritmo dei fantasmi

Fonti: [The Pac-Man Dossier](https://pacman.holenet.info/) di Jamey Pittman e
[Understanding Pac-Man Ghost Behavior](https://gameinternals.com/understanding-pac-man-ghost-behavior)
di Chad Birch.

Il punto chiave, e la ragione per cui questo e' implementabile su Z80: **i fantasmi
non fanno pathfinding**. Nessun A*, nessuna BFS, nessuna memoria del labirinto.
Ognuno calcola una *tile bersaglio*, e a ogni cella sceglie golosamente l'uscita che
lo avvicina di piu' in linea d'aria. Tutta la personalita' sta in *dove* mettono il
bersaglio; il motore di scelta e' identico per tutti e quattro.

### 2.1 Il motore di scelta (condiviso)

A ogni cella, per le direzioni candidate **nell'ordine up, left, down, right**:
1. scarta l'inversione della direzione corrente (`109 dir -`);
2. scarta se la destinazione non passa `?ghost-trail`;
3. calcola la distanza euclidea **al quadrato** dalla destinazione al bersaglio;
4. tieni la migliore, sostituendo solo con `<` **stretto**.

I quadrati evitano la radice (l'ordinamento e' identico) e il `<` stretto realizza
gratis il tie-break canonico **up > left > down > right**, perche' a parita' vince il
primo esaminato. Se nessun candidato sopravvive (vicolo cieco) si concede
l'inversione.

`dr` e `dc` restano sotto 64 anche col vettore raddoppiato di Inky, quindi
`dr*dr + dc*dc` sta comodo in una cella a 16 bit con segno: si usa il `*` core, senza
tabella di quadrati.

### 2.2 I quattro bersagli (gia' tradotti in riga/colonna)

Sia `P = (pr, pc)` Pac-Man, `D` la sua direzione, `B = (br, bc)` Blinky,
`G = (gr, gc)` il fantasma che decide.

**Blinky — inseguitore diretto.** `target = (pr, pc)`. Nient'altro: ti sta addosso.

**Pinky — imboscata.** Quattro celle davanti a Pac-Man:

| `D` | bersaglio |
|---|---|
| right | `(pr, pc+4)` |
| left | `(pr, pc-4)` |
| down | `(pr+4, pc)` |
| **up** | **`(pr-4, pc-4)`** ← il baco |

Il caso `up` e' il famoso overflow dell'originale 8080: la routine di offset aggiunge
erroneamente uno spostamento a sinistra pari a quello verso l'alto. Va riprodotto
**con un commento che ne spiega l'origine** — e' cio' che fa funzionare le imboscate
di Pinky ed e' la base della contromossa classica del "head-fake" (girarsi di scatto
verso Pinky sposta il bersaglio dietro di lui e lo fa deviare).

**Inky — vettore incrociato.** Prima una cella intermedia `O` due celle davanti a
Pac-Man, **con lo stesso baco su `up`**: right `(pr, pc+2)`, left `(pr, pc-2)`,
down `(pr+2, pc)`, **up `(pr-2, pc-2)`**. Poi si prende il vettore da Blinky a `O` e
lo si **raddoppia**:

```
target = ( 2*Or - br , 2*Oc - bc )
```

`2*n` e' `DUP +`. Conseguenza da preservare: Inky resta lontano finche' Blinky e'
lontano e stringe quando Blinky stringe — e' l'unico che dipende da un altro
fantasma, quindi **Blinky va valutato prima di Inky** in ogni giro. Il bersaglio puo'
risultare negativo: e' corretto e innocuo, viene usato solo come operando di una
sottrazione, mai come indice del labirinto.

**Ted (ruolo di Clyde) — timido.** Distanza al quadrato dalla **propria** cella a
Pac-Man:

```
dr = pr - gr ;  dc = pc - gc
dr*dr + dc*dc >= 64  ->  target = (pr, pc)      \ insegue come Blinky
                    altrimenti  target = il proprio angolo di scatter
```

Ne esce il comportamento caratteristico: carica, tocca l'anello delle 8 celle, si
sfila verso il suo angolo, si riallontana, ricarica.

### 2.3 Scatter / chase

Periodicamente tutti smettono di inseguire e puntano al proprio angolo: e' cio' che
rende il Pac-Man originale giocabile invece che spietato, perche' da' al giocatore
finestre di respiro ritmiche. Il motore non cambia — cambia solo il bersaglio.

Angoli di scatter, deliberatamente **fuori dal labirinto** perche' siano
irraggiungibili (il fantasma vi orbita attorno finche' la fase non cambia):

| Fantasma | Angolo | `(r, c)` |
|---|---|---|
| Blinky | alto-destra | `(0, 23)` |
| Pinky | alto-sinistra | `(0, 1)` |
| Inky | basso-destra | `(22, 23)` |
| Ted | basso-sinistra | `(22, 1)` |

Tabella fasi in **tick di gioco** (non frame): a ~10 Hz i 7s/20s/5s dell'arcade
diventano

```
scatter 70   chase 200
scatter 70   chase 200
scatter 50   chase 200
scatter 50   chase 0      \ 0 = chase indefinito
```

Il timer si azzera a inizio livello e a ogni morte, ed e' **sospeso mentre `hunt` =
-1** (fantasmi spaventati), riprendendo poi nella stessa fase. Si saltano le varianti
per livello dell'arcade (chase da 1033 s, scatter da 1/60 s): artefatti senza resa
percepibile.

**Inversione forzata al cambio di fase.** Su scatter→chase, chase→scatter e
all'ingresso in frightened i fantasmi sono obbligati a invertire la marcia — segnale
di gioco molto leggibile ("si sono girati tutti"). Flag `rev?` per fantasma, consumato
al successivo confine di cella, cosi' non girano all'unisono perfetto, come
nell'arcade. **Non** si inverte uscendo da frightened.

### 2.4 Frightened

Nessun bersaglio: a ogni incrocio si estrae una direzione pseudo-casuale e, se non e'
legale, si scorre in **senso orario** (up → right → down → left) fino alla prima
accettabile; vale sempre il divieto di inversione. Si riusa il `CHOOSE` gia' presente
(`inc/choose.f`, LCG di Brodie sul SEED della ROM) — nessun RNG nuovo.

### 2.5 Velocita' differenziata

Perche' il gioco sia giocabile i fantasmi devono essere **piu' lenti** di Pac-Man.
Accumulatore frazionario, solo somme e confronti:

```
accum += speed ;  while accum >= 256 : step ; accum -= 256
```

`speed` = 192 (75%) da normali, 128 (50%) da spaventati, contro Pac-Man che si muove
a ogni tick. Con 192: passi a 3 tick su 4. Questo sostituisce — e finalmente fa
funzionare — il gate difettoso della riga 1118.

---

## Parte 3 — Pacing esplicito

Si toglie `sync-vid` da `sync-emit` e si introduce **un pacer unico in testa a
`heart-beat`**, con un contatore di tick globale:

```forth
variable tick-frames   5 tick-frames !
variable ticks
: pace  ( -- )  1 ticks +!  tick-frames @ 0 ?do sync-vid loop ;
```

Il default `5` **riproduce esattamente la cadenza attuale** (5 sprite = 5 frame), cosi'
il gioco parte con la stessa sensazione; la differenza e' che ora e' un numero
modificabile, non il conteggio degli oggetti sullo schermo. Effetti collaterali
positivi: il disegno avviene tutto subito dopo un'interruzione (meno tearing) e
diventa possibile dare velocita' diverse a Pac-Man e ai fantasmi (§2.5), oggi
impossibile.

Il contatore `ticks` e' l'unica base dei tempi del gioco e serve **tre** clienti:
l'accumulatore di velocita' (§2.5), il timer scatter/chase (§2.3) e i cicli di colore
(Parte 4). Un solo contatore, letto una volta per `heart-beat`, elimina anche il
difetto di sincronia descritto in Parte 0a.

`maze.`, `inter-hunt` e `inter-flee` **mantengono** i propri `sync-vid`: li usano come
effetto di animazione deliberato, non come pacing di gioco.

Nota: `sync-vid` e' `halt`, quindi attende l'interruzione a 50 Hz
**indipendentemente dalla frequenza di CPU**. Il `2 SPEED!` in `game` (14 MHz) non
altera la cadenza — proprieta' da preservare.

---

## Parte 4 — Colori ciclici (facility riusabile)

### 4.1 Cosa c'e' oggi

`Ghost-white` mette tutti i fantasmi a **bianco fisso** (colore 7) per tutta la durata
dell'effetto pillola — nell'arcade sono **blu**, e diventano bianchi solo lampeggiando
quando il tempo sta per scadere. Il lampeggio esiste gia' ma e' scritto come cinque
test indipendenti in `count-down` (righe 1067-1076):

```forth
56 counting @ < if ghost-color then
57 counting @ < if ghost-white then
58 counting @ < if ghost-color then
59 counting @ < if ghost-white then
60 counting @ < if ghost-color 1 hunt ! then
```

Vengono valutati **tutti e cinque** a ogni tick e ciascuno puo' sovrascrivere il
colore: il risultato e' semplicemente "vince l'ultimo vero". Funziona, ma la durata e
il ritmo del lampeggio sono cablati nella sequenza dei test e non si possono regolare
senza riscriverla.

### 4.2 La facility

Un defining word che crea **anelli di colore** con nome, nello stesso idioma
`<builds ... does>` che il file gia' usa per `index-of` e `name-of`. L'anello tiene
un *rate* (quanti tick per colore) e la lista dei colori; a runtime restituisce il
colore corrente in funzione di `ticks`:

```forth
: COLORS: ( rate count -- )        \ poi:  c1 c,  c2 c,  ... cN c,
    <builds  swap c, c,            \ pfa: [count][rate][c1..cN]
    does>  ( pfa -- c )
        dup 1+ c@                  \ rate
        ticks @ swap /             \ indice grezzo
        over c@ mod                \ modulo count
        + 2+ c@ ;
```

Uso:

```forth
1 2 COLORS: SCARED-FLASH   1 c, 7 c,       \ blu/bianco, un tick ciascuno
4 3 COLORS: FRUIT-CYCLE    2 c, 6 c, 3 c,  \ rosso, giallo, magenta ogni 4 tick
```

Il colore si ricalcola e si scrive nel campo `color` subito prima di `sprite-put`.
**Non costa nulla**: le entita' vengono ridisegnate a ogni tick comunque.

### 4.3 Applicazioni

- **Fantasmi spaventati** — blu fisso (1) per la maggior parte dell'effetto, poi
  `SCARED-FLASH` (blu/bianco) nell'ultima fase. Sostituisce la cascata di `if` con una
  sola soglia leggibile e regolabile:
  ```forth
  : scared-color ( -- c )
      counting @ flash-at < if 1 else SCARED-FLASH then ;
  ```
  Nota: il blu (1) si libera proprio grazie al riallineamento dei colori della Parte 6
  (Inky passa da blu 1 a ciano 5), quindi non c'e' collisione.
- **Frutta** — `FRUIT-CYCLE` la fa pulsare, esattamente come chiesto: attira l'occhio
  senza costare un solo byte di grafica in piu'.
- **Pillole di potenza** — stesso meccanismo, se si vuole il classico lampeggio.

### 4.4 Alternativa notata: palette cycling

LAYER11 e' Enhanced ULA: 256 colori, 2 per cella 8x8, con INK che **indicizza una
palette riprogrammabile** (NextReg `$40`/`$41`/`$43` — il meccanismo e' gia'
documentato in `tutorial/056-layer2-palette.f`). Ciclando la voce di palette invece
dell'attributo si cambia colore **senza ridisegnare nulla**, il che permetterebbe di
animare anche cio' che non viene ridisegnato ogni tick: muri pulsanti, pillole che
respirano.

Per la Fase 1 si sceglie comunque il ciclo di attributo: le entita' sono gia'
ridisegnate a ogni tick (quindi e' gratis), non dipende dal modo video e resta valido
tale e quale nella Fase 2. Il palette cycling e' annotato come estensione naturale —
ed e' li' che darebbe il suo meglio, sui muri.

---

## Parte 5 — Sbloccare i glifi: font in RAM via CHARS

### 5.1 Il meccanismo

`EMITC` e' letteralmente `rst $10`
(`project/vForth18_DOES/source/L0.asm:765`), quindi tutto il rendering passa dal
driver di finestra della ROM NextZXOS e **qualunque codice di controllo che la ROM
supporta e' raggiungibile da vForth**. I codici rilevanti (manuale Next, cap. 21
"Window control codes" e tabella variabili di sistema):

| codice | effetto |
|---|---|
| `31, n` | sostituisce il set di dimensione `n` con il font puntato da CHARS |
| `3` | rigenera i set da 3 a 7 pixel a partire da quello da 8 |
| `30, n` | imposta la larghezza corrente del carattere (3..8 pixel) |

CHARS (`$5C36` / 23606) contiene **l'indirizzo del bitmap del codice 32 meno 256**.
Il font copre i **96 codici da 32 a 127**, 8 byte ciascuno = **768 byte**.

Ricetta (nuovo word, nello stile di `inc/widechar.f`):

```forth
MY-FONT 256 - $5C36 !      \ MY-FONT = 768 byte in RAM
$1F EMITC 8 EMITC          \ codice 31,8 : installa il font come set da 8 pixel
```

Il font di partenza si copia dalla ROM con l'idioma gia' usato altrove nel repo
(`demo/Layer3-demo1.f:77`, `lib/TILE80-setup.f:51`): `$5C36 @ #256 +` e' l'indirizzo
del codice 32.

### 5.2 Lo schema di codifica — e perche' semplifica il gioco

Il gioco stampa come testo solo: cifre `0-9`, le minuscole di "high"/"score", e lo
spazio. **Le maiuscole A-Z non sono mai stampate durante la partita.** Quindi si
ridefiniscono i codici **65-90 (A-Z) come glifi-muro**, piu' `.` (46) come pillola
centrata.

Il guadagno e' doppio, ed e' piu' grande di quanto sembri:

- **26 glifi muro invece di 14** — i 12 in piu' bastano per raccordi a T nelle quattro
  orientazioni, croci e angoli concavi, cioe' esattamente le forme che oggi mancano.
- **`udgize` sparisce.** Oggi `maze-copy` converte in linea le lettere A-U in codici
  UDG 144+. Se le lettere *sono gia'* i glifi, il testo del labirinto si stampa
  direttamente: nessuna conversione, un word in meno, e la sorgente del labirinto
  coincide byte per byte con quello che appare a schermo.
- **Tutti e 21 gli UDG si liberano** per i personaggi: Pac-Man (4), fantasma normale,
  fantasma spaventato, occhi, piu' frutta varia — dove oggi c'e' un solo fantasma per
  tutti e quattro e una sola frutta. Insieme alla Parte 4 questo permette frutta
  diverse per livello, ciascuna col proprio ciclo di colore.

Restano intatti: cifre, minuscole, i grafici a blocchi (128-143) e gli UDG (144-164).

### 5.3 Ripristino all'uscita

`game` deve rimettere CHARS al font di ROM e riemettere `31,8` prima di restituire il
prompt, accanto all'esistente `LAYER12 3 SPEED!`. Senza questo il prompt mostrerebbe
le maiuscole come pezzi di muro.

### 5.4 Rischio da verificare per primo

I codici 2/3/31 **non sono esercitati da nessuna parte in questo repo** — nessun
precedente. Vanno provati su CSpect con un test minimo (ridefinire una singola lettera
e stamparla) **prima** di costruirci sopra. Se `31,8` non si comportasse come
documentato, il ripiego e' restare nei 21 UDG (questa Parte decade, la Parte 6 resta
valida con l'alfabeto A-N attuale).

---

## Parte 6 — Un labirinto per livello, su Screen editabili

### 6.1 Perche' su Screen

Un labirinto e' 21 righe x 24 byte = **504 byte**. Entrerebbe in un solo BLOCK (512),
ma le righe non si allineano alla griglia 8x64 dell'editor. Con **2 Screen
consecutivi** (32 righe da 64 caratteri) invece si progetta un tracciato
**digitandolo con EDIT** e lo si rivede con `LIST`, senza compilare nulla. Lo spreco
(~1,5 KB per labirinto su un file da 16 MB) e' irrilevante; l'editabilita' vale molto
di piu'.

C'e' gia' il precedente in casa: la versione a blocchi tiene il maze sugli **Screen
615-616**, e i tutorial 028/029/063 sono tutti su questo idioma.

**Attenzione:** non usare `LOAD2BLOCK` — la sua etichetta-nome da 64 byte limita il
payload a 448 byte, meno dei 504 necessari. Serve l'accesso diretto via `BLOCK`.

### 6.2 Layout

Labirinto `N` = Screen `MAZE-SCR0 + 2N` e `+2N+1`:

- righe 0..20 delle 32 disponibili = le 21 righe del labirinto;
- colonne 0..22 di ciascuna riga = i 23 caratteri; colonne 23..63 libere per commenti;
- righe 21..31 libere per i metadati del livello (nome, velocita', colori, frutta).

Caricamento: per la riga `r` (0..20), `blocco = base + r/8`,
`offset = (r mod 8)*64`; si copiano 23 byte nella riga `r` di `maze-run` (stride 24,
offset 1) e si scrive 23 nel byte di count. Tre blocchi distinti su 6 buffer
disponibili: nessun thrashing.

Range libero contiguo verificato nel file blocchi: **724-776** (53 Screen = 26
labirinti). Da confermare dall'autore.

### 6.3 Aggancio e contatore di livello

`set-maze-run` e' gia' l'unico punto giusto: chiamato a riga 451 (caricamento), 1216
(`game`) e **1183 (`phase-complete`, cioe' proprio "nuovo schema")**. Non esiste alcun
contatore di livello nel gioco: se ne aggiunge uno, e `set-maze-run` sceglie il
labirinto `level MOD n-labirinti`.

### 6.4 Il labirinto #0 resta compilato — e perche'

Oggi il tracciato e' nel dizionario, quindi lo standalone prodotto da `ZAP` e'
autosufficiente. Spostando tutto su blocchi, lo standalone dipenderebbe dalla presenza
di `!Blocks-64.bin`. **Si tiene quindi il tracciato attuale compilato come labirinto
#0 di ripiego**, con i blocchi che forniscono i livelli 1..N e un fallback al #0 se la
lettura fallisce. Lo standalone continua a funzionare da solo.

### 6.5 Validatore

Un labirinto scritto a mano puo' rompere il gioco in silenzio. Un word
`MAZE-CHECK ( scr# -- )` da interprete (non compilato nel gioco) verifica: 21 righe da
23 caratteri; nessun NUL (che fermerebbe l'interpretazione senza messaggio); bordo
sigillato; casa dei fantasmi presente con porte `-`; tunnel `/` e `\` appaiati sulla
stessa riga; numero di pillole `O` atteso; e connettivita' via flood-fill dalla
partenza di Pac-Man (441 celle: banale in Forth). Senza questo, un tracciato sbagliato
si manifesta come un fantasma incastrato a meta' partita.

---

## Parte 7 — File toccati e ordine di lavoro

Quattro stadi, ciascuno verificabile da solo su CSpect prima di passare al successivo.

### Stadio 1 — AI e pacing (nessun cambiamento visivo al labirinto)

Tutto in **`demo/chomp-chomp.f`**:

1. *Prerequisito*: riattivare `sprite@ dir c!` nelle quattro `go-*` (Parte 0b).
2. `Ghost-color` ai colori canonici: Blinky=2 rosso, Pinky=3 magenta, Inky=5 ciano,
   Ted=6 giallo (il piu' vicino all'arancio negli 8 colori ULA). Oggi sono Inky=1,
   Pinky=3, Blinky=5, Ted=2 — nome, colore e ruolo non raccontano la stessa storia. Il
   nome "Ted" resta. Questo libera anche il blu (1) per lo stato spaventato.
3. Stride di `Array` da 8 a 16 byte per i nuovi attributi (`accum`, `speed`, `rev?`).
   **Quattro punti vanno cambiati insieme**, altrimenti il difetto e' silenzioso:

   | Riga | Ora | Diventa |
   |---|---|---|
   | 490 | `create Array 6 08 * allot` | `6 16 * allot` |
   | 503 | `sprite#` : `dup 3 lshift array +` | `4 lshift` |
   | 536 | `name-of` : `3 lshift Array +` | `4 lshift` |
   | 513-519 | `all-ghost` : `32 Array +` … `08 +loop` | `64 Array +` … `16 +loop` |

4. Motore AI: distanza al quadrato, cella di destinazione per direzione, scelta della
   migliore, inversione `109 SWAP -`.
5. Un word per bersaglio + dispatch su `Sprite-no` (`CASE`, coerente con lo stile del
   file che gia' lo usa ovunque).
6. Macchina scatter/chase: tabella fasi, timer, flag di inversione forzata.
7. Riscrivere `ghost-move`; **rimuovere** `ghost-decision` (morto) e le svolte casuali
   `2 choose` dentro `ghost-right/left/up/down`.
8. Pacer `tick-frames`/`ticks` + `pace`; togliere `sync-vid` da `sync-emit`.
9. Sostituire il gate rotto di riga 1118 con l'accumulatore di velocita'.

Riuso di quel che c'e': `?ghost-trail`, `maze@`, `xy-pos@`/`xy-pre@`, `c+!`, `D=`,
`CHOOSE`, `sprite#`/`name-of`/`index-of`, `hunt`/`counting`. `ABS`, `MIN`, `MAX`, `*`,
`<`, `U<` sono **word core** (`src/F18e.f`): nessun `NEEDS` nuovo.

### Stadio 2 — Colori ciclici

`COLORS:`, gli anelli `SCARED-FLASH` / `FRUIT-CYCLE`, la sostituzione della cascata di
`if` in `count-down` con la soglia `flash-at`, il blu fisso come colore spaventato di
base e l'aggancio del colore prima di `sprite-put`. Piccolo e indipendente: si puo'
validare da solo mangiando una pillola.

### Stadio 3 — Font in RAM (il gioco deve restare identico a vedersi)

Prima il test isolato dei codici 2/3/31 su CSpect (Parte 5.4). Poi: tabella font da
768 byte, copia dal font di ROM, ridefinizione di A-Z e `.`, installazione in
`init-display`, ripristino in `game`, rimozione di `udgize`, riassegnazione degli UDG
liberati ai personaggi. **Criterio di successo: schermata indistinguibile dallo
stadio 2.**

Candidato a diventare `inc/`: il word che installa un font RAM e' generico e utile
oltre questo gioco; se resta pulito vale un `inc/chars!.f` (decisione a valle).

### Stadio 4 — Labirinti su Screen

Formato e range Screen, loader in `set-maze-run`, contatore di livello, `MAZE-CHECK`,
conversione del tracciato attuale come primo Screen (verifica che la pipeline preservi
il comportamento), poi i nuovi tracciati che sfruttano i glifi in piu'.

### Altri file

- **`demo/chomp-chomp/chomp-chomp.f`** — verificato byte-identico al master (stesso
  MD5). Si ricopia dal master a fine lavoro.
- **`demo/chomp-chomp/*.bin`** — lo standalone si rigenera solo con `ZAP GAME` da una
  sessione vForth viva, non e' producibile headless: lo rifa' l'autore dopo la
  validazione.
- **`demo/README.txt`** — la voce dice *"Ghosts movement are completely random"*: da
  riscrivere con le quattro personalita' e i labirinti multipli.
- **Screen 600** — la copia residente nei blocchi (600 → 601/610/630/650/660, maze su
  615-616) e' **dichiarata superata**: una nota sullo Screen 600 rimanda a
  `demo/chomp-chomp.f` come unica versione mantenuta. Nessuna modifica al codice a
  blocchi.

*Drive-by opzionale:* `tutorial/059-standalone-executables.f` (righe 85-86) e
l'intestazione di `lib/ZAP.f` documentano entrambi `ZAP CHOMP-CHOMP`, ma nel sorgente
non esiste nessun word `CHOMP-CHOMP`: l'entry point e' `GAME` (ed e' con `ZAP GAME`
che sono stati prodotti i `.bin` distribuiti). Bug di documentazione reale in due file.

---

## Parte 8 — Verifica

### Test headless dell'aritmetica (`emu/repl.py`)

E' la parte davvero verificabile da qui, ed e' anche quella dove un errore e'
invisibile a occhio. I word di targeting vanno fattorizzati per essere chiamabili
senza far girare il gioco, e coperti con la notazione `{...}T` (vedi
`test/CLAUDE.md`):

- ogni bersaglio nelle 4 direzioni di Pac-Man, **incluso il caso `up` di Pinky e di
  Inky** — e' esattamente il caso che una mappatura riga/colonna sbagliata
  specchierebbe senza dare errore;
- il vettore raddoppiato di Inky con Blinky in posizioni diverse, incluso un bersaglio
  negativo;
- la soglia di Ted esattamente a distanza al quadrato 63 / 64 / 65;
- l'inversione `109 SWAP -` su tutti e quattro i valori;
- il tie-break: con due uscite equidistanti deve vincere up>left>down>right;
- il vicolo cieco (unica uscita = l'inversione);
- gli anelli di colore: `COLORS:` con rate e count noti deve restituire la sequenza
  attesa al variare di `ticks`, incluso il wrap;
- `MAZE-CHECK` su un labirinto volutamente rotto (bordo aperto, zona irraggiungibile).

### Validazione su CSpect (la avvia l'autore)

La sandbox non puo' lanciare GUI: serve `cspect.bat 4` e il caricamento manuale di
`Forth18_loader.bas`.

**Stadio 1** — 1) con `tick-frames`=5 la velocita' e' indistinguibile da oggi;
2) i quattro fantasmi si comportano visibilmente in modo diverso (Blinky ti sta
dietro, Pinky ti taglia la strada, Ted si sfila quando ti avvicini); 3) al cambio
scatter/chase si girano tutti, a un frame di distanza l'uno dall'altro; 4) da
spaventati vanno a caso **e** visibilmente piu' lenti (conferma che il bug di riga
1118 e' chiuso); 5) nessun fantasma resta incastrato nella casa centrale;
6) `tick-frames` a 3 e a 8 scala la velocita' in modo pulito.

**Stadio 2** — mangiando una pillola i fantasmi diventano blu, e lampeggiano
blu/bianco solo nella fase finale; la frutta pulsa; regolando `flash-at` cambia il
momento in cui inizia il lampeggio.

**Stadio 3** — test isolato dei codici 2/3/31 **prima** di tutto il resto; poi
schermata identica allo stadio 2; e all'uscita da `game` il prompt torna con le
maiuscole normali.

**Stadio 4** — il tracciato convertito si comporta come l'originale; il cambio di
livello carica un tracciato diverso; `MAZE-CHECK` passa su tutti quelli distribuiti.

Se in playtest i fantasmi escono troppo compatti dalla casa centrale, il rimedio piu'
economico e' un rilascio scaglionato (0/20/40/60 tick) invece della logica completa
della ghost house.

---

## Parte 9 — Fase 2 (non in questo piano)

Questa revisione lascia il gioco in forma 48K legacy: testo ULA 8x8, `.AT`/`.INK`,
ROM BEEP. La riscrittura Next — Sprite hardware (tutorial 053), tilemap Layer 3
(tutorial 058: 256 tile 8x8 a 16 colori su griglia 40x32 o 80x32, indipendente dalla
ULA), grafica hires — e' lavoro separato, gia' in `TODO.md`.

Cio' che questo piano gli prepara e' il termine di paragone: **l'AI, la macchina a
stati, i cicli di colore e il formato dei labirinti progettati qui sono indipendenti
dal livello di presentazione** e vanno riusati tali e quali dalla versione Next, che
cambia solo come le entita' vengono disegnate. I labirinti su Screen in particolare
restano validi identici: cambia il glifo che rappresenta ogni cella, non il tracciato.
E il palette cycling annotato in 4.4 e' esattamente il punto in cui la versione Next
puo' superare questa senza toccare la logica. Il capstone "before/after" mette a
confronto le due presentazioni a parita' di logica di gioco.
