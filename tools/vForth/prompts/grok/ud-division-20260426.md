You are an expert in vForth system which repository is stored at this location: https://github.com/mattsteeldue/vforth-next/tree/master

Latest official documentation is given by the document vForth1.8-core-en-20260419.pdf available at the same location https://github.com/mattsteeldue/vforth-next/tree/master/doc

The current core v.1.8 is built using VSCode using Z80 assembly source code available in project/DIRECT_MMU7
The core is maintainded in vForth itself, the source is given in src/F18e.f

A double-integer is usually kept in CPU registers as HLDE then pushed on stack.
On the stack a double number is treated as two single numbers where HL is on the top of the stack and DE is the second from top, so in the stack memory it appears as LHED. Instead, in 2VARIABLE a double number is stored as EDLH.

Today's task is to help create a new definitions that accepts an unsigned double precision integer ud1 and an unsigned integer u1 and computes the unsigned floored integer division ud1/u1 and returns an unsigned integer u2 as remainder and an unsigned double precision integer ud2 as quotient

________________________

How to modify the initial prompt for the best answer next time:

Include these key pieces of information from the very first message:

Exact stack order for double numbers in vForth (e.g.: “In vForth, an unsigned double ud is represented on the data stack with the high cell on top (high low), while in memory (2@/2!/2VARIABLE) it is stored low-cell first (low high). In registers it is often HLDE with HL = high cell.”)

Desired output stack order (e.g.: “Return ud2 with high cell on top, like other double words in the system.” or “I want remainder first then quotient” etc.)

Whether you prefer high-level colon (:) or low-level CODE definition using Z80N registers (HL/DE/BC etc.)

The exact name and purpose you want (e.g. UD/, UD/MOD, MU/MOD, floored vs truncated, etc.)

Any existing primitives you want to build upon (especially how UM/MOD behaves with doubles in vForth).

Any constraints (size, speed, no return stack usage, etc.)

Example of a strong initial prompt:"In vForth (Z80N), doubles are on the stack with high cell on top (high low). In memory they are stored low first. 

Write a colon definition : UD/ ( ud1 u -- ud2 ) that performs unsigned division of unsigned double ud1 by single u, returning the unsigned double quotient ud2 (high cell on top). Use only UM/MOD, >R, etc. 

Provide stack comments and a short explanation."




