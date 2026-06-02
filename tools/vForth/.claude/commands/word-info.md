---
description: Look up a vForth word: definition, stack effect, and usage. Usage: /word-info <WORD-NAME>
---

Find and summarize information about the Forth word named $ARGUMENTS.

FAT filename mapping (to compute candidate filenames):
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
1. Apply the FAT mapping to $ARGUMENTS to get <fat-name>.
2. Search in this order and collect all hits:
   a. inc/<fat-name>.f  -- single-word definition (read full file if found)
   b. lib/*.f           -- search for ": <WORD-NAME> " or "CODE <WORD-NAME>"
                          and show the matching definition block
   c. help/<fat-name>.txt -- quick reference card (read full file if found)
   d. src/F18e.f        -- core Forth source (search for the word definition;
                          show the surrounding block)
3. For each source found, display:
   - File path and the relevant content.
   - For inc/ files (short): full content.
   - For lib/ and src/F18e.f: the definition block only.
   - For help/: full content.
4. Summarize: stack effect, what the word does, any notable dependencies or caveats.
5. If the word is not found anywhere, say so and suggest checking for a FAT name
   mismatch or whether the word is built into forth18e.bin (core, no source file).