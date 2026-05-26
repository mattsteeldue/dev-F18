
needs layer2  needs layer12
needs wait-key
needs FLIP

HEX 12 reg@ 2* CONSTANT Layer2-Base-Page  \ 8K Base page for Layer 2

create filename ," C:/demos/bmp256converts/bitmaps/critters.bmp"
0 variable fh-BMP

DECIMAL
: LOAD-BMP< ( a -- )
    1+ 0 01 f_open 41 ?error fh-BMP !
    PAD 14 fh-BMP @ f_read swap 14 - or 46 ?error \ read error
    PAD @ [ HEX ] 4D42 [ decimal ] -    38 ?error \ not BMP
    PAD 10 + 2@ swap fh-BMP @ f_seek    45 ?error \ seek error
    6 0 DO
        5 I - LAYER2-BASE-PAGE + MMU7! \ CR I .
        32 0 DO
            31 I - FLIP [ HEX ] E000 or [ DECIMAL ] \ destination addr
            256 fh-BMP @ f_read  1 ?error drop
        LOOP
    LOOP
    fh-BMP @ f_close 42 ?error
;

: show-layer2
    layer2 wait-key layer12
;

filename LOAD-BMP<
show-layer2
