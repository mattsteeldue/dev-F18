---
description: Create a new CODE word (Z80 machine code) in inc/ using hex literals. Usage: /new-code-word <WORD-NAME>
---

Create a new low-level CODE word file in inc/ for the word named $ARGUMENTS.

FAT filename character mapping:
| Forth | File |
|-------|------|
| :     | _    |
| ?     | ^    |
| /     | %    |
| *     | &    |
| |     | $    |
| <     | {    |
| >     | }    |
| "     | ~    |

Steps:
1. Apply the FAT mapping to $ARGUMENTS to get the filename.
2. Check that inc/<fat-name>.f does not already exist.
3. Create inc/<fat-name>.f with this CODE template:

   \
   \ <fat-name>.f
   \
   .( <WORD-NAME> )
   \
   CODE <WORD-NAME>
       $XX C,             \ opcode (lowercase comment)
       $DD C, $E9 C,      \ jp (ix)  -- Next
       SMUDGE
       \

   Rules:
   - Use $-prefixed hex literals (e.g. $DD C,). Never switch BASE (no HEX/DECIMAL).
   - Z80 opcode comments in lowercase for reading fluency.
   - The last two bytes $DD C, $E9 C, are jp (ix) -- the inner interpreter Next.
     Keep them unless this word has a non-standard exit (e.g. RET or conditional branch).
   - Do NOT add NEEDS ASSEMBLER. CODE words in inc/ must not depend on the assembler
     vocabulary (~7 KB overhead).
   - Use $, %, # prefix characters for all numeric literals.

4. Copy the same content to SD/tools/vForth/inc/<fat-name>.f.
5. Report both created files and remind the user to replace $XX with the actual opcodes.