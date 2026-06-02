---
description: Create a new library module in lib/. Usage: /new-lib <MODULE-NAME>
---

Create a new Forth library module in lib/ for the module named $ARGUMENTS.

Steps:
1. Convert $ARGUMENTS to uppercase (e.g. "graphics" -> "GRAPHICS").
2. Check that lib/<NAME>.f does not already exist. If it does, read and show its
   contents instead of overwriting.
3. Create lib/<NAME>.f with this template (7-bit ASCII, no BOM):

   \
   \ <NAME>.f
   \
   .( <NAME> )
   \
   NEEDS MARKER
   MARKER NO-<NAME>
   \
   \ NEEDS <dependency>
   \
   \ : <WORD>  ( -- )
   \     ;
   \

   Rules:
   - MARKER NO-<NAME> near the top: lets the entire module be removed in one step
     during interactive development.
   - Use NEEDS for every dependency -- never assume a word is already loaded.
   - If a definition is general enough to be useful independently, extract it to
     inc/ and replace the inline definition with NEEDS.

4. Copy the same content to SD/tools/vForth/lib/<NAME>.f.
5. Report both created files.