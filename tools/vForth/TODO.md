## Possible improvements and Known Bugs

# improve (COMPARE) 
**2026-05-27**
because it uses djnz strings can be 256 bytes in length at most.
Register C seems free: modify the code to use BC instead of B as counter.
**Status: Done** 2026-05-31


# ?VOCAB and .VOCAB are broken 
**2026-06-01**
Tested on real hardware; both definitions do not work correctly.
Removed from tutorial/018-vocabularies.f until fixed.


# EVALUATE little bug
**2026-05-31**
I just discovered this definition has to be put on a new line to work *always*.
Tutorial 021 shows that if written on the same line of some complex evaluating 
strings it does not work well.


# F>D in FLOATING library has bug
**2026-06-01**
The example in tutorial 024:  3.7 F>D D. display 37 instead of 3
Removed from tutorial/024-floating-point.f until fixed.    
UPDATE: False positive, probably I missed typing FLOATING before testing.
**Status: Done** 2026-06-02

