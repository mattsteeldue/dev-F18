\
\ TILE-80.f
\ ______________________________________________________________________ 
\
\ MIT License (c) 1990-2026 Matteo Vitturi     
\ ______________________________________________________________________ 

\ Tilemode 80 
\
.( TILE-80 )
\
\

\ ______________________________
\
\ NextREG 0x68 (104) - ULA Control. disable ULA output
\ $80 $68 reg!
\
\ NextREG 0x6B (107) - Tilemap Control
\ %10100001 $6B reg!

\ 0x6B (107) Tilemap Control
\ bit 7 = 1 enable the tilemap
\ bit 6 = 0 for 40x32, 1 for 80x32
\ bit 5 = no attribute byte in tilemap (saves space)
\ bit 4 = select palette, 0 first, 1 second
\ bit 3 = set text mode, i.e. 1-bit B&W bitmaps
\ bit 2 = reserved, must be zero
\ bit 1 = activate 512 tile mode
\ bit 0 = force tilemap on top of ULA
: TILE-80  %11001001 $6B reg! $80 $68 reg! ;
