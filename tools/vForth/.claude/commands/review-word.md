---
description: Review a vForth inc/ word file for coding convention compliance. Usage: /review-word <WORD-NAME>
---

Review the inc/ file for the word named $ARGUMENTS against vForth coding conventions.

FAT filename mapping:
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
1. Apply FAT mapping to $ARGUMENTS to locate inc/<fat-name>.f.
2. Read the file. If not found, report and stop.
3. Check each convention and report PASS or the list of issues with line numbers:

   a. CHARACTER ENCODING
      All bytes must be in range 0x20-0x7E, 0x09 (tab), 0x0A (LF), 0x0D (CR),
      0x7F (copyright). No UTF-8 multibyte sequences. No BOM (EF BB BF prefix).

   b. FAT FILENAME CONSISTENCY
      The .( NAME ) line and the word name in : NAME or CODE NAME must match
      $ARGUMENTS exactly (case-sensitive, Forth names are uppercase).

   c. HEX LITERALS IN CODE WORDS
      If the file contains a CODE word, all numeric literals must use $, %, or #
      prefix. Flag any bare decimal literal or BASE switch (HEX/DECIMAL) inside
      the body.

   d. NO BASE SWITCHING DURING COMPILATION
      HEX or DECIMAL inside a colon definition or CODE block is flagged.
      (Allowed only for output formatting at interpret time.)

   e. NO ASSEMBLER DEPENDENCY
      CODE words in inc/ must not use NEEDS ASSEMBLER. Flag it if present.

   f. COMMENT QUALITY
      Comments should explain WHY (hidden constraint, workaround, subtle invariant).
      Flag multi-line comment blocks or comments that merely restate the code.

   g. NEEDS COMPLETENESS
      Every word used but not defined in this file should have a corresponding
      NEEDS at the top. List any words that appear to be missing a NEEDS.

4. Final verdict: PASS (all checks ok) or ISSUES FOUND (list each issue).