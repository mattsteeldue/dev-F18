\ ZX Next Sprite test ported from Boriel ZX BASIC

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

  [ DECIMAL 64 ] LITERAL sprite-fname load-init-sprites

  DROP                                                                      \ Discard returned sprite data address

\  .( Press any key... ) CR
\  KEY DROP

  CLS

  [ HEX 8 ] LITERAL [ HEX FE ] LITERAL SWAP REG! DECIMAL \ no contention
  [ HEX 14 ] LITERAL [ HEX E3 ] LITERAL SWAP REG! DECIMAL \ global transparency
  [ HEX 40 ] LITERAL [ HEX 18 ] LITERAL SWAP REG! DECIMAL \ $40 Palette Index Register  I assume that colours 0-7 ink 8-15 bright ink 16+ paper etc? 	' 24 = paper bright 0 
  [ HEX 41 ] LITERAL [ HEX E3 ] LITERAL SWAP REG! DECIMAL \ $41
  [ 7 ] LITERAL [ 1 ] LITERAL SWAP REG! DECIMAL \ go 7mhz

\ Bit	Function
\ 7	Enable Lores Layer
\ 6-5	Reserved
\ 3-4	If %00, ULA is drawn under Layer 2 and Sprites; if %01, it is drawn between them, if %10 it is drawn over both
\ 2	If 1, Layer 2 is drawn over Sprites, else sprites drawn over layer 2
\ 1	Enable sprites over border
\ 0	Enable sprite visibility

  [ HEX 15 ] LITERAL [ BIN 00001011 ] LITERAL SWAP REG! DECIMAL \ Layer 2

  CLS
  
  [ DECIMAL 8 ] LITERAL [ 0 ] LITERAL DO

    0 bvar !

    BEGIN

      bvar @ [ DECIMAL 8 ] LITERAL * I + currspriteid !                          \ currspriteid = bvar * 8 + I

      I [ DECIMAL 24 ] LITERAL *                                    \ xcoord = I * 24
      bvar @ [ DECIMAL 24 ] LITERAL * [ DECIMAL 24 ] LITERAL +           \ ycoord = bvar * 24 + 24
      currspriteid @
      currspriteid @
      [ 0 ] LITERAL
      [ 0 ] LITERAL
      update-sprite    \ x y id patt mflip anch
     
      bvar @ 1+ bvar !
     
      bvar @ [ DECIMAL 8 ] LITERAL =

    UNTIL
     
  LOOP

  .( Press any key... ) CR
  KEY DROP

  CLS

  [ DECIMAL 230 ] LITERAL sprycoord @ DO
  
    [ 0 ] LITERAL I [ 0 ] LITERAL [ 0 ] LITERAL [ 0 ] LITERAL [ 0 ] LITERAL update-sprite       \ x y id patt mflip anch

    [ DECIMAL 2 ] LITERAL PAUSE

  LOOP

  .( Press any key... ) CR
  KEY DROP

  CLS

  0 currspriteid !
  
  [ DECIMAL 319 ] LITERAL [ 0 ] LITERAL DO

      I
      [ DECIMAL 230 ] LITERAL
      [ 0 ] LITERAL
      currspriteid @
      [ 0 ] LITERAL
      [ 0 ] LITERAL
      update-sprite    \ x y id patt mflip anch

      [ DECIMAL 4 ] LITERAL PAUSE

      currspriteid @ 1+ 5 MOD currspriteid !   \ currspriteid++ : IF currspriteid > 4 THEN currspriteid = 0

  LOOP

  .( Press any key... ) CR
  KEY DROP

  CLS
  
  [ 0 ] LITERAL [ 0 ] LITERAL remove-sprite     \ spriteid visibleflag

  .( Press any key... ) CR
  KEY DROP

  [ 1 ] LITERAL [ 0 ] LITERAL remove-sprite     \ spriteid visibleflag

;

  CR
  .( Done ) CR
