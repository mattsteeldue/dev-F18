---
description: Create the next numbered tutorial file in tutorial/. Usage: /new-tutorial <topic description>
---

Create a new tutorial file in tutorial/ for the topic described in $ARGUMENTS.

Steps:
1. Scan tutorial/ for files matching NNN-*.f (three-digit prefix). Find the highest
   existing number and add 1. If no numbered files exist, start at 001.
2. Convert $ARGUMENTS to a kebab-case slug: lowercase, spaces to hyphens, remove
   characters that are unsafe in filenames.
3. New filename: tutorial/<NNN>-<slug>.f
4. Create the file with this template (7-bit ASCII, no BOM):

   \
   \ <NNN>-<slug>.f
   \ <Brief one-line description of this tutorial.>
   \

   MARKER NO-<SLUG-UPPER>

   \ --- Introduction ---
   \ <Explain the concept here. Tutorials are comment-heavy -- explain the WHY,
   \  show stack effects, describe expected output.>

   .( Tutorial <NNN>: <Topic> loaded. )

   \ --- Example ---
   \ Expected output: ...

   \ : DEMO  ( -- )
   \     ;

   \ To reset this tutorial: NO-<SLUG-UPPER>

   Rules:
   - Each tutorial must be self-contained: use NEEDS for every dependency.
   - MARKER NO-<NAME> near the top for interactive reset.
   - Show expected output as comments.
   - Later tutorials may use NEEDS to load vocabulary from earlier ones, but must
     not use INCLUDE tutorial/NNN-...f.

5. Report the created filename and its number.