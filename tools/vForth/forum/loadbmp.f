
needs layer2  needs layer12
needs wait-key
needs FLIP

HEX 12 reg@ 2* CONSTANT Layer2-Base-Page  \ 8K Base page for Layer 2

create filename ," C:/demos/bmp256converts/bitmaps/critters.bmp"
0 variable fh-BMP

DECIMAL
: LOAD-BMP< ( a -- )  \ a is a counted z-string address, the kind created by ,"
    1+ 0 01 f_open 41 ?error fh-BMP !
    PAD 14 fh-BMP @ f_read swap 14 - or 46 ?error \ read error
    PAD @ [ HEX ] 4D42 [ decimal ] -    41 ?error \ not a BMP file
    PAD 10 + 2@ swap fh-BMP @ f_seek    45 ?error \ skip header
    6 0 DO
        5 I - LAYER2-BASE-PAGE + MMU7!  \ fit the correct page at MMU7
        32 0 DO
            31 I - FLIP [ HEX ] E000 OR [ DECIMAL ] \ destination address
            256 fh-BMP @ f_read 46 ?error drop \ ignore number of byte read
        LOOP
    LOOP
    fh-BMP @ f_close 42 ?error
;
: show-layer2
    layer2 wait-key layer12
;

filename LOAD-BMP<
show-layer2
