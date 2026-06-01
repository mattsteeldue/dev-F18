## Possible improvements.

# improve (COMPARE) 
because it uses djnz strings can be 256 bytes in length at most.
Register C seems free: modify the code to use BC instead of B as counter.
**Status: Done**

# ?VOCAB and .VOCAB are broken
Tested on real hardware; both definitions do not work correctly.
Removed from tutorial/018-vocabularies.f until fixed.

 