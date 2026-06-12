---
name: bump-build
description: Aggiorna il numero di build (data YYYY-MM-DD / YYYYMMDD) del core vForth in tutti i punti canonici (SPLASH di DOES e DOT, header main.asm, F18e.f, CLAUDE.md, primo blocco di !Blocks-64.bin) e ricompila i binari. Usare quando il binario del core viene modificato e serve un nuovo build number, o quando l'utente chiede /bump-build.
---

# bump-build: nuovo numero di build del core vForth

Ogni volta che `forth18e.bin` / `ram8.bin` / il dot-command cambiano, il
deliverable riceve un nuovo build number = data odierna. Due codifiche:

- **con trattini** `YYYY-MM-DD` (stringhe SPLASH e primo blocco di !Blocks-64.bin)
- **compatta** `YYYYMMDD` (commento di testata nei main.asm)

Argomento opzionale: la data nel formato `YYYYMMDD` (default: oggi).
Lavorare da `tools/vForth/`.

## 1. Individuare la data corrente

```
grep -rn "build 20" project/vForth18_DOES/source/L0.asm
```

La data vecchia (es. `2026-05-31`) e' quella nella riga SPLASH
`" Heap Vocabulary - build YYYY-MM-DD "`. Da essa derivare anche la forma
compatta vecchia (es. `20260531`).

## 2. Punti canonici da aggiornare (data a larghezza fissa: i conteggi
##    di byte dello SPLASH non cambiano)

| File | Riga | Forma |
|---|---|---|
| `project/vForth18_DOES/source/L0.asm` | `" Heap Vocabulary - build YYYY-MM-DD "` | con trattini |
| `project/vForth18_DOES/source/main.asm` | `//  build YYYYMMDD` (testata) | compatta |
| `project/vForth18_DOT/source/L0.asm` | `" Dot-command - build YYYY-MM-DD "` | con trattini |
| `project/vForth18_DOT/source/main.asm` | `//  build YYYYMMDD` (testata) | compatta |
| `src/F18e.f` | riga 3 di testata `\ v-Forth 1.8 ... - build YYYY-MM-DD` | con trattini |
| `CLAUDE.md` | `**Current version**: 1.8 (build YYYY-MM-DD)` | con trattini |
| `!Blocks-64.bin` | primo blocco (512 byte): `build YYYY-MM-DD` | con trattini |
| `Forth18.bas` | corpo BASIC, REM prima riga: `Build YYYYMMDD` | compatta |
| `Forth18_loader.bas` | corpo BASIC, REM prima riga: `build YYYYMMDD` | compatta |

Per i file di testo usare sostituzioni esatte della sola data. Per
`!Blocks-64.bin` sostituire in-place SOLO nei primi 512 byte (la dimensione
non deve cambiare):

```python
python3 - <<'EOF'
OLD = b"build 2026-05-31"   # adattare
NEW = b"build 2026-06-12"   # adattare
assert len(OLD) == len(NEW)
with open("!Blocks-64.bin", "r+b") as f:
    head = bytearray(f.read(512))
    i = head.find(OLD)
    assert i >= 0, "data vecchia non trovata nel blocco 0"
    head[i:i+len(OLD)] = NEW
    f.seek(0); f.write(head)
EOF
```

I due `.bas` sono file ZX BASIC in formato +3DOS salvati da macchina
reale/emulatore: intestazione di 128 byte (`PLUS3DOS`, checksum al byte 127
= somma dei byte 0-126 mod 256), corpo BASIC tokenizzato a seguire. La data
sta nel corpo (REM della prima riga) in forma compatta a larghezza fissa:
sostituirla in-place byte a byte SENZA cambiare la lunghezza del file. Il
checksum copre solo l'intestazione, quindi con una sostituzione a parita'
di lunghezza non cambia: ricalcolarlo comunque come verifica (byte 127 ==
somma 0-126 mod 256) prima di riscrivere il file.

Nota: in `src/F18e.f` e nei due `L3.asm` esistono anche occorrenze della
data dentro commenti/codice commentato (vecchio SPLASH): non sono canoniche,
ma aggiornarle non guasta. Le copie sotto `project/*/source/version/`,
`version/`, `util/*_YYYYMMDD.txt` e `doc/` sono ARCHIVI STORICI: non toccarle.

**NON aggiornare i sorgenti `.f` sotto `inc/` e `lib/`.** Alcuni di essi
riportano un numero di build nei commenti: e' la data in cui QUEL sorgente
e' stato scritto o modificato l'ultima volta, non il build corrente del
core. Toccarli in massa produrrebbe solo un flood di modifiche inutili
verso git. La data in quei file si aggiorna soltanto quando si modifica
davvero il contenuto del singolo file, contestualmente alla modifica.

## 3. Ricompilare entrambe le varianti

Sul Pi sjasmplus e' in `~/.local/bin/sjasmplus` (su Windows: task VS Code
"sjasmplus" oppure `c:\Zx\sjasmplus\sjasmplus.exe`, stessi argomenti):

```
cd project/vForth18_DOES
sjasmplus --sld=list/main.sld.txt --fullpath --zxnext --lst=list/main.lst source/main.asm
cd ../vForth18_DOT
sjasmplus --sld=list/main.sld.txt --fullpath --zxnext --lst=list/main.lst source/main.asm
cat output/vforth.1 output/vforth.2 > output/vforth
cd ../..
```

## 4. Verifica

1. Nessuna data vecchia residua nei punti canonici:
   `grep -rn "VECCHIA" CLAUDE.md src/F18e.f project/vForth18_DOES/source project/vForth18_DOT/source | grep -v version/`
2. La nuova data e' nei binari:
   `grep -c "build 2026-06-12" project/vForth18_DOES/output/ram8.bin` (atteso 1; lo SPLASH vive nella heap => ram8.bin / vforth.2)
3. `!Blocks-64.bin` ha ancora la stessa dimensione di prima e
   `head -c 512 '!Blocks-64.bin' | grep -c "NUOVA"` da' 1.
4. (Opzionale, ~2 min) banner nell'emulatore:
   `printf '.quit\n' | python3 emu/repl.py | grep build` deve mostrare la nuova data.

## 5. Concludere

Riepilogare i file toccati. Commit/push solo se l'utente lo chiede
(tipicamente insieme alla modifica che ha motivato il bump).
