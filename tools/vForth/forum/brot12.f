needs j
needs layer2
needs PLOT

0 VARIABLE XX
0 VARIABLE YY
0 VARIABLE X
0 VARIABLE Y
0 VARIABLE XT
0 VARIABLE XZ
0 VARIABLE YZ
0 VARIABLE IDX

100 CONSTANT FXP


HEX
CREATE COLOR-TAB
00 C,   \ BLACK
01 C,   \ BLUE
41 C,
81 C,
A1 C,
C1 C,
E1 C,
E9 C,
E8 C,
F0 C,
D4 C,
B8 C,
9C C,
00 C,  \ BLACK
DECIMAL


: +COLOR ( b -- c )
  COLOR-TAB + C@
;


: BROT12
layer2
cls


DECIMAL
192 0 DO
  256 0 DO
    I 350 256 */ 250 - XZ !
    J 200 192 */ 100 - YZ !
    0 X ! 0 Y !

    14 0 DO
      I IDX !
      X @ DUP FXP */ XX !
      Y @ DUP FXP */ YY !
      YY @ XX @ + 400 > IF LEAVE THEN XX @
      YY @ - XZ @ + XT !
      200 X @ FXP */ Y @ FXP */ YZ @ + Y !
      XT @ X !
    LOOP

    ?TERMINAL IF QUIT THEN

    \ J 32 * I + 22528 + IDX @ 8 * SWAP C!
    J I IDX @ +COLOR PLOT
  LOOP
LOOP ;

