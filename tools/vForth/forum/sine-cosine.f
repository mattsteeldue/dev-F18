\ Sinus und Cosinus
\ Tabellengestützte Berechnung für ganze Zahlen.
\ Ergibt auf 10K skalierte Werte.
\ Prototypische Lösung mittels:
\ Gforth 0.6.2, Copyright (C) 1995-2003 Free Software Foundation, Inc.

\ Tabular calculation for whole numbers. 
\ Results in values scaled to 10K
\
NEEDS TRUE
NEEDS FALSE
NEEDS CELL


vocabulary sinus sinus definitions decimal

create sinustabelle \ 0…90 Grad, Index in Grad
0000 , 0175 , 0349 , 0523 , 0698 , 0872 ,
1045 , 1219 , 1392 , 1564 , 1736 , 1908 ,
2079 , 2250 , 2419 , 2588 , 2756 , 2924 ,
3090 , 3256 , 3420 , 3584 , 3746 , 3907 ,
4067 , 4226 , 4384 , 4540 , 4695 , 4848 ,
5000 , 5150 , 5299 , 5446 , 5592 , 5736 ,
5878 , 6018 , 6157 , 6293 , 6428 , 6561 ,
6691 , 6820 , 6947 , 7071 , 7193 , 7314 ,
7431 , 7547 , 7660 , 7771 , 7880 , 7986 ,
8090 , 8192 , 8290 , 8387 , 8480 , 8572 ,
8660 , 8746 , 8829 , 8910 , 8988 , 9063 ,
9135 , 9205 , 9272 , 9336 , 9397 , 9455 ,
9511 , 9563 , 9613 , 9659 , 9703 , 9744 ,
9781 , 9816 , 9848 , 9877 , 9903 , 9925 ,
9945 , 9962 , 9976 , 9986 , 9994 , 9998 ,
10000 ,



: sinus@ cell * sinustabelle + @ ;

: sin ( grad — sinus )
  dup >r                \ save grad sign
  abs 360 mod
  dup 180 > if 180 –  -1  else  1  then >r
  dup  90 > if 180 swap – then
  sinus@
  r> +-
  r> +- ;
 
: cos 90 + sin ;