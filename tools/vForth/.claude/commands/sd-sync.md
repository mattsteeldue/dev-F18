---
description: Synchronize inc/ and lib/ files to SD/tools/vForth/ (copies missing and outdated files).
---

Synchronize root inc/ and lib/ directories to SD/tools/vForth/ by copying all files
that are missing or outdated in the SD staging area.

Steps:
1. Run the same audit as /check-sync: find all MISSING and OUTDATED files in
   SD/tools/vForth/inc/ and SD/tools/vForth/lib/.

2. If there are no files to sync, report "Already in sync. Nothing to copy." and stop.

3. Show the list of files that will be copied and ask the user to confirm before
   proceeding. Do not copy until confirmation is received.

4. After confirmation, copy each file:
   - inc/<filename>  ->  SD/tools/vForth/inc/<filename>
   - lib/<filename>  ->  SD/tools/vForth/lib/<filename>
   Preserve content exactly: no encoding conversion, no BOM added.
   Use PowerShell Copy-Item or [System.IO.File]::Copy to avoid encoding pitfalls.

5. Report the total number of files copied and list each one.

6. Reminder: this updates the PC-side SD staging area only. To transfer to the
   physical SD card, use the Komppa sync utility (separate step).