\
\ l1-point.f
\
\ POINT (per-pixel attribute) for Layer 1,0 and Layer 2
\
.( L1-POINT )

NEEDS GRAPHICS-COMMON    \ PIXELADD

: L1-POINT  ( x y -- c )
    PIXELADD C@
;

