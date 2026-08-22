Sezione "Open questions for the author" (3 punti):

1. Numerazione - parzialmente risolta: i tutorial 030-059 sono stati
   classificati come traccia hardware-specifica ZX Spectrum Next; il
   tilemap vi si e` inserito al posto 058 (vedi CHIUSA sotto). Resta da
   decidere solo per i gap rimanenti (Q8.8, chomp-capstone): continuare ad
   appendere a 059+ (oltre 063) o inserire in mezzo alla sequenza esistente?
2. Asset AFX - CHIUSA: tutorial/afx/ (centinaia di file .afx, materiale di
   tut. 050+055) resta al suo posto sotto tutorial/, nessuno spostamento in
   work/assets/ previsto.
3. Buzzwords/BLOCK - CHIUSA (028/054 coprono il caso, gli screen restano solo come riferimento incrociato).

CHIUSA: Tilemap / Layer 3 (Axis-1). Il tutorial 058-layer3-tilemap.f e`
stabile e copre il materiale prima solo in demo/Layer3-demo1/2/3 + screen
340, 420-436 (ora riferimento incrociato).

Gap Axis-1 ancora non chiusi (codice gia` esistente in demo/ o negli screen, manca solo la promozione a tutorial):
- Fixed-point Q8.8/12.4 - screen 590-595 esistono, manca il tutorial dedicato (*/  con intermedio 32-bit, SPLIT).
- ZAP / standalone executable workflow - documentato solo dentro chomp-chomp, mai reso tutorial a se` (screen 670 come riferimento).

Axis-3 (promozione/organizzazione), ancora da fare:
- Promuovere brot.f - tutorial Layer2/Mandelbrot e Fedora.f - tutorial vettoriale/trig (il .dot.f e' gia` stato promosso a 057).
- chomp-chomp: raccomandazione di scrivere una versione "Next-like" come capstone before/after (rewrite del modello sprite/tilemap), non ancora iniziata.

CHIUSA: Riuso degli screen 880-881 per materiale BLOCK. I tutorial nei
blocchi 800-905 coprono ormai per intero il libro di Leo Brodie *Starting
FORTH* (Cap.1-11, vedi prompts/tutorial-vs-screens.md): gli Screen 880-881
sono gia` impegnati dal Buzzphrase Generator del Cap.10 e non sono piu`
"liberi" per un riuso come contenitore di materiale BLOCK -- coerente col
punto 3 sopra, gia` segnato CHIUSA.

In sintesi: la parte "dot commands" e' chiusa da ieri; asset AFX e tilemap
sono ora CHIUSI. Restano aperti: la numerazione per i soli gap rimanenti
(Q8.8, chomp-capstone), due gap di contenuto (Q8.8, ZAP) e due promozioni
demo?tutorial (brot, Fedora) oltre al capstone chomp-chomp.