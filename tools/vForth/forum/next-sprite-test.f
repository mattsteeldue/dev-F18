\ ZX Next Sprite test ported from Boriel ZX BASIC ported versions of NextBASIC sprite demos
\ by Derek Bolli (dbolli at mac dot com)

\ NEEDS DEB
NEEDS next-sprite-lib

  CR

  .( ZX Next Sprite Test. ) CR

: BIN 2 BASE ! ;

CODE PAUSE ( ms --- )

  EXX
  POP         BC|                               \ Get PAUSE ms value
  PUSH        IX|
  CALL    HEX 1F3D AA,                          \ ROM PAUSE-1 call
  POP         IX|
  EXX
  NEXT
  C;

  CREATE sprite-fname ," ../../demos/NextBASIC/basicSprites/DKSprite.spr"   \ new Counted String zero-padded

  DECIMAL 24 VARIABLE sprycoord
  0 VARIABLE bvar
  0 VARIABLE currspriteid

: next-sprite-test ( --- )

  [ DECIMAL ] 64 sprite-fname load-init-sprites

  DROP                                                                      \ Discard returned sprite data address

\  .( Press any key... ) CR
\  KEY DROP

  CLS

  [ HEX ]
   FE  08     REG!                           \ no contention \ Works
   E3  14     REG!                           \ global transparency
   18  40     REG!                           \ $40 Palette Index Register  I assume that colours 0-7 ink 8-15 bright ink 16+ paper etc? 	' 24 = paper bright 0 
   E3  41     REG!                           \ $41
    1   7     REG! \ go 7mhz

\ Bit	Function
\ 7	Enable Lores Layer
\ 6-5	Reserved
\ 3-4	If %00, ULA is drawn under Layer 2 and Sprites; if %01, it is drawn between them, if %10 it is drawn over both
\ 2	If 1, Layer 2 is drawn over Sprites, else sprites drawn over layer 2
\ 1	Enable sprites over border
\ 0	Enable sprite visibility

  [ BIN ] 00001011  [ HEX ] 15  REG!  \ Layer 2
\  HEX 15 HEX 0B SWAP REG! DECIMAL \ Layer 2
\  HEX 15 BIN 00001011 SWAP REG! DECIMAL \ Layer 2

  CLS
  
  [ DECIMAL ]
  
\  DECIMAL 8 0 DO                               \ Generates compile time error "8 is not defined"
  8 0 DO                    \ Works

    0 bvar !

    BEGIN

      bvar @ 8 * I + currspriteid !                          \ currspriteid = bvar * 8 + I

      I 24 *                                                        \ xcoord = I * 24
      bvar @ 24 * 24 +                                              \ ycoord = bvar * 24 + 24
      currspriteid @
      currspriteid @
      0
      0
      update-sprite    \ x y id patt mflip anch
     
      bvar @ 1+ bvar !
     
      bvar @ 8 =

    UNTIL
     
  LOOP

  .( Press any key... ) CR
  KEY DROP

  CLS

  230 sprycoord @ DO
  
    0 I 0 0 0 0 update-sprite       \ x y id patt mflip anch

    2 PAUSE

  LOOP

  .( Press any key... ) CR
  KEY DROP

  CLS

  0 currspriteid !
  
  319 0 DO

      I
      230
      0
      currspriteid @
      0
      0
      update-sprite    \ x y id patt mflip anch

      4 PAUSE

      currspriteid @ 1+ 5 MOD currspriteid !   \ currspriteid++ : IF currspriteid > 4 THEN currspriteid = 0

  LOOP

  .( Press any key... ) CR
  KEY DROP

  CLS
  
  0 0 remove-sprite     \ spriteid visibleflag

  .( Press any key... ) CR
  KEY DROP

  1 0 remove-sprite     \ spriteid visibleflag

;

  CR
  .( Done ) CR
