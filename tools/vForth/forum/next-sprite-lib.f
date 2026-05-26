\ ZX Next Sprite lib v0.1.1 ported from Boriel ZX BASIC nextlib.bas
\ by Derek Bolli (dbolli at mac dot com)
\ https://github.com/em00k/NextBuild/blob/master/Scripts/nextlib.bas

NEEDS ASSEMBLER

  CR

  .( ZX Next Sprite Library. ) CR

  HEX 303B CONSTANT ZXN-SPRITE-SLOT-SELECT-PORT DECIMAL
  HEX 57 CONSTANT ZXN-SPRITE-ATTRIBUTE-PORT DECIMAL
  HEX 5B CONSTANT ZXN-SPRITE-PATTERN-PORT DECIMAL

  .( Load Init Sprites. ) \ CR

  DECIMAL 256 CONSTANT SPRBUFFERLEN

  0 VARIABLE sprfileh

  0 VARIABLE sprite-buffer SPRBUFFERLEN ALLOT   \ Create sprite data buffer
  sprite-buffer SPRBUFFERLEN ERASE              \ Fill with $00

  .( Init Sprite. ) \ CR

CODE send-sprite-data ( port sprdataaddr --- )

  POP         HL|                               \ Get sprite buffer array address
  POP         DE|                               \ Get Next Sprite Pattern port
  PUSH        BC|
  LD         B'|         D|
  LD         C'|         E|
  OTIR                                          \ Send bytes to port
  POP         BC|
  NEXT
  C;

: init-sprite ( spriteid --- )

  ZXN-SPRITE-SLOT-SELECT-PORT P!           \ Set sprite slot spriteid via ZXN Port $303B \ Removed SWAP

\  CR .( Sending Sprite data. ) CR

  ZXN-SPRITE-PATTERN-PORT                       \ Put Next Sprite Pattern port on stack
  sprite-buffer                                 \ Put sprite buffer array address on stack
  send-sprite-data

\  .( Finished Sending Sprite data. ) CR

;

: load-init-sprites ( num fname --- addr )

  .( Load sprite bytes ) CR                     \ DEBUG  

  1+ PAD 1 F_OPEN                               \ num-sprites fname-addr

  CR .( File open result: ) . CR

  sprfileh !                                    \ Save sprite data file handle

  0 DO                                          \ num limit already on stack

\    .( Reading sprite: ) I DECIMAL U. .(  ) \ CR

\    I SHOW-PROGRESS

    sprite-buffer SPRBUFFERLEN sprfileh @ F_READ
\    .( File read result: ) . \ CR
\    .( Bytes read: ) DECIMAL . CR

    I
    init-sprite                                 \ Send sprite data in buffer
  
  LOOP

  sprfileh @ F_CLOSE
  .( File close result: ) . CR

  sprite-buffer                                 \ Leave sprite buffer addr on stack
;

  .( Update Sprite. ) \ CR

  0 VARIABLE xcoord
  0 VARIABLE ycoord
  0 VARIABLE spriteid
  0 VARIABLE pattern
  0 VARIABLE mflipflags
  0 VARIABLE anchor

CODE update-sprite-data ( anch patt mflip y x port --- )

  EXX
  POP         BC|                               \ Get Next Sprite Attribute port
  POP         HL|                               \ Get xcoord (save MSB for later)
  LD         A'|         L|
  OUT(C)      A'|
  POP         DE|                               \ Get ycoord
  LD         A'|         E|
  OUT(C)      A'|
  POP         DE|                               \ Get flags
  LD         A'|         H|                     \ Get MSB of xcoord
  ANDN        1    N,
  ORA          E|
  OUT(C)      A'|
  POP         HL|                               \ Get pattern
  LD         A'|         L|
  ORN         HEX C0 N,
  OUT(C)      A'|
  POP         HL|                               \ Get anchor
  LD         A'|         L|
  OUT(C)      A'|
  EXX
  NEXT
  C;

: update-sprite ( x y id patt mflip anch --- )

  anchor ! mflipflags ! pattern ! spriteid ! ycoord ! xcoord !  \ Get params off stack

  ZXN-SPRITE-SLOT-SELECT-PORT spriteid @ SWAP P!     \ Set sprite ID via ZXN Port $303B

\  HEX
  
\  ZXN-SPRITE-ATTRIBUTE-PORT xcoord @ [ HEX FF ] LITERAL AND SWAP P! \ Set sprite attribute 0 x coord (lo byte)
\  ZXN-SPRITE-ATTRIBUTE-PORT ycoord @ SWAP P!         \ Set sprite attribute 1 y coord
\  ZXN-SPRITE-ATTRIBUTE-PORT mflipflags @        \ Get sprite attribute 2 palette offset
\ \  xcoord @ 8 RSHIFT [ HEX FF ] LITERAL AND 1 AND OR SWAP P!  \ Set sprite attribute 3 palette offset and x coord (bit 0 of hi byte) 
\  xcoord @ 8 RSHIFT 1 AND OR SWAP P!                 \ Set sprite attribute 3 palette offset and x coord (bit 0 of hi byte) 
\  ZXN-SPRITE-ATTRIBUTE-PORT pattern @ [ HEX C0 ] LITERAL OR SWAP P!  \ Set sprite attribute 4 sprite visible and pattern num (bit 7 for visibility bit 6 for 4 bit)
\  ZXN-SPRITE-ATTRIBUTE-PORT anchor @ SWAP P!         \ Set sprite attribute 5 anchor (attr 5 the sub-pattern displayed is selected by "N6" bit in 5th sprite-attribute byte.)

\  DECIMAL

\  CR .( Updating Sprite data. ) CR

  anchor @
  pattern @
  mflipflags @
  ycoord @
  xcoord @
  ZXN-SPRITE-ATTRIBUTE-PORT
  update-sprite-data

\  .( Finished Updating Sprite data. ) CR

;

  .( Remove Sprite. ) \ CR

  0 VARIABLE visibleflag

CODE remove-sprite-data ( visibleflag sprattrport --- )

  EXX
  POP         BC|                               \ Get Next Sprite Attribute port
  XORA         A|                               \ get x and send byte 1
  OUT(C)      A'|                               \ X POS
  OUT(C)      A'|                               \ Y POS and send byte 2
  OUT(C)      A'|                               \ no palette offset and no rotate and mirrors flags send  byte 3
  POP         HL|                               \ Get visible flag
  LD          A'|         L|
  OUT(C)      A'|                               \ Sprite visible and show pattern #0 byte 4
  EXX
  NEXT
  C;

: remove-sprite ( spriteid visibleflag -- )

  visibleflag ! spriteid !

  ZXN-SPRITE-SLOT-SELECT-PORT spriteid @ SWAP P!     \ Set sprite ID via ZXN Port $303B

\  .( Removing Sprite. ) CR

  visibleflag @
  ZXN-SPRITE-ATTRIBUTE-PORT
  remove-sprite-data                            \ visibleflag sprattrport

;

  CR
  .( Done ) CR
