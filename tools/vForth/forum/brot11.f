needs j
needs layer11

0 VARIABLE XX 
0 VARIABLE YY
0 VARIABLE X 
0 VARIABLE Y
0 VARIABLE XT 
0 VARIABLE XZ 
0 VARIABLE YZ
0 VARIABLE IDX

100 CONSTANT FXP

: BROT 
layer11
cls

24 0 DO 
  32 0 DO 
    I 350 32 */ 250 - XZ ! 
    J 200 24 */ 100 - YZ ! 
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
    
    J 32 * I + 22528 + IDX @ 8 * SWAP C!
  LOOP 
LOOP ;

