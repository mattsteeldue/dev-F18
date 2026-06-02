---
description: Show the FAT filename mapping for a Forth word name. Usage: /fat-name <WORD-NAME>
---

Apply the vForth FAT filename character mapping to the Forth word name $ARGUMENTS.

Mapping table (all other characters are unchanged):
| Forth char | Filename char |
|------------|---------------|
| :          | _             |
| ?          | ^             |
| /          | %             |
| *          | &             |
| |          | $             |
| <          | {             |
| >          | }             |
| "          | ~             |

Steps:
1. Apply the mapping to every character in $ARGUMENTS.
2. Show the result as:
   Forth name  : <original>
   FAT filename: <mapped>.f
   inc/ path   : inc/<mapped>.f
   lib/ path   : lib/<mapped>.f (uppercase)
   help/ path  : help/<mapped>.txt

3. Check whether inc/<mapped>.f and/or lib/<mapped>.f already exist and report.

Note: characters like !, @, +, -, ., # are already legal in FAT filenames and pass
through unchanged. The mapping only applies to the characters in the table above.