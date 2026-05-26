\ search-string.f
\
\ from Simon N Goodwin's Facebook post
\ 2190 REM DEMO: String array searching via VARS
\ 2200 CLEAR 65399: DIM A$(1000,16): DIM Z$(16):%s=65400
\ 2210 POKE %s,%33,%256,%0,%45432,%58824,%11017,%58851,%17,%256,
\ %0,%45177,%8232,%6853,%41453,%2336,%30739,%8369,%57846,%57793,
\ %49609,%53729,%2517,%60389,%21229,%12513,%57818,%1,%51456,%57825,%201


CREATE X    

33 , 256 , 0 , 45432 , 58824 , 11017 , 58851 , 17 , 256 ,
0 , 45177 , 8232 , 6853 , 41453 , 2336 , 30739 , 8369 , 57846 , 57793 ,
49609 , 53729 , 2517 , 60389 , 21229 , 12513 , 57818 , 1 , 51456 , 57825 , 
201 ,


\   8E48
\       LD      HL, 0       ; S: start address of array to search
\       LD      BC, 0       ; T: target length (1000*16)
\       LD      A,B
\       OR      C
\       RET     Z           ; quit if length is zero, BC = zero
\       PUSH    HL          ;       \ TOS: S (start)
\       ADD     HL, BC      ; 
\       DEC     HL          ; F (finish)
\       EX      (SP), HL    ; S     \ TOS: F (finish)
\   8E55
\       PUSH    HL          ;       \ TOS: S F
\       LD      DE, 0       ; search pattern start address
\       LD      BC, 0       ; L: pattern length in bytes (16)
\       LD      A, C    
\       OR      B
\       JR      Z, 8E80     ; skip if zero length
\       PUSH    BC          ;       \ TOS: L S F
\   8E61
\       LD      A, (DE)     ;
\       CPI                 ; search a byte from addr
\       JR      NZ, 8E6F    ; skip if not found
\       INC     DE          ; found then continue until 
\       LD      A, B        ; end of matching string
\       OR      C
\       JR      NZ, 8E61    ; not end of matching string
\       POP     HL          ; end of matching string
\       POP     BC          ; retrieve address of positive search
\       POP     HL          ; discard
\       RET                 ; return BC = address of match
\   8E6F
\       POP     BC          ; L       \ TOS: S F
\       POP     HL          ; S       \ TOS: F
\       POP     DE          ; F       \ TOS:  
\       PUSH    DE          ; F       \ TOS: F
\       ADD     HL, BC      ; S+L     \ 
\       PUSH    HL          ;         \ TOS: S+L  F
\       EX      DE, HL      ; F
\       SBC     HL, DE      ; F-S-L
\       POP     HL          ; S+L     \ TOS: F (finish)
\       JR      NC, 8E55    ; 
\       POP     HL
\       LD      BC, 0
\       RET                 ; return BC = zero
\   8E80
\       POP     HL
\       POP     HL
\       RET                 ; return BC = zero

