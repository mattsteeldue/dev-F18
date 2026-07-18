Sezione "Open questions for the author" (3 punti):

1. Numerazione — parzialmente risolta: si è confermato il precedente "append" (055?056?057, con lo slot DMA spostato da 057 a 058-dma.f). Resta da decidere per i gap rimanenti (tilemap, Q8.8, chomp-capstone): continuare ad appendere a 059+ o inserire in mezzo alla sequenza esistente?
2. Asset AFX — parzialmente risolta: lo scopo di tutorial/afx/ (centinaia di file .afx) è ormai chiaro (materiale di tut. 050+054), ma resta aperto se spostarli fuori da tutorial/ (in work//assets/) per non gonfiare il repo, o lasciarli dove sono.
3. Buzzwords/BLOCK — CHIUSA (028/054 coprono il caso, gli screen restano solo come riferimento incrociato).

Gap Axis-1 ancora non chiusi (codice già esistente in demo/ o negli screen, manca solo la promozione a tutorial):
- Tilemap / Layer 3 — solo demo/Layer3-demo1/2/3 + screen 340, 420-436; nessun tutorial.
- Fixed-point Q8.8/12.4 — screen 590-595 esistono, manca il tutorial dedicato (*/  con intermedio 32-bit, SPLIT).
- ZAP / standalone executable workflow — documentato solo dentro chomp-chomp, mai reso tutorial a sé (screen 670 come riferimento).

Axis-3 (promozione/organizzazione), ancora da fare:
- Promuovere brot.f ? tutorial Layer2/Mandelbrot e Fedora.f ? tutorial vettoriale/trig (il .dot.f è già stato promosso a 057).
- chomp-chomp: raccomandazione di scrivere una versione "Next-like" come capstone before/after (rewrite del modello sprite/tilemap), non ancora iniziata.
- Riuso o meno degli screen 880-881 per materiale BLOCK (menzionato nel TL;DR finale come terza decisione dell'autore, in sovrapposizione col punto AFX).

In sintesi: la parte "dot commands" è chiusa da ieri; restano aperte le tre decisioni esplicite dell'autore (numerazione, asset AFX, riuso screen 880-881) più tre gap di contenuto (tilemap, Q8.8, ZAP) e due promozioni demo?tutorial (brot, Fedora) oltre al capstone chomp-chomp.