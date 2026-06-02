---
description: Create a new single-word definition file in inc/. Usage: /new-word <WORD-NAME>
---

Create a new Forth word file in inc/ for the word named $ARGUMENTS.

FAT filename character mapping (apply to convert Forth name to filename):
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
All other characters (letters, digits, !, @, +, -, ., #, etc.) are unchanged.
Result: inc/<fat-mapped-name>.f

Steps:
1. Apply the FAT mapping to $ARGUMENTS to get the filename.
2. Check that inc/<fat-name>.f does not already exist. If it does, read and show its
   contents instead of overwriting.
3. Create inc/<fat-name>.f with this template (7-bit ASCII, no BOM, LF line endings):

   \
   \ <fat-name>.f
   \
   .( <WORD-NAME> )
   \
   : <WORD-NAME>  ( -- )
       ;

   - Word name in UPPERCASE.
   - Replace ( -- ) with the correct stack effect if the user provided one.
   - All source must be 7-bit ASCII only (0x20-0x7E, 0x09, 0x0A, 0x0D, 0x7F).

4. Copy the same content to SD/tools/vForth/inc/<fat-name>.f.
5. Report both created files and remind the user to fill in the implementation.